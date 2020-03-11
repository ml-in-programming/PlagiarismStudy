from operator import itemgetter

all = 0
bad = 0
badc = 0
good = 0
goodc = 0
violated = {}
violating = {}

with open('data/PlagiarismCummulativeFull.txt','r') as fin:
    for line in fin:
        data = line.rstrip().split(';')
        all = all + int(data[1])

with open('data/PlagiarismCummulativeFull.txt','r') as fin:
    for line in fin:
        data = line.rstrip().split(';')
        if len(data) == 4:
            if data[3] == 'GOOD':
                good = good + int(data[1])
                goodc = goodc + 1
            if data[3] == 'BAD':
                bad = bad + int(data[1])
                badc = badc + 1
                lic = data[0].split('/')
                if lic[0] not in violated.keys():
                    violated[lic[0]] = int(data[1])
                else:
                    violated[lic[0]] = violated[lic[0]] + int(data[1])
                if lic[1] not in violating.keys():
                    violating[lic[1]] = int(data[1])
                else:
                    violating[lic[1]] = violating[lic[1]] + int(data[1])

violated_sorted = sorted(violated.items(), key = itemgetter(1), reverse=True)

with open('data/StatisticsPlagiarismViolated.txt','w+') as fout:
    for i in violated_sorted:
        fout.write(i[0] + ';' + str(i[1]) + '\n')

violating_sorted = sorted(violating.items(), key = itemgetter(1), reverse=True)

with open('data/StatisticsPlagiarismViolating.txt','w+') as fout:
    for i in violating_sorted:
        fout.write(i[0] + ';' + str(i[1]) + '\n')


print('good',goodc,good/all,'bad',badc,bad/all)