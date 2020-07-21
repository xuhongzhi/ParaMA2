'''
Created on Jan 30, 2018

@author: xh
'''

from em import EM

class BayesianModel():
    '''
    '''
    
    def __init__(self):
        '''
        '''
        self.__trained = False
    
    def __feat_func(self, root, proc):
        return '$'
    
    def __features(self, root, proc):
        pat = proc.pat()
        trans = [change.key() for change in proc.change()]
        feat = self.__feat_func(root, proc)
        return root, pat, trans, feat
    
    def train(self, word_root_procs):
        '''
        '''
        word_cand_feats = []
        for word, root_procs in word_root_procs:
            cand_feats = [self.__features(root, proc) for root, proc in root_procs]
            word_cand_feats.append((word, cand_feats))
        self.__prob_roots, self.__prob_pats, self.__prob_trans_on_feat = EM().estimate(word_cand_feats)
        self.__trained = True
    
    def calc_cand_probs(self, word, root_procs):
        if not self.__trained:
            return None
        cand_feats = [self.__features(root, proc) for root, proc in root_procs]
        cand_probs = [self.calc_prob(word, root, pat, trans, feat) for root, pat, trans, feat in cand_feats]
        cand_procs_probs = list(zip(cand_probs, root_procs))
        return sorted(cand_procs_probs, key=lambda x: -x[0])
    
    def __argmax(self, iterable, key=lambda x: x):
        max_val = max(iterable, key=key)
        for x in iterable:
            if key(iterable) == max_val:
                return x
    
    def get_best_root_proc(self, word, root_procs):
        if not self.__trained:
            return None
        cand_feats = [self.__features(root, proc) for root, proc in root_procs]
        cand_probs = [self.calc_prob(word, root, pat, trans, feat) for root, pat, trans, feat in cand_feats]
        return self.__argmax(zip(cand_probs, root_procs))[1]
        
    def calc_prob(self, word, root, pat, trans, feat):
        if not self.__trained:
            return 0.0
        if not (root in self.__prob_roots and pat in self.__prob_pats):
            return 0.0
        for t in trans:
            if not (t, feat) in self.__prob_trans_on_feat:
                return 0.0
        prob_r = self.__prob_roots[root]
        prob_p = self.__prob_pats[pat]
        prob = prob_r * prob_p
        for t in trans:
            prob *= self.__prob_trans_on_feat[(t, feat)]
        return  prob
    


    


















