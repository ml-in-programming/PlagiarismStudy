import os

path = '/home/ubuntu/projects/'

os.system('ls -d -1 ' + path + '*/*.zip > project-list.txt')
