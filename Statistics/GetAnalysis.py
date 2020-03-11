strong = 0
weak = 0
legal = 0
origin = 0
unique = 0

with open('PlagiarismBlocksThree.txt','r') as fin, open('PlagiarismBlocksThreeFull.txt','w+') as fout:
    for line in fin:
        data = line.rstrip().split(';')
        diff = int(data[1])
        diff_older = int(data[2])
        bad = int(data[3])
        if (diff != 0) and (diff_older != 0) and (bad != 0) and (diff_older == bad):
            strong = strong + 1
            fout.write(line.rstrip() + ';strong;100\n')
        if (diff != 0) and (diff_older != 0) and (bad != 0) and (diff_older != bad):
            weak = weak + 1
            fout.write(line.rstrip() + ';weak;' + str(100*bad/diff_older)[:6] + '\n')
        if (diff != 0) and (diff_older != 0) and (bad == 0):
            legal = legal + 1
            fout.write(line.rstrip() + ';legal;0\n')
        if (diff != 0) and (diff_older == 0):
            origin = origin + 1
            fout.write(line.rstrip() + ';origin;0\n')
        if (diff == 0):
            unique = unique + 1
            fout.write(line.rstrip() + ';unique;0\n')

print('Strong:', strong)
print('Weak:', weak)
print('Legal:', legal)
print('Origin:', origin)
print('Unique:', unique)
