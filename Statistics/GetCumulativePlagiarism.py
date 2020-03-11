count = 0

with open('data/Plagiarism.txt','r') as fin:
    for line in fin:
        count = count + int(line.split(';')[1])

print(count)

count2 = 0
with open('data/Plagiarism.txt','r') as fin, open('data/PlagiarismCumulative.txt','w+') as fout:
    for line in fin:
        count2 = count2 + int(line.split(';')[1])
        fout.write(line.rstrip() + ';' + str(100 * count2 / count)[:6] + '\n')
