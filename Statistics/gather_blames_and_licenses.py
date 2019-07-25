import re
import time
from subprocess import PIPE, Popen
from os import mkdir, path
from datetime import datetime, timedelta
from urllib.parse import unquote

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def getLicense(fileid):
    command = 'perl ninka/ninka.pl -d \"' + bookkeeping_projects_address[bookkeeping_files_project[fileid]] + '/' + bookkeeping_files_address[fileid] + '\"'
    return(cmdline(command).decode('utf8'))

def getBlame(fileid):
    command = '(cd ' + bookkeeping_projects_address[bookkeeping_files_project[fileid]] + '; git blame \"' + bookkeeping_files_address[fileid] + '\")'
    blame = cmdline(command).decode('utf8').split('\n')
    result = {}
    for i in range(len(blame)-1):
        name = re.search(r'(\d{4}-\d{2}-\d{2})',blame[i])
        result[i + 1] = datetime.strptime(name.group(1),'%Y-%m-%d')
    return(result)

def largestMode(numbers):
    counts = {k:numbers.count(k) for k in set(numbers)}
    modes = sorted(dict(filter(lambda x: x[1] == max(counts.values()), counts.items())).keys())
    return modes[-1]

def currentTime():
    return str(timedelta(seconds = time.time() - start_time)).split('.')[0]

start_time = time.time()

print(currentTime(), 'STARTED OPERATING — GATHERING DATA')

if not path.exists('data'):
    mkdir('data')
    
set_of_blocks_temporary = set()
set_of_blocks_extended = set()
set_of_files_extended = set()
set_of_projects_extended = set()
with open('../SourcererCC/results.pairs','r') as fin:
    with open('data/results.pairs.different','w') as fout:
        for line in fin:
            x = line.split(',')
            if int(x[0]) != int(x[2]):
                set_of_blocks_temporary.add(int(x[1]))
                set_of_blocks_temporary.add(int(x[3]))
                fout.write(x[0] + ',' + x[1] + ',' + x[2] + ',' + x[3])

print(currentTime(), 'Created the lists and dictionaries of resulting pairs, part 1')
                    
with open('../SourcererCC/results.pairs','r') as fin:
    with open('data/results.pairs.different.extended','w') as fout:
        for line in fin:
            x = line.split(',')
            if (int(x[1]) in set_of_blocks_temporary) or (int(x[3]) in set_of_blocks_temporary):
                fout.write(x[0] + ',' + x[1] + ',' + x[2] + ',' + x[3])
                set_of_blocks_extended.add(int(x[1]))
                set_of_blocks_extended.add(int(x[3]))
                set_of_files_extended.add(int(x[1][5:]))
                set_of_files_extended.add(int(x[3][5:]))
                set_of_projects_extended.add(int(x[0]))
                set_of_projects_extended.add(int(x[2]))
set_of_blocks_temporary = None
del set_of_blocks_temporary

print(currentTime(), 'Created the lists and dictionaries of resulting pairs, part 2')

bookkeeping_projects_name = {}
bookkeeping_projects_address = {}
with open('../SourcererCC/tokenizers/block-level/bookkeeping_projs/bookkeeping-proj-all.projs','r') as fin:
    for line in fin:
        x = line.split(',')
        if int(x[0]) in set_of_projects_extended:
            name = re.match(r'"((.*)\/(.*)).zip"',x[1]) 
            bookkeeping_projects_name[int(x[0])] = name.group(3)
            bookkeeping_projects_address[int(x[0])] = name.group(1)
            
print(currentTime(), 'Created a dictionary of projects')

bookkeeping_blocks_project = {}
bookkeeping_blocks_name = {}
bookkeeping_blocks_length = {}
with open('../SourcererCC/tokenizers/block-level/blocks_tokens/files-tokens-all.tokens','r',encoding='utf8') as fin:
    for line in fin:
        x = line.split(',')
        if int(x[1]) in set_of_blocks_extended:
            bookkeeping_blocks_project[int(x[1])] = int(x[0])
            name = line.split(')')[0].split('(')[0].split(',')[4] + '(' + line.split(')')[0].split('(')[1] + ')'
            bookkeeping_blocks_name[int(x[1])] = name
            bookkeeping_blocks_length[int(x[1])] = int(x[2])
            
print(currentTime(), 'Created various dictionaries of blocks')

bookkeeping_files_project = {}
bookkeeping_files_address = {}
bookkeeping_blocks_lines = {}
with open('../SourcererCC/tokenizers/block-level/file_block_stats/files-stats-all.stats','r') as fin:
    with open('data/statistics_bad_files.txt','w') as fout:
        for line in fin:
            x = line.split(',')
            if (x[0][0] == 'f') and (int(x[2]) in set_of_files_extended):
                bookkeeping_files_project[int(x[2])] = int(x[1])
                name = re.match(r'"NULL/([^\/]*)\/(.*)"',x[4])
                if (name is not None) and ('(' not in unquote(name.group(2))) and (')' not in unquote(name.group(2))) and ('\'' not in unquote(name.group(2))) and ('\"' not in unquote(name.group(2))):
                    bookkeeping_files_address[int(x[2])] = unquote(name.group(2))
                else:
                    fout.write(line)
                    set_of_files_extended.remove(int(x[2]))
            if (x[0][0] == 'b') and (int(x[2]) in set_of_blocks_extended):
                bookkeeping_blocks_lines[int(x[2])] = [int(x[7]),int(x[8])]
            
print(currentTime(), 'Created a dictionary of files and block lines, as well as filtered bad files, total amount of files to process:',len(set_of_files_extended))

set_of_blocks_extended_copy = set_of_blocks_extended.copy()
for i in set_of_blocks_extended_copy:
    if int(str(i)[5:]) not in set_of_files_extended:
        set_of_blocks_extended.remove(i)
set_of_blocks_extended_copy = None
del set_of_blocks_extended_copy

print(currentTime(), 'Filtered blocks from bad files', len(set_of_blocks_extended))

bookkeeping_projects_default_license = {}
for i in set_of_projects_extended:
    with open(bookkeeping_projects_address[i] + '.txt','r') as fin:
        x = fin.readline().rstrip()
        if ':' in x:
            if ',' in x:
                bookkeeping_projects_default_license[i] = x.split(',')[0].split(':')[0]
            else:
                bookkeeping_projects_default_license[i] = x.split(':')[0]
        else:
            bookkeeping_projects_default_license[i] = 'GitHub'
            
print(currentTime(), 'Created a dictionary of default projects licenses')

with open('data/statistics_licenses.txt','w') as fout:
    bookkeeping_files_license = {}
    bookkeeping_files_license_processed = {}
    for i in set_of_files_extended:
        bookkeeping_files_license[i] = getLicense(i)
        x = bookkeeping_files_license[i].split(';')
        if x[1].rstrip() == 'NONE' or x[1].rstrip() == 'UNKNOWN':
            x[1] = bookkeeping_projects_default_license[bookkeeping_files_project[i]]
        bookkeeping_files_license_processed[i] = x[1].rstrip()
        fout.write(str(i) + ';' + bookkeeping_projects_address[bookkeeping_files_project[i]] + '/' + bookkeeping_files_address[i]  + ';' + bookkeeping_files_license_processed[i] + '\n')
        
print(currentTime(), 'Created a dictionary and a text file with the licenses')

with open('data/statistics_blame.txt','w') as fout:
    bookkeeping_files_blame = {}
    for i in set_of_files_extended:
        bookkeeping_files_blame[i] = getBlame(i)
        fout.write(str(i) + ';' + bookkeeping_projects_address[bookkeeping_files_project[i]] + '/' + bookkeeping_files_address[i] + '/' + str(bookkeeping_files_blame[i]) + '\n')
        
print(currentTime(), 'Created a dictionary and a text file of files blames')

with open('data/statistics_blame_processed.txt','w') as fout:
    bookkeeping_blocks_blame_processed = {}
    for i in set_of_blocks_extended:
        bookkeeping_blocks_blame = []
        for j in range(bookkeeping_blocks_lines[i][0],bookkeeping_blocks_lines[i][1] + 1):
            bookkeeping_blocks_blame.append(bookkeeping_files_blame[int(str(i)[5:])][j])
        bookkeeping_blocks_blame_processed[i] = largestMode(bookkeeping_blocks_blame)
        fout.write(str(i) + ';' + bookkeeping_projects_address[bookkeeping_blocks_project[i]] + '/' + bookkeeping_files_address[int(str(i)[5:])] + ';' + str(bookkeeping_blocks_lines[i][0]) + '-' + str(bookkeeping_blocks_lines[i][1]) + ';' + str(bookkeeping_blocks_blame_processed[i]) + '\n')
        
print(currentTime(), 'Created a dictionary and a text file of blocks blames processed')
