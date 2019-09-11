import csv

csv.field_size_limit(100000000)
count = 0
with open('java_projects_data.txt','w') as fout:
    with open('pga.csv', newline='') as fin:
        reader = csv.reader(fin)
        for row in reader:
            langs = row[3].split(',')
            if 'Java' in langs:
                count = count + 1
                url = row[0].split('/')
                author = url[-2]
                name = url[-1]
                if ':' not in row[13]:
                    row[13] = 'NONE'
                lic = row[13]
                fout.write(author + ';' + name + ';' + lic + '\n')
                
print('Created java_projects_data.txt for',count,'Java projects')
