'''
Created on Apr 12, 2018

@author: xh
'''

import argparse
from dataio import read_item_freq_list, read_item_list
from morphanalyzer import MorphAnalyzer
from parameters import Parameter
from typology import MorphTypology, get_gold_features
from languages import LanguageCatalog


def save_segmentations(word_segs, outfile):
    fout = open(outfile, 'w', -1, 'utf-8')
    for word, (seg, components) in word_segs:
#         seg_str = ' '.join(seg)
#         component_str = ' '.join([' '.join(component) for component in components])
        seg_str = ' '.join(seg)
        component_str = ' '.join([' '.join(component) for component in components])
        fout.write('%s\t%s\t%s\n' % (word, seg_str, component_str))
    fout.close()

def save_segmentations_1(word_segs, outfile):
    fout = open(outfile, 'w', -1, 'utf-8')
    for word, (seg, components) in word_segs:
#         seg_str = ' '.join(seg)
#         component_str = ' '.join([' '.join(component) for component in components])
        seg_str = ', '.join(seg)
        component_str = ' '.join(['(' + ', '.join(component) + ')' for component in components])
        fout.write('%s\t[%s]\t%s\n' % (word, seg_str, component_str))
    fout.close()

def seg_file(infile, params, outfile = None, infile_test = None, outfile_test = None, add_test_to_train = True, morph_typology=None, outfile_der=None, outfile_pdgm = None):
    print('| Reading data...')
    word_freq_list = read_item_freq_list(infile)
    print('Read word count: %s' % (len(word_freq_list)))
    word_list_good = [(word, freq) for word, freq in word_freq_list if freq >= params.min_word_freq]
    if infile_test != None:
        test_list = read_item_list(infile_test)
        print('Test words: %s' % (len(test_list)))
        if add_test_to_train:
            print('| Add test words to training list...')
            word_dict = dict(word_list_good)
            for word in test_list:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
            word_list_good = sorted(word_dict.items(), key=lambda x: -x[1])
    print('No. of words for training: %s' % (len(word_list_good)))
    print('| Analyzing...')
    if not morph_typology:
        morph_typology = MorphTypology()
    lang = LanguageCatalog.Other
    morph_analyzer = MorphAnalyzer(lang, dict(word_list_good), morph_typology, params)
    if outfile != None:
        print('| Segmenting...')
        word_list = [word for word, _freq in word_freq_list]
        word_segs = morph_analyzer.segment_word_list(word_list)
        print('| Saving result...')
        save_segmentations(zip(word_list, word_segs), outfile)
    if infile_test != None and outfile_test != None:
        print('| Segmenting test data...')
        test_segs = morph_analyzer.segment_word_list(test_list)
        print('| Saving test result...')
        save_segmentations(zip(test_list, test_segs), outfile_test)
    if outfile_der:
        morph_analyzer.save_der_chain_groups(outfile_der)
    if outfile_pdgm:
        morph_analyzer.save_final_paradigms(outfile_pdgm)
    print('| Done!')


## ----------------- Simply run the segmentor with default parameters ------------------
# def run():
#     infile_train = r''
#     infile_test = r''
#     outfile_test = r''
#     params = Parameter()
#     morph_typology = MorphTypology()
#     seg_file(infile, params, infile_test=infile_test, outfile_test=outfile_test, add_test_to_train=True, morph_typology=morph_typology)
## -------------------------------------------------------------------------------------
# def run2():
#     infile = r''
#     outfile = r''
#     params = Parameter()
#     morph_typology = MorphTypology()
#     seg_file(infile, params, outfile=outfile, morph_typology=morph_typology)
## -------------------------------------------------------------------------------------


if __name__ == '__main__':
    params = Parameter()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('infile', help='The file containing a training word list with line format: <word> <freq>')
    arg_parser.add_argument('-o', '--output', help='File to save the training segmentation result', type=str, default=None)
    arg_parser.add_argument('-ti', '--testin', help='File containing a test word list with format: <word>', type=str, default=None)
    arg_parser.add_argument('-to', '--testout', help='File to save the test result', type=str, default=None)
    arg_parser.add_argument('-np', '--noprune', help='Turn off paradigm pruning', default=False, action='store_true')
    arg_parser.add_argument('-H', '--hyphen', help='Whether explicitly deal with hyphen words', default=False, action='store_true')
    arg_parser.add_argument('-a', '--apos', help='Whether explicitly deal with apostrophes', default=False, action='store_true')
    arg_parser.add_argument('-c', '--case', help='Whether case sensitive', default=False, action='store_true')
    arg_parser.add_argument('-l', '--len', help='Minimal length of roots that will be possibly segmented (default:%s)' % params.min_stem_len, type=int, default=params.min_stem_len)
    arg_parser.add_argument('-y', '--partcpy', help='Minimal length of partial copy (default:%s)' % params.min_partialcopy_len, type=int, default=params.min_partialcopy_len)
    arg_parser.add_argument('-ss', '--minsuf', help='Maximal length of suffixes (default:%s)' % params.min_suf_len, type=int, default=params.min_suf_len)
    arg_parser.add_argument('-sl', '--maxsuf', help='Maximal length of suffixes (default:%s)' % params.max_suf_len, type=int, default=params.max_suf_len)
    arg_parser.add_argument('-ps', '--minpref', help='Minimal length of prefixes (default:%s)' % params.min_pref_len, type=int, default=params.min_pref_len)
    arg_parser.add_argument('-pl', '--maxpref', help='Maximal length of prefixes (default:%s)' % params.max_pref_len, type=int, default=params.max_pref_len)
    arg_parser.add_argument('-is', '--mininf', help='Minimal length of infixes (default:%s)' % params.min_inf_len, type=int, default=params.min_inf_len)
    arg_parser.add_argument('-il', '--maxinf', help='Maximal length of infixes (default:%s)' % params.max_inf_len, type=int, default=params.max_inf_len)
    arg_parser.add_argument('-f', '--freq', help='Minimal word frequency (default:%s)' % params.min_word_freq, type=int, default=params.min_word_freq)
    arg_parser.add_argument('-b', '--te2tr', help='Add test data to training', default=False, action='store_true')
    
    args = arg_parser.parse_args()
    params.do_pruning = not args.noprune
    params.do_hyphen = args.hyphen
    params.do_apostrophe = args.apos
    params.case_sensitive = args.case
    params.min_stem_len = args.len
    params.min_partialcopy_len = args.partcpy
    params.max_suf_len = args.maxsuf
    params.min_suf_len = args.minsuf
    params.max_pref_len = args.maxpref
    params.min_pref_len = args.minpref
    params.max_inf_len = args.maxinf
    params.min_inf_len = args.mininf
    params.min_word_freq = args.freq
    params.print_all()
    
    ## ---------- Use the default typological features. You can change typological features here ------------------
    morph_typology = MorphTypology()
    ## For a language in the catalog, you can get the gold typological features:
    #morph_typology = get_gold_features(LanguageCatalog.Akan)
    ## ------------------------------------------------------------------------------------------------------------
    
    infile = args.infile
    outfile = args.output
    infile_test = args.testin
    outfile_test = args.testout
    test_to_train = args.te2tr
    seg_file(infile, params, outfile=outfile, infile_test=infile_test, outfile_test=outfile_test, add_test_to_train=test_to_train, morph_typology=morph_typology)


















