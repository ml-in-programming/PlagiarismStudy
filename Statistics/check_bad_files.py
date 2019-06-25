import re
import os
from urllib.parse import unquote

bookkeeping_projects_name = {}
bookkeeping_projects_address = {}
number_of_projects_all = 0
with open('../SourcererCC/tokenizers/block-level/bookkeeping_projs/bookkeeping-proj-all.projs','r') as fin:
    for line in fin:
        number_of_projects_all = number_of_projects_all + 1
        x = line.split(',')
        name = re.match(r'"((.*)\/(.*)).zip"',x[1])
        bookkeeping_projects_name[int(x[0])] = name.group(3)
        bookkeeping_projects_address[int(x[0])] = name.group(1)

bookkeeping_files_project = {}
bookkeeping_files_address = {}
number_of_files_all = 0
with open('../SourcererCC/tokenizers/block-level/file_block_stats/files-stats-all.stats','r') as fin:
    with open('commas_files.txt','w') as fout:
        for line in fin:
            x = line.split(',')
            name = re.match(r'"NULL/([^\/]*)\/(.*)"',x[4])
            if x[0][0] == 'f':
                number_of_files_all = number_of_files_all + 1
                bookkeeping_files_project[int(x[2])] = int(x[1])
                if name is not None:
                    bookkeeping_files_address[int(x[2])] = name.group(2)
                else:
                    fout.write(str(number_of_files_all) + ';' + line)
        fout.write(str(number_of_files_all))

bad_files = 0
for i in bookkeeping_files_address.keys():
    full_address = bookkeeping_projects_address[bookkeeping_files_project[i]] + '/' + unquote(bookkeeping_files_address[i])
    if os.path.isfile(full_address) is False:
        bad_files = bad_files + 1
        print(bad_files, full_address)
