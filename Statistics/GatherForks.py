import time
from datetime import datetime, timedelta
from os import system

def currentTime():
    return str(timedelta(seconds = time.time() - start_time)).split('.')[0]

from urllib.request import urlopen
import requests
from math import ceil
import json

projects = []
username = 'abc'
password = 'def'

print(currentTime(), 'STARTED OPERATING — GATHERING DATA')

with open('project-list.txt', 'r') as fin:
    for line in fin:
        projects.append([line[1:].split('/')[3], line[1:].rstrip().split('/')[4][:-4]])

count = 0

with open('ForksData.txt', 'w+') as fout:
    for i in projects:

        count = count + 1

        user = i[0]
        repo = i[1]
        fout.write(user + '/' + repo + ';')

        github_url='https://api.github.com/repos/%s/%s'
        resp = requests.get(github_url % (user, repo), auth = (username, password))
        content = resp.json()
        data = content
        if 'forks' in data.keys():
            amount = data['forks']
            fout.write(str(amount) + ';')

            pages = ceil(amount/100)

            forks = []

            for j in range(1, pages + 1):
                github_url='https://api.github.com/repos/%s/%s/forks?page=%s&per_page=100'
                resp = requests.get(github_url % (user, repo, j), auth = (username, password))
        content = resp.json()
        data = content
        if 'forks' in data.keys():
            amount = data['forks']
            fout.write(str(amount) + ';')

            pages = ceil(amount/100)

            forks = []

            for j in range(1, pages + 1):
                github_url='https://api.github.com/repos/%s/%s/forks?page=%s&per_page=100'
                resp = requests.get(github_url % (user, repo, j), auth = (username, password))
                content = resp.json()
                data = content
                for k in data:
                    forks.append(k['full_name'])

            fout.write(str(len(forks)) + ';')

            for j in forks:
                fout.write(j + ',')

        fout.write('\n')
        print(currentTime(), 'Comleted for', count, 'projects')
        
print(currentTime(), 'Processing results')

with open('ForksData.txt', 'r') as fin, open('ForksDataProcessed.txt', 'w+') as fout:
    for line in fin:
        fout.write(line.rstrip()[:-1] + '\n')

os.system('rm ForksData.txt')
os.system('mv ForksDataProcessed.txt ForksData.txt')

print(currentTime(), 'DONE')
