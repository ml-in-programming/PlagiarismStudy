import time
from datetime import datetime, timedelta
from os import mkdir, path

def currentTime():
    return str(timedelta(seconds = time.time() - start_time)).split('.')[0]

start_time = time.time()

print(currentTime(), 'STARTED OPERATING — GATHERING NEIGHBORS')

if not path.exists('data/neighbors'):
    mkdir('data/neighbors')

count = 0
set_of_blocks_extended = set()
with open('data/resultsRelated.pairs','r') as fin:
    for line in fin:
        count = count + 1
        set_of_blocks_extended.add(int(data[1]))
        set_of_blocks_extended.add(int(data[3]))
        data = line.split(',')
        if not path.exists('data/neighbors/' + data[1] + '.txt'):
            with open('data/neighbors/' + data[1] + '.txt', 'w+') as fout:
                fout.write(x[1] + ';')
        if not path.exists('data/neighbors/' + data[3].rstrip() + '.txt'):
            with open('data/neighbors/' + data[3].rstrip() + '.txt', 'w+') as fout:
                fout.write(data[3].rstrip() + ';')
        with open('data/neighbors/' + data[1] + '.txt', 'a') as fout:
            fout.write(data[3].rstrip() + ',')
        with open('data/neighbors/' + data[3].rstrip() + '.txt', 'a') as fout:
            fout.write(data[1] + ',')
        if count % 10000000 == 0:
            print(currentTime(), 'Processed', number, 'of lines')

print(currentTime(), 'Created temporary files of blocks neighbors')

with open('data/StatisticsNeighbors.txt','w+') as fout:
    for i in set_of_blocks_extended:
        with open('data/neighbors/' + str(i) + '.txt', 'r') as fin:
            fout.write(fin.readline().rstrip()[:-1] + '\n')

print(currentTime(), 'Created a file with blames statistics and deleted temporary files')
print(currentTime(), 'NEIGHBORS GATHERED')
        
