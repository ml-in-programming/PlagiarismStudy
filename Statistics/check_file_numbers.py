set_of_files_extended = set()
set_of_files_extended_v2 = set()
set_of_files_extended_v3 = set()
set_of_blocks_extended = set()
all_files = set()
set_of_blocks = set()
with open('../SourcererCC/results.pairs','r') as fin:
    for line in fin:
        x = line.split(',')
        if int(x[0]) != int(x[2]):
            set_of_blocks.add(int(x[1]))
            set_of_blocks.add(int(x[3]))
print('End of part 1')
with open('../SourcererCC/results.pairs','r') as fin:
    for line in fin:
        x = line.split(',')
        if (int(x[1]) in set_of_blocks) or (int(x[3]) in set_of_blocks):
            set_of_blocks_extended.add(int(x[1]))
            set_of_blocks_extended.add(int(x[3]))
            set_of_files_extended.add(int(x[1]) % 10000000)
            set_of_files_extended.add(int(x[3]) % 10000000)
            set_of_files_extended_v2.add(int(x[1][5:]))
            set_of_files_extended_v2.add(int(x[3][5:]))
print('End of part 2')
with open('../SourcererCC/tokenizers/block-level/file_block_stats/files-stats-all.stats','r') as fin:
    for line in fin:
        x = line.split(',')
        if (x[0][0] == 'f'):
            all_files.add(int(x[2]))
            current_file = int(x[2])
        if (x[0][0] == 'b'):
            if int(x[2]) in set_of_blocks_extended:
                set_of_files_extended_v3.add(current_file)

print('End of part 3')
print('Files to license (1st version):',len(set_of_files_extended))
print('Files to license (2nd version):',len(set_of_files_extended_v2))
print('Files to license (real):',len(set_of_files_extended_v3))
print('All files:',len(all_files))
print('Blocks to blame:',len(set_of_blocks_extended))

