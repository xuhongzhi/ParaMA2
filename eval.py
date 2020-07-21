'''
Created on May 21, 2018

@author: xh
'''

from evalsegpoint import EvalSegPoint


class EvalSeg():
    '''
    '''
    
    def __init__(self):
        '''
        '''
    
    def __read_segmentation(self, infile):
        '''
        Assumed format: <word>\t<seg>
        where <seg> are white space separated morphemes
        '''
        word_seg_list = []
        fin = open(infile, 'r', -1, 'utf-8')
        for line in fin:
            line = line.strip()
            split_line = line.split('\t')
            if len(split_line) < 2:
                print('Error Line: ' + line)
                continue
            word = split_line[0].strip()
            seg = split_line[1].strip().split(' ')
            word_seg_list.append((word, seg))
        fin.close()
        return word_seg_list
    
    def __read_gold_seg(self, infile):
        '''
        Assumed format: <word>\t<segs>
        where <segs> is all possible segmentations (allowing multiple gold segmentations) of <seg> separated by comma, and each <seg> is white space separated morphemes
        '''
        word_seg_list = []
        fin = open(infile, 'r', -1, 'utf-8')
        for line in fin:
            line = line.strip()
            split_line = line.split('\t')
            if len(split_line) != 2:
                print('Error Line: ' + line)
                continue
            word = split_line[0].strip()
            segs = [seg_str.strip().split(' ') for seg_str in split_line[1].strip().split(',')]
            word_seg_list.append((word, segs))
        fin.close()
        return word_seg_list
    
    def evaluate(self, infile_pred, infile_gold):
        seg_pred = self.__read_segmentation(infile_pred)
        seg_gold = self.__read_gold_seg(infile_gold)
        EvalSegPoint().evaluate_seg(seg_gold, seg_pred)
    

if __name__ == '__main__':
    import argparse
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('infile_gold', help='The file containing the gold segmentations')
    arg_parser.add_argument('infile_pred', help='The file containing the segmentation results')
    args = arg_parser.parse_args()
    infile_gold = args.infile_gold
    infile_pred = args.infile_pred
    EvalSeg().evaluate(infile_pred, infile_gold)





















