import numpy as np
import re
import networkx as nx
import time
from matplotlib import pyplot
from operator import itemgetter
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

print(currentTime(), 'STARTED OPERATING')

if not path.exists('data'):
    mkdir('data')
bookkeeping_projects_frequency = {}
bookkeeping_blocks_frequency = {}
set_of_blocks_temporary = set()
set_of_blocks_extended = set()
set_of_files_extended = set()
set_of_projects_extended = set()
number_of_project_pairs_all = 0
number_of_project_pairs = 0
with open('../SourcererCC/results.pairs','r') as fin:
    with open('data/results.pairs.different','w') as fout:
        for line in fin:
            number_of_project_pairs_all = number_of_project_pairs_all + 1
            x = line.split(',')
            if int(x[0]) != int(x[2]):
                number_of_project_pairs = number_of_project_pairs + 1
                set_of_blocks_temporary.add(int(x[1]))
                set_of_blocks_temporary.add(int(x[3]))
                fout.write(x[0] + ',' + x[1] + ',' + x[2] + ',' + x[3])
                if int(x[0]) not in bookkeeping_projects_frequency.keys():
                    bookkeeping_projects_frequency[int(x[0])] = 1
                else:
                    bookkeeping_projects_frequency[int(x[0])] = bookkeeping_projects_frequency[int(x[0])] + 1
            
                if int(x[2]) not in bookkeeping_projects_frequency.keys():
                    bookkeeping_projects_frequency[int(x[2])] = 1
                else:
                    bookkeeping_projects_frequency[int(x[2])] = bookkeeping_projects_frequency[int(x[2])] + 1
            
                if int(x[1]) not in bookkeeping_blocks_frequency.keys():
                    bookkeeping_blocks_frequency[int(x[1])] = 1
                else:
                    bookkeeping_blocks_frequency[int(x[1])] = bookkeeping_blocks_frequency[int(x[1])] + 1
        
                if int(x[3]) not in bookkeeping_blocks_frequency.keys():
                    bookkeeping_blocks_frequency[int(x[3])] = 1
                else:
                    bookkeeping_blocks_frequency[int(x[3])] = bookkeeping_blocks_frequency[int(x[3])] + 1
number_of_projects_different = len(bookkeeping_projects_frequency)

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
number_of_projects_all = 0
with open('../SourcererCC/tokenizers/block-level/bookkeeping_projs/bookkeeping-proj-all.projs','r') as fin:
    for line in fin:
        number_of_projects_all = number_of_projects_all + 1
        x = line.split(',')
        if int(x[0]) in set_of_projects_extended:
            name = re.match(r'"((.*)\/(.*)).zip"',x[1]) 
            bookkeeping_projects_name[int(x[0])] = name.group(3)
            bookkeeping_projects_address[int(x[0])] = name.group(1)
for i in bookkeeping_projects_name.keys():
    if i not in bookkeeping_projects_frequency.keys():
        bookkeeping_projects_frequency[i] = 0

print(currentTime(), 'Created a dictionary of projects')

bookkeeping_blocks_project = {}
bookkeeping_blocks_name = {}
bookkeeping_blocks_length = {}
number_of_blocks = 0
with open('../SourcererCC/tokenizers/block-level/blocks_tokens/files-tokens-all.tokens','r',encoding='utf8') as fin:
    for line in fin:
        number_of_blocks = number_of_blocks + 1
        x = line.split(',')
        if int(x[1]) in set_of_blocks_extended:
            bookkeeping_blocks_project[int(x[1])] = int(x[0])
            name = line.split(')')[0].split('(')[0].split(',')[4] + '(' + line.split(')')[0].split('(')[1] + ')'
            bookkeeping_blocks_name[int(x[1])] = name
            bookkeeping_blocks_length[int(x[1])] = int(x[2])

print(currentTime(), 'Created various dictionaries of blocks')

sorted_projects_frequency = sorted(bookkeeping_projects_frequency.items(), key=itemgetter(1), reverse = True)
sorted_blocks_frequency = sorted(bookkeeping_blocks_frequency.items(), key=itemgetter(1), reverse = True)
sorted_blocks_length = sorted(bookkeeping_blocks_length.items(), key=itemgetter(1), reverse = True)
sorted_projects_frequency = np.asarray(sorted_projects_frequency)
sorted_blocks_frequency = np.asarray(sorted_blocks_frequency)
sorted_blocks_length = np.asarray(sorted_blocks_length)

print(currentTime(), 'Created sorted lists of blocks and projects')

with open('data/statistics_most_frequent_projects.txt','w') as fout:
    for i in sorted_projects_frequency:
        fout.write(bookkeeping_projects_name[i[0]] + ';' + str(i[1]) + '\n')

print(currentTime(), 'Created a text file with the most frequent projects')

with open('data/statistics_most_frequent_blocks.txt','w') as fout:
    for i in sorted_blocks_frequency:
        fout.write(str(i[0]) + ';' + str(i[1]) + '\n')

print(currentTime(), 'Created a text file with the most frequently copied blocks')

with open('data/statistics_largest_blocks.txt','w') as fout:
    for i in sorted_blocks_length:
        fout.write(str(i[0]) + ';' + str(i[1]) + '\n')

print(currentTime(), 'Created a text file with the largest copied blocks')

pyplot.bar(sorted_projects_frequency[:, 0], sorted_projects_frequency[:, 1], align='center')
pyplot.xticks(sorted_projects_frequency[:, 0])
pyplot.title('Projects distribution by number of inter-project clone')
pyplot.xlabel('Project ID')
pyplot.ylabel('Number of clones')
pyplot.savefig('data/projects.png')
pyplot.close()

print(currentTime(), 'Created a bar graph of the projects frequency')

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

graph_pairs_extended = nx.Graph()
graph_pairs_extended.add_nodes_from(set_of_blocks_extended)
with open ('data/results.pairs.different.extended','r') as fin:
    for line in fin:
        x = line.split(',')
        if (int(x[1][5:]) in set_of_files_extended) and (int(x[3][5:]) in set_of_files_extended):
            graph_pairs_extended.add_edge(int(x[1]),int(x[3]))

list_of_cliques_extended = [clique for clique in nx.find_cliques(graph_pairs_extended) if len(clique)>1]
graph_pairs_extended = None
del graph_pairs_extended
print(currentTime(), 'Created a graph of clones and a list of all cliques for different project (extended)')

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

with open('data/statistics_plagiarism.txt','w') as fout:
    with open('data/statistics_sets_of_blocks.txt','w') as fout2:
        with open('data/statistics_licenses_pairs.txt','w') as fout3:
            set_of_license_pairs = set()
            for i in list_of_cliques_extended:
                bookkeeping_cliques_blame = {}
                for j in i:
                    bookkeeping_cliques_blame[j] = bookkeeping_blocks_blame_processed[j]
                sorted_cliques_blame = sorted(bookkeeping_cliques_blame.items(), key=itemgetter(1), reverse = False)
                sorted_cliques_blame = np.asarray(sorted_cliques_blame)
                fout.write(str(sorted_cliques_blame[0][0]) + ';' + bookkeeping_projects_address[bookkeeping_blocks_project[sorted_cliques_blame[0][0]]] + '/' + bookkeeping_files_address[int(str(sorted_cliques_blame[0][0])[5:])] + ';' + str(bookkeeping_blocks_lines[sorted_cliques_blame[0][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_cliques_blame[0][0]][1]) + ';' + str(sorted_cliques_blame[0][1]) + ';' + bookkeeping_files_license_processed[int(str(sorted_cliques_blame[0][0])[5:])] + '\n')
                fout2.write(str(sorted_cliques_blame[0][0]))
                fout2.write(';')
                for k in range(1,len(sorted_cliques_blame)):
                    fout2.write(str(sorted_cliques_blame[k][0]))
                    fout2.write(';')
                    if bookkeeping_blocks_project[sorted_cliques_blame[k][0]] != bookkeeping_blocks_project[sorted_cliques_blame[0][0]]:
                        fout.write('--- ' + str(sorted_cliques_blame[k][0]) + ';' + bookkeeping_projects_address[bookkeeping_blocks_project[sorted_cliques_blame[k][0]]] + '/' + bookkeeping_files_address[int(str(sorted_cliques_blame[k][0])[5:])] + ';' + str(bookkeeping_blocks_lines[sorted_cliques_blame[k][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_cliques_blame[k][0]][1]) + ';' + str(sorted_cliques_blame[k][1]) + ';' + bookkeeping_files_license_processed[int(str(sorted_cliques_blame[k][0])[5:])] + '\n')
                        if (bookkeeping_files_license_processed[int(str(sorted_cliques_blame[k][0])[5:])] + ';' + bookkeeping_files_license_processed[int(str(sorted_cliques_blame[0][0])[5:])]) not in set_of_license_pairs:
                            set_of_license_pairs.add(bookkeeping_files_license_processed[int(str(sorted_cliques_blame[k][0])[5:])] + ';' + bookkeeping_files_license_processed[int(str(sorted_cliques_blame[0][0])[5:])])
                            fout3.write(bookkeeping_files_license_processed[int(str(sorted_cliques_blame[k][0])[5:])] + ';' + bookkeeping_files_license_processed[int(str(sorted_cliques_blame[0][0])[5:])] + '\n')
                fout2.write('\n')

print(currentTime(), 'Created a dictionary and text files of plagiarisms')

with open('data/statistics_genreal.txt','w') as fout:
    fout.write('Total amount of projects checked: ' + str(number_of_projects_all) + '\n')
    fout.write('Out of which the number of projects engaged in inter-project cloning: ' + str(number_of_projects_different) + '\n')
    fout.write('Total number of tokenized blocks: ' + str(number_of_blocks) + '\n')
    fout.write('Total number of found pairs: ' + str(number_of_project_pairs_all) + '\n')
    fout.write('Out of which the number of inter-project pairs: ' + str(number_of_project_pairs) + '\n')
    fout.write('\n')
    fout.write('Top 3 projects by number of inter-project pairs: \n')
    fout.write('1: ' + str(bookkeeping_projects_name[sorted_projects_frequency[0][0]]) + ' (#' + str(sorted_projects_frequency[0][0]) + '), number of pairs: ' + str(sorted_projects_frequency[0][1]) + '\n')
    fout.write('2: ' + str(bookkeeping_projects_name[sorted_projects_frequency[1][0]]) + ' (#' + str(sorted_projects_frequency[1][0]) + '), number of pairs: ' + str(sorted_projects_frequency[1][1]) + '\n')
    fout.write('3: ' + str(bookkeeping_projects_name[sorted_projects_frequency[2][0]]) + ' (#' + str(sorted_projects_frequency[2][0]) + '), number of pairs: ' + str(sorted_projects_frequency[2][1]) + '\n')
    fout.write('The histogram of projects is in "projects.png"\n')
    fout.write('\n')
    fout.write('Top 3 blocks by number of inter-project pairs: \n')
    fout.write('1: ' + str(sorted_blocks_frequency[0][0]) + ' from ' + str(bookkeeping_projects_name[bookkeeping_blocks_project[sorted_blocks_frequency[0][0]]]) + ', ' + str(bookkeeping_blocks_name[sorted_blocks_frequency[0][0]]) + ' (lines ' + str(bookkeeping_blocks_lines[sorted_blocks_frequency[0][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_blocks_frequency[0][0]][1]) +'), located in ' + bookkeeping_files_address[int(str(sorted_blocks_frequency[0][0])[5:])] + ', number of repetitions: ' + str(sorted_blocks_frequency[0][1]) + '\n')
    fout.write('2: ' + str(sorted_blocks_frequency[1][0]) + ' from ' + str(bookkeeping_projects_name[bookkeeping_blocks_project[sorted_blocks_frequency[1][0]]]) + ', ' + str(bookkeeping_blocks_name[sorted_blocks_frequency[1][0]]) + ' (lines ' + str(bookkeeping_blocks_lines[sorted_blocks_frequency[1][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_blocks_frequency[1][0]][1]) +'), located in ' + bookkeeping_files_address[int(str(sorted_blocks_frequency[1][0])[5:])] + ', number of repetitions: ' + str(sorted_blocks_frequency[1][1]) + '\n')
    fout.write('3: ' + str(sorted_blocks_frequency[2][0]) + ' from ' + str(bookkeeping_projects_name[bookkeeping_blocks_project[sorted_blocks_frequency[2][0]]]) + ', ' + str(bookkeeping_blocks_name[sorted_blocks_frequency[2][0]]) + ' (lines ' + str(bookkeeping_blocks_lines[sorted_blocks_frequency[2][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_blocks_frequency[2][0]][1]) +'), located in ' + bookkeeping_files_address[int(str(sorted_blocks_frequency[2][0])[5:])] + ', number of repetitions: ' + str(sorted_blocks_frequency[2][1]) + '\n')
    fout.write('\n')
    fout.write('Top 3 blocks by token length: \n')
    fout.write('1: ' + str(sorted_blocks_length[0][0]) + ' from ' + str(bookkeeping_projects_name[bookkeeping_blocks_project[sorted_blocks_length[0][0]]]) + ', ' + str(bookkeeping_blocks_name[sorted_blocks_length[0][0]]) + ' (lines ' + str(bookkeeping_blocks_lines[sorted_blocks_length[0][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_blocks_length[0][0]][1]) +'), located in ' + bookkeeping_files_address[int(str(sorted_blocks_length[0][0])[5:])] + ', token length: ' + str(sorted_blocks_length[0][1]) + ' (' + str(bookkeeping_blocks_frequency[sorted_blocks_length[0][0]]) + ' clones) \n')
    fout.write('2: ' + str(sorted_blocks_length[1][0]) + ' from ' + str(bookkeeping_projects_name[bookkeeping_blocks_project[sorted_blocks_length[1][0]]]) + ', ' + str(bookkeeping_blocks_name[sorted_blocks_length[1][0]]) + ' (lines ' + str(bookkeeping_blocks_lines[sorted_blocks_length[1][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_blocks_length[1][0]][1]) +'), located in ' + bookkeeping_files_address[int(str(sorted_blocks_length[1][0])[5:])] + ', token length: ' + str(sorted_blocks_length[1][1]) + ' (' + str(bookkeeping_blocks_frequency[sorted_blocks_length[1][0]]) + ' clones) \n')
    fout.write('3: ' + str(sorted_blocks_length[2][0]) + ' from ' + str(bookkeeping_projects_name[bookkeeping_blocks_project[sorted_blocks_length[2][0]]]) + ', ' + str(bookkeeping_blocks_name[sorted_blocks_length[2][0]]) + ' (lines ' + str(bookkeeping_blocks_lines[sorted_blocks_length[2][0]][0]) + '-' + str(bookkeeping_blocks_lines[sorted_blocks_length[2][0]][1]) +'), located in ' + bookkeeping_files_address[int(str(sorted_blocks_length[2][0])[5:])] + ', token length: ' + str(sorted_blocks_length[2][1]) + ' (' + str(bookkeeping_blocks_frequency[sorted_blocks_length[2][0]]) + ' clones) \n')
    
print(currentTime(), 'Created a text file with general statistics')

print(currentTime(), 'FINISHED OPERATING')
