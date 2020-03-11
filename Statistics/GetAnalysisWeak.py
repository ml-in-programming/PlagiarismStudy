below20 = 0
below40 = 0
below60 = 0
below80 = 0
below100 = 0

with open('data/PlagiarismBlocksThreeFull.txt', 'r') as fin:
    for line in fin:
        data = line.rstrip().split(';')
        if data[4] == 'weak':
            weakness = float(data[5])
            if weakness <= 20:
                below20 = below20 + 1
            if (weakness > 20) and (weakness <=40):
                below40 = below40 + 1
            if (weakness > 40) and (weakness <=60):
                below60 = below60 + 1
            if (weakness > 60) and (weakness <=80):
                below80 = below80 + 1
            if (weakness > 80):
                below100 = below100 + 1

print('Below 20:', below20)
print('Below 40:', below40)
print('Below 60:', below60)
print('Below 80:', below80)
print('Below 100:', below100)
