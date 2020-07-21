'''
Created on Jun 15, 2018

@author: xh
'''

import math

class AffixGenerator():
    '''
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def filter_afx_by_freq(self, afx_dict, min_afx_freq):
        filtered_suf_dict = {}
        for suf, stem_len_dist in afx_dict.items():
            count = sum(stem_len_dist.values())
            if count >= min_afx_freq:
                filtered_suf_dict[suf] = stem_len_dist
        return filtered_suf_dict
    
    def group_afx_by_length(self, affix_stem_len_dist):
        min_root_len = 100
        max_root_len = 0
        groups = {}
        for afx, stem_len_dist in affix_stem_len_dist.items():
            afx_len = len(afx)
            if afx_len in groups:
                groups[afx_len].append((afx, stem_len_dist))
            else:
                groups[afx_len] = [(afx, stem_len_dist)]
            min_root_len, max_root_len = min(min_root_len, min(stem_len_dist)), max(max_root_len, max(stem_len_dist))
        return groups, min_root_len, max_root_len
    
    
    def gen_suf_cand_by_stem_len(self, word_dict, min_stem_len, max_suf_len=6, min_suf_len=1, min_suf_freq = 1):
        suf_dict = {}
        for word in word_dict:
            if len(word) <= min_stem_len: 
                continue
            sIndx = max(min_stem_len, len(word) - max_suf_len)
            for i in range(sIndx, len(word) - min_suf_len + 1):
                stem = word[:i]
                suf = word[i:]
                if stem in word_dict:
                    stem_len = len(stem)
                    if suf in suf_dict:
                        suf_len_dict = suf_dict[suf]
                        if stem_len in suf_len_dict:
                            suf_len_dict[stem_len] += 1
                        else:
                            suf_len_dict[stem_len] = 1
                    else:
                        suf_dict[suf] = {stem_len:1}
        if min_suf_freq <= 1:
            return suf_dict
        return self.filter_afx_by_freq(suf_dict, min_suf_freq)
    
    def gen_pref_cand_by_stem_len(self, word_dict, min_stem_len, max_pref_len=6, min_pref_len=1, min_pref_freq = 1):
        pref_dict = {}
        for word in word_dict:
            if len(word) <= min_stem_len: 
                continue
            eIndx = min(len(word) - min_stem_len, max_pref_len)
            for i in range(min_pref_len, eIndx + 1):
                stem = word[i:]
                pref = word[:i]
                if stem in word_dict:
                    stem_len = len(stem)
                    if pref in pref_dict:
                        pref_len_dict = pref_dict[pref]
                        if stem_len in pref_len_dict:
                            pref_len_dict[stem_len] += 1
                        else:
                            pref_len_dict[stem_len] = 1
                    else:
                        pref_dict[pref] = {stem_len:1}
        if min_pref_freq <= 1:
            return pref_dict
        return self.filter_afx_by_freq(pref_dict, min_pref_freq)
    
    def gen_inf_cand_by_stem_len(self, word_dict, min_stem_len, max_inf_len=5, min_inf_len=2, min_inf_freq = 1):
        inf_dict = {}
        for word in word_dict:
            if len(word) <= min_stem_len: 
                continue
            for i in range(1, len(word) - min_inf_len):
                e_indx = len(word) - max(1, (min_stem_len - i)) 
                for j in range(i + min_inf_len, e_indx + 1):
                    inf = word[i:j]
                    stem = word[:i] + word[j:]
                    if stem in word_dict:
                        stem_len = len(stem)
                        if inf in inf_dict:
                            inf_len_dict = inf_dict[inf]
                            if stem_len in inf_len_dict:
                                inf_len_dict[stem_len] += 1
                            else:
                                inf_len_dict[stem_len] = 1
                        else:
                            inf_dict[inf] = {stem_len:1}
        if min_inf_freq <= 1:
            return inf_dict
        return self.filter_afx_by_freq(inf_dict, min_inf_freq)
    
    
    def calc_expected_stem_len(self, affix_stem_len_dist, min_stem_len, max_stem_len):
        # Smoothing by plus .001
        epi = 0.001
        afx_len_exp = []
        for afx, stem_len_dist in affix_stem_len_dist:
            #count_sum = sum([count + epi for stem_len, count in stem_len_dist])
            #len_sum = sum([stem_len * (epi + count) / count_sum for stem_len, count in stem_len_dist])
            count_sum = 0.0
            len_sum = 0.0
            for stem_len in range(min_stem_len, max_stem_len+1):
                count = epi
                if stem_len in stem_len_dist:
                    count += stem_len_dist[stem_len]
                count_sum += count
                len_sum += stem_len * count
            len_exp = len_sum / count_sum
            afx_score = math.log10(1 + count_sum) * len_exp
            afx_len_exp.append((afx, afx_score, count_sum, len_exp))
        return afx_len_exp
    
    def calc_expected_stem_len_1(self, affix_stem_len_dist):
        afx_len_exp = []
        for afx, stem_len_dist in affix_stem_len_dist.items():
            #count_sum = sum([count + epi for stem_len, count in stem_len_dist])
            #len_sum = sum([stem_len * (epi + count) / count_sum for stem_len, count in stem_len_dist])
            count_sum = 0.0
            len_sum = 0.0
            for stem_len, count in stem_len_dist.items():
                count_sum += count
                len_sum += stem_len * count
            len_exp = len_sum / count_sum
            afx_score = math.log10(1 + count_sum) * (len_exp + len(afx))
            afx_len_exp.append((afx, afx_score))
        return afx_len_exp
    

    def filter_afxes(self, affix_root_len_dist, top_N):
        filtered_affixes = []
        same_len_affix_dist, min_root_len, max_root_len = self.group_afx_by_length(affix_root_len_dist)
        print('Suffix Legth Range: (%s, %s)' % (min(same_len_affix_dist.keys()), max(same_len_affix_dist.keys())))
        for afx_len, afx_stem_len_dist in sorted(same_len_affix_dist.items(), key=lambda x: x[0]):
            print('Processing Suffix Length: %s.' % (afx_len))
            affix_len_exp = self.calc_expected_stem_len(afx_stem_len_dist, min_root_len, max_root_len)
            affix_len_exp = sorted(affix_len_exp, key=lambda x: -x[1])
            top_N_afx = affix_len_exp[:top_N]
            filtered_affixes.extend(top_N_afx)
        filtered_affixes = sorted([(afx, afx_score) for afx, afx_score, _count, _len_exp in filtered_affixes], key = lambda x: -x[1])
        return filtered_affixes
    
    def filter_afxes_1(self, affix_root_len_dist, top_N):
        affix_scores = self.calc_expected_stem_len_1(affix_root_len_dist)
        return sorted(affix_scores, key=lambda x: -x[1])[:top_N]
        
    def gen_N_best_suffixes(self, word_dict, min_stem_len=3, max_suf_len=5, min_suf_len=1, min_suf_freq=10, best_N=500):
        suffix_stem_len_dist = self.gen_suf_cand_by_stem_len(word_dict, min_stem_len, max_suf_len, min_suf_len, min_suf_freq)
        best_suffix_list = self.filter_afxes_1(suffix_stem_len_dist, best_N)
        return best_suffix_list

    def gen_N_best_prefixes(self, word_dict, min_stem_len=3, max_pref_len=5, min_pref_len=1, min_pref_freq=10, best_N=500):
        prefix_stem_len_dist = self.gen_pref_cand_by_stem_len(word_dict, min_stem_len, max_pref_len, min_pref_len, min_pref_freq)
        best_prefix_list = self.filter_afxes_1(prefix_stem_len_dist, best_N)
        return best_prefix_list
    
    def gen_N_best_infixes(self, word_dict, min_stem_len=3, max_inf_len=4, min_inf_len=2, min_inf_freq=10, best_N=500):
        infix_stem_len_dist = self.gen_inf_cand_by_stem_len(word_dict, min_stem_len, max_inf_len, min_inf_len, min_inf_freq)
        best_infix_list = self.filter_afxes_1(infix_stem_len_dist, best_N)
        return best_infix_list

    
    def __save_item_scores(self, item_scores, outfile):
        fout = open(outfile, 'w', -1, 'utf-8')
        for item, score in item_scores:
            fout.write('%s\t%s\n' % (item, score))
        fout.close()
    
    def save_affix_lists(self, word_dict):
        min_stem_len=3
        max_pref_len=5
        min_pref_len=1
        min_pref_freq=3
        best_N=500
        prefix_stem_len_dist = self.gen_pref_cand_by_stem_len(word_dict, min_stem_len, max_pref_len, min_pref_len, min_pref_freq)
        pref_freq_list = sorted([(pref, sum(stem_len_dist.values())) for pref, stem_len_dist in prefix_stem_len_dist.items()], key=lambda x: -x[1])
        best_prefix_list = self.filter_afxes_1(prefix_stem_len_dist, best_N)
        outfile_pref_freq = r'E:\LORELEI\mitch\pref_freq.txt'
        outfile_pref_conf = r'E:\LORELEI\mitch\pref_conf.txt'
        self.__save_item_scores(pref_freq_list, outfile_pref_freq)
        self.__save_item_scores(best_prefix_list, outfile_pref_conf)
        min_stem_len=3
        max_inf_len=4
        min_inf_len=2
        min_inf_freq=3
        best_N=500
        infix_stem_len_dist = self.gen_inf_cand_by_stem_len(word_dict, min_stem_len, max_inf_len, min_inf_len, min_inf_freq)
        inf_freq_list = sorted([(inf, sum(stem_len_dist.values())) for inf, stem_len_dist in infix_stem_len_dist.items()], key=lambda x: -x[1])
        best_infix_list = self.filter_afxes_1(infix_stem_len_dist, best_N)
        outfile_inf_freq = r'E:\LORELEI\mitch\inf_freq.txt'
        outfile_inf_conf = r'E:\LORELEI\mitch\inf_conf.txt'
        self.__save_item_scores(inf_freq_list, outfile_inf_freq)
        self.__save_item_scores(best_infix_list, outfile_inf_conf)
        min_stem_len=3
        max_suf_len=5
        min_suf_len=1
        min_suf_freq=3
        best_N=500
        suffix_stem_len_dist = self.gen_suf_cand_by_stem_len(word_dict, min_stem_len, max_suf_len, min_suf_len, min_suf_freq)
        suf_freq_list = sorted([(suf, sum(stem_len_dist.values())) for suf, stem_len_dist in suffix_stem_len_dist.items()], key=lambda x: -x[1])
        best_suffix_list = self.filter_afxes_1(suffix_stem_len_dist, best_N)
        outfile_suf_freq = r'E:\LORELEI\mitch\suf_freq.txt'
        outfile_suf_conf = r'E:\LORELEI\mitch\suf_conf.txt'
        self.__save_item_scores(suf_freq_list, outfile_suf_freq)
        self.__save_item_scores(best_suffix_list, outfile_suf_conf)
        



















