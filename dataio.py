'''
Created on Jan 25, 2018

@author: xh
'''


def read_item_freq_list(infile, delimiter='\t'):
    item_freq_list = []
    fin = open(infile, 'r', -1, 'utf-8')
    for line in fin:
        line = line.strip()
        split_line = line.split(delimiter)
        if len(split_line) != 2:
            print('Skip line: %s' % line)
            continue
        item, freq = split_line
        item_freq_list.append((item, int(freq)))
    fin.close()
    return item_freq_list

def read_item_list(infile):
    item_list = []
    fin = open(infile, 'r', -1, 'utf-8')
    for line in fin:
        line = line.strip()
        if len(line) == 0:
            print('Empty line: %s' % line)
            continue
        item_list.append(line)
    fin.close()
    return item_list

def save_item_freq_list(item_freq_list, outfile):
    fout = open(outfile, 'w', -1, 'utf-8')
    for item, freq in item_freq_list:
        fout.write('%s\t%s\n' % (item, freq))
    fout.close()























