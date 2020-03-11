from operator import itemgetter

licenses = {}
blocks = {}

with open('data/StatisticsLicensesFiles.txt', 'r') as fin:
    for line in fin:
        data = line.split(';')
        licenses[int(data[0])] = data[2].rstrip()

with open('data/StatisticsNeighbors.txt', 'r') as fin:
    for line in fin:
        cur = licenses[int(line.split(';')[0][5:])]
        if '_' not in cur:
            if cur not in blocks.keys():
                blocks[cur] = 1
            else:
                blocks[cur] = blocks[cur] + 1
        else:
            multi = cur.split('_')
            for i in multi:
                if i not in blocks.keys():
                    blocks[i] = 1
                else:
                    blocks[i] = blocks[i] + 1

blocks_sorted = sorted(blocks.items(), key = itemgetter(1), reverse=True)

with open('data/StatisticsLicensesBlocksList.txt','w+') as fout:
    for i in blocks_sorted:
        fout.write(i[0] + ';' + str(i[1]) + '\n')
