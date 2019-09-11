import os
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

num_lines = sum(1 for line in open('java_projects_data.txt'))
print('// Commencing download of', num_lines, 'projects.')

path = '/home/ubuntu/projects/' 

count = 0
with open('java_projects_data.txt','r') as fin:
    for line in fin:
        count = count + 1
        data = line.split(';')
        os.system('git clone https://user:password@github.com/' + data[0] + '/' + data[1] + ' ' + path + data[0] + '/' + data[1])
        print('// Created folder for', data[0], '/', data[1])
        os.system('curl -L -o ' + path + data[0] + '/' + data[1] + '.zip https://user:password@github.com/' + data[0] + '/' + data[1] + '/zipball/master/')
        print('// Created zip for', data[0], '/', data[1])
        with open(path + data[0] + '/' + data[1] + '.txt', 'w') as fout:
            fout.write(data[2])
        print('// Created text file for', data[0], '/', data[1])
        print('// Completed for project', count, 'out of', num_lines)
        print('___________________________________________')
print('Completed initial download')

with open('java_projects_data.txt','r') as fin:
    with open('list_checks.txt','w') as fout:
        for line in fin:
            data = line.split(';')
            fout.write(data[0] + '/' + data[1] + ';' + str(os.path.isdir(path + data[0] + '/' + data[1])) + ';' + str(os.path.isfile(path + data[0] + '/' + data[1] + '.zip')) + ';' + str(os.path.isfile(path + data[0] + '/' + data[1] + '.txt')) + '\n')

with open('list_checks.txt','r') as fin:
    for line in fin:
        data = line.split(';')
        if data[1] == 'False':
            os.system('rm ' + path + data[0] + '/' + data[1] + '.zip')
            os.system('rm ' + path + data[0] + '/' + data[1] + '.txt')
print('Deleted uncloned projects (deleted or made private)')

with open('java_projects_data','r') as fin:
    with open('list_branches.txt','w') as fout:
        for line in fin:
            data = line.split(';')
            if os.path.isdir(path + data[0] + '/' + data[1]) == True:
                sout = cmdline('(cd ' + path + data[0] + '/' + data[1] + '; git rev-parse --abbrev-ref HEAD)').decode('utf8').rstrip()
                fout.write(data[0] + ';' + data[1] + ';' + sout + '\n')
print('Gathered main branch of every remaining project')

nonmaster = 0
with open ('list_branches.txt','r') as fin:
    for line in fin:
        data = line.split(';')
        if data[2].rstrip() != 'master':
            nonmaster = nonmaster + 1
            os.system('rm -r -f ' + path + data[0] + '/' + data[1])
            print('// Deleted folder for', data[0], '/', data[1])
            os.system('rm -f ' + path + data[0] + '/' + data[1] + '.zip')
            print('// Deleted zip for', data[0], '/', data[1])
            os.system('git clone https://user:password@github.com/' + data[0] + '/' + data[1] + ' ' + path + data[0] + '/' + data[1])
            print('// Created folder for', data[0], '/', data[1])
            branch = cmdline('(cd ' + path + data[0] + '/' + data[1] + '; git rev-parse --abbrev-ref HEAD)').decode('utf8').rstrip()
            os.system('curl -L -o ' + path + data[0] + '/' + data[1] + '.zip https://user:password@github.com/' + data[0] + '/' + data[1] + '/zipball/' + branch + '/')
            print('// Created zip for', data[0], '/', data[1])
            print('Done for project', nonmaster)
            print('_____________________________________')
print('Redownloaded correct branches for non-master projects'
print('Done.')

