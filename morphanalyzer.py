'''
Created on May 3, 2018

@author: xh
'''


from bayesian import BayesianModel
from typology import MorphTypology
from morphprocess import Automic
from parameters import Parameter
from paradigm import Paradigm
from derivationchain import DerivationChain
from unifiedcandgen import UniCandGen
from affixcandidate import AffixGenerator
from languages import create_language


class MorphAnalyzer():
    '''
    '''
    
    def __init__(self, lang, lexicon, morph_typology=None, param=None):
        '''
        '''
        #print('Initializing morphology analyzer...')
        self.__case_sensitive = param.case_sensitive
        self.__do_hyphen = param.do_hyphen
        self.__do_apostrophe = param.do_apostrophe
        self.__apostrophe_char = param.apostrophe_char
        lexicon = set(lexicon)
        if not self.__case_sensitive:
            lexicon = self.__process_uppercase_words(lexicon)
        if self.__do_hyphen:
            lexicon = self.__process_hyphen_words(lexicon)
        if self.__do_apostrophe:
            lexicon = self.__process_apostrophe_words(lexicon)
        self.__lexicon = lexicon
        #self.__use_trans = param.use_trans
        self.__do_pruning = param.do_pruning
        self.__morph_typology = morph_typology
        self.__param = param
        self.__morph_priority = None
        self.__lang = lang
        #
        if not self.__morph_typology: 
            self.__morph_typology = MorphTypology()
        if not self.__param:
            self.__param = Parameter()
        #
        #self.__morph_cand_generators = create_morph_cand_generators(morph_typology, lexicon, param)
        self.__sufs = dict(AffixGenerator().gen_N_best_suffixes(lexicon, self.__param.min_stem_len, self.__param.max_suf_len, self.__param.min_suf_len, min_suf_freq=3, best_N=200))
        self.__prefs = dict(AffixGenerator().gen_N_best_prefixes(lexicon, self.__param.min_stem_len, self.__param.max_pref_len, self.__param.min_pref_len, min_pref_freq=3, best_N=200))
        self.__infs = dict(AffixGenerator().gen_N_best_infixes(lexicon, self.__param.min_stem_len, self.__param.max_inf_len, self.__param.min_inf_len, min_inf_freq=3, best_N=50))
        self.__unified_cand_generator = UniCandGen(create_language(lang), self.__morph_typology, self.__param, lexicon, self.__prefs, self.__sufs, self.__infs)
        # Keep the frequencies of each possible stem changes and choose the top N as valid and redo the analyses again
        self.__stem_change_count = {}
        #
        print('| Analyzing...')
        print('_' * 50)
        self.__analyze()
        print('_' * 50)
        print('| Analysis Done!')
    
    
    def __analyze(self):
        print('1. Generating candidates...')
        word_root_proc_cands = [(word, self.__get_typological_candidates(word)) for word in self.__lexicon]
        self.__ambiguiity_degree_dist = self.__get_ambiguity_degree_dist(word_root_proc_cands)
        #word_root_proc_cands_filtered = [(word, self.__fiter_candidates_heu(proc_cands)) for word, proc_cands in word_root_proc_cands]
        word_root_proc_cands_filtered = word_root_proc_cands
        self.__ambiguiity_degree_dist_filtered = self.__get_ambiguity_degree_dist(word_root_proc_cands_filtered)
        self.__word_root_proc_cands = word_root_proc_cands_filtered
        #
        print('2. Training probabilistic model...')
        bayes_model = BayesianModel()
        bayes_model.train(word_root_proc_cands)
        word_root_proc_cand_probs = [(word, bayes_model.calc_cand_probs(word, root_procs)) for word, root_procs in word_root_proc_cands]
        #word_root_proc = [(word, bayes_model.get_best_root_proc(word, root_procs)) for word, root_procs in word_root_proc_cands]
        self.__model = bayes_model
        self.__word_root_proc_cand_probs = dict(word_root_proc_cand_probs)
        #
        word_root_proc_list = [(word, [(root, proc) for _prob, (root, proc) in root_proc_probs][:1]) for word, root_proc_probs in word_root_proc_cand_probs]
        if self.__do_pruning:
            print('3. Pruning...')
            self.__pdgm = Paradigm(word_root_proc_list)
            word_root_proc = [(word, root_procs[0] if len(root_procs) > 0 else (word, Automic())) for word, root_procs in self.__pdgm.final_word_procs()]
        else:
            #word_root_proc_list = [(word, (root_proc_probs[0][1] if len(root_proc_probs) > 0 else (word, Automic()))) for word, root_proc_probs in word_root_proc_cand_probs]
            word_root_proc = [(word, root_procs[0] if len(root_procs) > 0 else (word, Automic())) for word, root_procs in word_root_proc_list]
        print('4. Generating derivational chain and segmentation...')
        self.__der_chain = DerivationChain(word_root_proc)
        self.__final_word_root_proc = word_root_proc
        # Get the stem change counts
        #self.__stem_change_count = self.__count_final_stem_changes(self.__final_word_root_proc)
    
    
    def __undo_uppercase_word_seg(self, word_seg, word_ori):
        seg_0 = word_ori[0] + word_seg[0][1:]
        return tuple([seg_0] + word_seg[1:])
    
    def __process_uppercase_word(self, word):
        if word[0].lower() != word[0] and word[1:].lower() == word[1:]:
            return word.lower()
        return word
        
    def __process_uppercase_words(self, word_set):
        return set([self.__process_uppercase_word(word) for word in word_set])
    
    def __process_hyphen_word(self, word):
        sub_words = []
        for sub_word in word.split('-'):
            sub_word = sub_word.strip()
            if len(sub_word) > 0:
                sub_words.append(sub_word)
        return sub_words
    
    def __process_hyphen_words(self, word_set):
        word_list = []
        for word in word_set:
            word_list.extend(self.__process_hyphen_word(word))
        return set(word_list)
    
    def __process_apostrophe_word(self, word):
        sub_words = []
        indx = word.find(self.__apostrophe_char, 1)
        while indx > 0:
            sub_word = word[:indx]
            if len(sub_word) > 0:
                sub_words.append(sub_word)
            word = word[indx:]
            indx = word.find(self.__apostrophe_char, 1)
        if len(word) > 0:
            sub_words.append(word)
        return sub_words
    
    def __process_apostrophe_words(self, word_set):
        word_list = []
        for word in word_set:
            word_list.append(self.__process_apostrophe_word(word)[0])
        return set(word_list)
    
    def __get_typological_candidates(self, word):
        '''
        Generate candidate patterns according to the typological features:
        '''
        return self.__unified_cand_generator.get_candidate_analyses(word)
    
    
    def __get_ambiguity_degree_dist(self, word_root_proc_cands):
        ambiguity_degree_dist = {}
        for _word, proc_cands in word_root_proc_cands:
            amb_deg = len(proc_cands)
            if amb_deg in ambiguity_degree_dist:
                ambiguity_degree_dist[amb_deg] += 1
            else:
                ambiguity_degree_dist[amb_deg] = 1
        return ambiguity_degree_dist
    
    def __analyze_word_proc(self, word, topN=1):
        if word in self.__word_root_proc_cand_probs:
            return self.__word_root_proc_cand_probs[word]
        root_procs = self.__get_typological_candidates(word)
        root_procs_probs = self.__model.calc_cand_probs(word, root_procs, sort=True)
        if topN <= 0: return root_procs_probs
        return root_procs_probs[:topN]
    
    def __count_prior_stem_changes(self, word_root_proc_cands):
        stem_change_counts = {}
        for _word, root_proc_cands in word_root_proc_cands:
            prob = 1.0 / len(root_proc_cands)
            for _root, proc in root_proc_cands:
                stem_change = proc.change_key()
                if stem_change in stem_change_counts:
                    stem_change_counts[stem_change] += prob
                else:
                    stem_change_counts[stem_change] = prob
        return stem_change_counts
    
    def __count_weighted_stem_changes(self, word_root_proc_cand_probs):
        stem_change_counts = {}
        for _word, root_proc_cand_probs in word_root_proc_cand_probs:
            for prob, (_root, proc) in root_proc_cand_probs:
                stem_change = proc.change_key()
                if stem_change in stem_change_counts:
                    stem_change_counts[stem_change] += prob
                else:
                    stem_change_counts[stem_change] = prob
        return stem_change_counts
    
    def __count_final_stem_changes(self, final_word_root_proc):
        stem_change_counts = {}
        for _word, (_root, proc) in final_word_root_proc:
            stem_change = proc.change_key()
            if stem_change in stem_change_counts:
                stem_change_counts[stem_change] += 1
            else:
                stem_change_counts[stem_change] = 1
        return stem_change_counts
    
    def analyze_word(self, word, topN=1):
        '''
        Return the result in a tuple: word (root, morph-type, pattern, change)
        '''
        if not self.__case_sensitive:
            word = self.__process_uppercase_word(word)
        root_procs = self.__analyze_word_proc(word, topN)
        word_analyses = [(root, proc.morph_type().value, proc.pat(), proc.change().key()) for root, proc in root_procs]
        return word_analyses
    
    def analyze_word_list(self, word_list, topN=1):
        return [self.analyze_word(word, topN) for word in word_list]
    
    
    def segment_word(self, word):
        word_bak = word
        if not self.__case_sensitive:
            word = self.__process_uppercase_word(word)
        word_seg, components = self.__der_chain.get_segmentation(word)
        if word_seg:
            return word_seg, components
        root_proc_cands = self.__get_typological_candidates(word)
        if len(root_proc_cands) == 0:
            return (word,)
        cand_probs = self.__model.calc_cand_probs(word, root_proc_cands)
        root, proc = cand_probs[0][1]
        root_seg, components = self.__der_chain.get_segmentation(root)
#         if not root_seg:
#             root_seg = (root,)
        components_1 = components.copy()
        component = ('__'.join(root_seg), proc.pat(), proc.change_key())
        components_1.append(component)
        if not self.__case_sensitive and word_bak != word:
            return self.__undo_uppercase_word_seg(proc.apply2seg(root_seg), word_bak), components_1
        return proc.apply2seg(root_seg), components_1
    
    def segment_word_list(self, word_list):
        return [self.segment_word(word) for word in word_list]
    
    def __print_ambiguity_degree_info(self, ambiguiity_degree_dist):
        sorted_amb_deg_dist = sorted(ambiguiity_degree_dist.items(), key=lambda x: -x[0])
        for amb_deg, count in sorted_amb_deg_dist:
            print(' Amb-degree %s: %s' % (amb_deg, count))
        avg_amb_deg = sum(amb_deg * count for amb_deg, count in ambiguiity_degree_dist.items()) / sum(ambiguiity_degree_dist.values())
        print(' Avg-degree: %s' % (avg_amb_deg))
        
    def __print_all_ambiguity_degree_info(self):
        print('-------------Ambiguity Degree Distribution (before filtering with heuristics)')
        self.__print_ambiguity_degree_info(self.__ambiguiity_degree_dist)
        print('-------------Ambiguity Degree Distribution (after filtering with heuristics)')
        self.__print_ambiguity_degree_info(self.__ambiguiity_degree_dist_filtered)
    
    def __print_morph_type_distriution_info(self):
        print('-------------Morphological Type Distribution')
        morph_type_dist = {}
        for _word, (_root, proc) in self.__final_word_root_proc:
            morph_type = proc.morph_type()
            if morph_type in morph_type_dist:
                morph_type_dist[morph_type] += 1
            else:
                morph_type_dist[morph_type] = 1
        for morph_type, count in sorted(morph_type_dist.items(), key=lambda x: -x[1]):
            print(' Morph Type [%s]: %s' % (morph_type.value, count))
    
    def __print_raw_normalized_morph_type_distriution(self):
        print('-------------Normalized Morphological Type Distribution')
        morph_type_dist = {}
        for _word, root_procs in self.__word_root_proc_cands:
            if len(root_procs) == 0:
                continue
            weight = 1.0 / len(root_procs)
            for (_root, proc) in root_procs:
                morph_type = proc.morph_type()
                if morph_type in morph_type_dist:
                    morph_type_dist[morph_type] += weight
                else:
                    morph_type_dist[morph_type] = weight
        for morph_type, count in sorted(morph_type_dist.items(), key=lambda x: -x[1]):
            print(' Morph Type [%s]: %s' % (morph_type.value, count/len(self.__word_root_proc_cands)))
            
    def print_info(self):
        print('----------------------Morphological Analysis Statistical Information--------------------')
        self.__print_all_ambiguity_degree_info()
        self.__print_morph_type_distriution_info()
        self.__print_raw_normalized_morph_type_distriution()
        if self.__do_pruning:
            self.__pdgm.print_statistics()
        self.__der_chain.print_statistics()
    
      
    def save_model(self, outfile):
        pass
    
    def save_final_paradigms(self, outfile):
        self.__pdgm.save_final_paradigms(outfile)
    
    def save_der_chain_groups(self, outfile):
        self.__der_chain.save_chain_groups(outfile)
    
    def save_stem_change_counts(self, outfile):
        stem_change_counts = self.__count_final_stem_changes(self.__final_word_root_proc)
        fout = open(outfile, 'w', -1, 'utf-8')
        for stem_change, count in sorted(stem_change_counts.items(), key=lambda x: -x[1]):
            fout.write('%s\t%s\n' % (stem_change, count))
        fout.close()
    











    
