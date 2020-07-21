'''
Created on Jan 19, 2018

@author: xh
'''

import math

class Paradigm():
    '''
    '''


    def __init__(self, word_procs):
        '''
        '''
        self.__word_procs = word_procs
        self.__create_pat_pdgm()
        self.__get_reliable_paradigms()
        self.__prune_paradigms()
    
    def __create_pat_pdgm(self):
        root_pats = {}
        for word, proc_cands in self.__word_procs:
            for root, proc in proc_cands:
                if root in root_pats:
                    root_pats[root].append((word, proc))
                else:
                    root_pats[root] = [(word, proc)]
        paradigms = {}
        for root, word_proc_list in root_pats.items():
            sorted_word_proc_list = sorted(word_proc_list, key=lambda x: x[1].pat())
            pat_tup = tuple([proc.pat() for word, proc in sorted_word_proc_list])
            word_tup = tuple([word for word, proc in sorted_word_proc_list])
            #pat_tup = tuple(sorted([proc.pat() for word, proc in word_proc_list]))
            #word_set = set(word for word, proc in word_proc_list)
            if pat_tup in paradigms:
                paradigms[pat_tup].append((root, word_tup))
            else:
                paradigms[pat_tup] = [(root, word_tup)]
        self.__paradigms = paradigms
    
    def __get_reliable_paradigms(self):
        reliable_paradigms = {}
        singleton_paradigms = {}
        unreliable_paradigms = {}
        for pat_tup, root_word_tup_list in self.__paradigms.items():
            if len(root_word_tup_list) < 2:
                unreliable_paradigms[pat_tup] = root_word_tup_list
                continue
            if len(pat_tup) < 2:
                singleton_paradigms[pat_tup] = root_word_tup_list
                continue
            reliable_paradigms[pat_tup] = root_word_tup_list
        self.__reliable_paradigms = reliable_paradigms
        self.__singleton_paradigms = singleton_paradigms
        self.__unreliable_paradigms = unreliable_paradigms
        self.__reliable_word_procs = self.__filter_word_procs(self.__reliable_paradigms, self.__word_procs)
    
    def __filter_word_procs(self, gold_paradigms, word_procs):
        kept_root_word_tup = set()
        for root_word_tup_list in gold_paradigms.values():
            for root, word_set in root_word_tup_list:
                for word in word_set:
                    kept_root_word_tup.add((root, word))
        filtered_word_procs = []
        for word, proc_cands in word_procs:
            filtered_proc_cands = []
            for root, proc in proc_cands:
                if (root, word) in kept_root_word_tup:
                    filtered_proc_cands.append((root, proc))
#                 elif root == word:
#                     filtered_proc_cands.append((root, proc))
            filtered_word_procs.append((word, filtered_proc_cands))
        return filtered_word_procs
    
    def __get_reliable_pat_scores(self):
        pat_scores = {}
        for rel_pat_tup, rel_root_word_tup_list in self.__reliable_paradigms.items():
            for pat in rel_pat_tup:
                pat_count = len(rel_root_word_tup_list)
                if pat in pat_scores:
                    pat_scores[pat] += pat_count
                else:
                    pat_scores[pat] = pat_count
        self.__reliable_pat_scores = pat_scores
    
    def __score_pat_tuple(self, pat_tup):
        score = 0.0
        for pat in pat_tup:
            if pat in self.__reliable_pat_scores:
                score += self.__reliable_pat_scores[pat]
        return score
    
    def __get_reliable_pat_sets(self):
        # Mining maximal pat set could be added here
        rel_pat_set_list = []
        for rel_pat_tup in self.__reliable_paradigms:
            pat_set = set(rel_pat_tup)
            rel_pat_set_list.append(pat_set)
        self.__rel_pat_sets = rel_pat_set_list
    
    def __get_intersection(self, pat_set, pat_tup):
        intersect_tup = []
        for pat in pat_tup:
            if pat in pat_set:
                intersect_tup.append(pat)
        return tuple(intersect_tup)
    
    def __get_best_intersection_pat_tup(self, pat_tup):
        pruned_pat_tup = tuple()
        best_score = 0.0
        for rel_pat_set in self.__rel_pat_sets:
            intersect_tup = self.__get_intersection(rel_pat_set, pat_tup)
            score = self.__score_pat_tuple(intersect_tup)
            if score > best_score:
                pruned_pat_tup = intersect_tup
                best_score = score
        return pruned_pat_tup
    
    def __combine_paradigms(self, pdgm_0, pdgm_1):
        pdgm_combined = pdgm_0.copy()
        for pat_tup, root_word_tup_list in pdgm_1.items():
            if pat_tup in pdgm_combined:
                pdgm_combined[pat_tup].extend(root_word_tup_list)
            else:
                pdgm_combined[pat_tup] = root_word_tup_list
        return pdgm_combined
    
    def __prune_paradigms(self):
        self.__get_reliable_pat_sets()
        self.__get_reliable_pat_scores()
        pruned_paradigms = {}
        for pat_tup, root_word_tup_list in self.__unreliable_paradigms.items():
            pruned_pat_tup = self.__get_best_intersection_pat_tup(pat_tup)
            if pruned_pat_tup in pruned_paradigms:
                pruned_paradigms[pruned_pat_tup].extend(root_word_tup_list)
            else:
                pruned_paradigms[pruned_pat_tup] = root_word_tup_list
        self.__pruned_paradigms = pruned_paradigms
        pruned_singleton_paradigms = {}
        for pat_tup, root_word_tup_list in self.__singleton_paradigms.items():
            pat = pat_tup[0]
            if pat in self.__reliable_pat_scores:
                pruned_singleton_paradigms[pat_tup] = root_word_tup_list
        self.__pruned_singleton_paradigms = {}
        combined_paradigms = self.__combine_paradigms(self.__reliable_paradigms, self.__pruned_paradigms)
        combined_paradigms = self.__combine_paradigms(combined_paradigms, pruned_singleton_paradigms)
        self.__final_paradigms = combined_paradigms
        self.__final_word_procs = self.__filter_word_procs(self.__final_paradigms, self.__word_procs)
    
    def __save_paradigms(self, paradigms, outfile):
        fout = open(outfile, 'w', -1, 'utf-8')
        sorted_paradigms = sorted(paradigms, key=lambda x: -len(x[1]))
        for pat_tup, root_word_tup_list in sorted_paradigms:
            roots = [root for root, _word_tups in root_word_tup_list]
            fout.write('------pdgm=(%s)\n' % (', '.join(pat_tup)))
            #fout.write('------pdgm=(%s)\n' % (str(pat_tup)))
            for i in range(math.ceil(len(roots) / 10)):
                fout.write('  %s\n' % (' '.join(roots[10*i:10*(i+1)])))
        fout.close()
    
    def print_statistics(self):
        print('----------------Paradigm Statistics-------------------------')
        print('Original word procs: %s' % (len(self.__word_procs)))
        print('Original paradigms: %s' % (len(self.__paradigms)))
        print('Reliable paradigms: %s' % (len(self.__reliable_paradigms)))
        print('Singleton paradigms: %s' % (len(self.__singleton_paradigms)))
        print('Unreliable paradigms: %s' % (len(self.__unreliable_paradigms)))
        print('(After) Pruned paradigms: %s' % (len(self.__pruned_paradigms)))
        print('(After) Pruned singleton paradigms: %s' % (len(self.__pruned_singleton_paradigms)))
        print('Final paradigms: %s' % (len(self.__final_paradigms)))
        print('Final word procs: %s' % (len(self.__final_word_procs)))
    
    def save_reliable_paradigms(self, outfile):
        self.__save_paradigms(self.__reliable_paradigms.items(), outfile)
    
    def save_final_paradigms(self, outfile):
        self.__save_paradigms(self.__final_paradigms.items(), outfile)
    
    def save_raw_paradigms(self, outfile):
        self.__save_paradigms(self.__paradigms.items(), outfile)
    
    def reliable_paradigms(self):
        return self.__reliable_paradigms
    
    def reliable_word_procs(self):
        return self.__reliable_word_procs
    
    def final_word_procs(self):
        return self.__final_word_procs
    


    
    
    
        
    




















