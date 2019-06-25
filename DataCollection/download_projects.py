import os
num_lines = sum(1 for line in open('pga.txt'))
print('// Commencing download of', num_lines, 'projects.')
i = 0
with open('java_projects_data.txt','r') as fin:
    for line in fin:
        i = i + 1
        x = line.split(';')
        os.system('git clone https://user:password@github.com/' + x[0] + '/' + x[1] + ' /home/ubuntu/projects/' + x[0] + '/' + x[1])
        print('// Created folder for', x[0], '/', x[1])
        os.system('curl -L -o /home/ubuntu/projects/' + x[0] + '/' + x[1] + '.zip https://areyde:Orwell19841984@github.com/' + x[0] + '/' + x[1] + '/zipball/master/')
        print('// Created zip for', x[0], '/', x[1])
        name = '/home/ubuntu/projects/' + x[0] + '/' + x[1] + '.txt'
        with open(name, 'w') as fout:
            fout.write(x[2])
        print('// Created text file for', x[0], '/', x[1])
        print('// Completed for project', i, 'out of', num_lines)
        print('___________________________________________')
print('Completed initial download')

with open('java_projects_data.txt','r') as fin:
    with open('list_checks.txt','w') as fout:
        for line in fin:
            x = line.split(';')
            fout.write(x[0] + '/' + x[1] + ';' + str(os.path.isdir('/home/ubuntu/projects/' + x[0] + '/' + x[1])) + ';' + str(os.path.isfile('/home/ubuntu/projects/' + x[0] + '/' + x[1] + '.zip')) + ';' + str(os.path.isfile('/home/ubuntu/projects/' + x[0] + '/' + x[1] + '.txt')) + '\n')

with open('list_checks.txt','r') as fin:
    for line in fin:
        x = line.split(';')
        if x[2] == 'False':
            os.system('rm /home/ubuntu/projects/' + x[0] + '/' + x[1] + '.zip')
            os.system('rm /home/ubuntu/projects/' + x[0] + '/' + x[1] + '.txt')
print('Deleted uncloned projects (deleted or made private)')

from subprocess import PIPE, Popen
def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

with open('java_projects_data','r') as fin:
    with open('list_branches.txt','w') as fout:
        for line in fin:
            x = line.split(';')
            if os.path.isdir(x[0] + '/' + x[1]) == True:
                y = cmdline('(cd /home/ubuntu/projects/' + x[0] + '/' + x[1] + '; git rev-parse --abbrev-ref HEAD)').decode('utf8').rstrip()
                fout.write(x[0] + ';' + x[1] + ';' + y + '\n')
print('Gathered main branch of every remaining project')

nonmaster = 0
with open ('list_branches.txt','r') as fin:
    for line in fin:
        x = line.split(';')
        if x[2].rstrip() != 'master':
            nonmaster = nonmaster + 1
            os.system('rm -r -f /home/ubuntu/projects/' + x[0] + '/' + x[1])
            print('// Deleted folder for', x[0], '/', x[1])
            os.system('rm -f /home/ubuntu/projects/' + x[0] + '/' + x[1] + '.zip')
            print('// Deleted zip for', x[0], '/', x[1])
            os.system('git clone https://user:password@github.com/' + x[0] + '/' + x[1] + ' /home/ubuntu/projects/' + x[0] + '/' + x[1])
            print('// Created folder for', x[0], '/', x[1])
            branch = cmdline('(cd /home/ubuntu/projects/' + x[0] + '/' + x[1] + '; git rev-parse --abbrev-ref HEAD)').decode('utf8').rstrip()
            os.system('curl -L -o /home/ubuntu/projects/' + x[0] + '/' + x[1] + '.zip https://user:password@github.com/' + x[0] + '/' + x[1] + '/zipball/' + branch + '/')
            print('// Created zip for', x[0], '/', x[1])
            print('Done for project',nonmaster)
            print('_____________________________________')
print('Redownloaded correct branches for non-master projects'
print('Done.')

