from operator import itemgetter

licenses = {}
amount = {1:0, 2:0, 3:0, 4:0}
several = {}

with open('data/StatisticsLicensesFiles.txt', 'r') as fin:
    for line in fin:
        data = line.split(';')
        if '_' not in data[2]:
            amount[1] = amount[1] + 1
            if data[2].rstrip() not in licenses.keys():
                licenses[data[2].rstrip()] = 1
            else:
                licenses[data[2].rstrip()] = licenses[data[2].rstrip()] + 1
        else:
            if data[2].rstrip() not in several.keys():
                several[data[2].rstrip()] = 1
            else:
                several[data[2].rstrip()] = several[data[2].rstrip()] + 1
            multi = data[2].rstrip().split('_')
            amount[len(multi)] = amount[len(multi)] + 1
            for i in multi:
                if i not in licenses.keys():
                    licenses[i] = 1
                else:
                    licenses[i] = licenses[i] + 1

licenses_sorted = sorted(licenses.items(), key = itemgetter(1), reverse=True)
several_sorted = sorted(several.items(), key = itemgetter(1), reverse=True)

with open('data/StatisticsLicensesList.txt','w+') as fout:
    for i in licenses_sorted:
        fout.write(i[0] + ';' + str(i[1]) + '\n')

with open('data/StatisticsLicensesSeveral.txt','w+') as fout:
    for i in several_sorted:
        fout.write(i[0] + ';' + str(i[1]) + '\n')

with open('data/StatisticsLicensesAmount.txt','w+') as fout:
    for i in range(1,5):
        fout.write(str(i) + ';' + str(amount[i]) + '\n')
