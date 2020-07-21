'''
Created on Feb 2, 2018

@author: xh
'''


class EM():
    '''
    '''
    
    def __init__(self):
        '''
        '''
    
    def __set_prior_uniform(self, word_cand_feats):
        word_cand_feats_pri = []
        for word, cand_feats in word_cand_feats:
            if len(cand_feats) == 0:
                word_cand_feats_pri.append((word, cand_feats))
                continue
            avg_prob = 1.0 / len(cand_feats)
            cand_feat_prior = [(avg_prob, cand_feat) for cand_feat in cand_feats]
            word_cand_feats_pri.append((word, cand_feat_prior))
        return word_cand_feats_pri
    
    def __e_step(self, word_cand_feats, prob_roots, prob_pats, prob_trans_on_feat):
        '''
        Calculate expectation of p(root, pat, trans|w)
        '''
        word_cand_feats_probs_1 = []
        #
        for word, cand_feats in word_cand_feats:
            if len(cand_feats) == 0:
                word_cand_feats_probs_1.append((word, cand_feats))
                continue
            probs_1 = []
            for root, pat, trans, feat in cand_feats:
                prob_r = prob_roots[root]
                prob_p = prob_pats[pat]
                prob_1 = prob_r * prob_p
                for t in trans:
                    prob_1 *= prob_trans_on_feat[(t, feat)]
                probs_1.append(prob_1)
            prob_sum_1 = sum(probs_1)
            probs_1 = [prob_1 / prob_sum_1 for prob_1 in probs_1]
            cand_feats_probs_1 = sorted(list(zip(probs_1, cand_feats)), key=lambda x: -x[0])
            word_cand_feats_probs_1.append((word, cand_feats_probs_1))
        return word_cand_feats_probs_1
    
    def __m_step(self, word_cand_feats_probs):
        '''
        Estimate \theta_i+1: p(r), p(pat), p(trans|f(r, pat))
        '''
        n_roots = {}
        n_pats = {}
        n_feats = {}
        n_trans = {}
        #
        for _word, root_cand_feat_probs in word_cand_feats_probs:
            if len(root_cand_feat_probs) == 0:
                continue
            for prob_1, (root, pat, trans, feat) in root_cand_feat_probs:
                if root in n_roots: n_roots[root] += prob_1
                else: n_roots[root] = prob_1
                #
                if pat in n_pats: n_pats[pat] += prob_1
                else: n_pats[pat] = prob_1
                #
                for t in trans:
                    if (t, feat) in n_trans: n_trans[(t, feat)] += prob_1
                    else: n_trans[(t, feat)] = prob_1
                #
                if feat in n_feats: n_feats[feat] += prob_1
                else: n_feats[feat] = prob_1
        #
        sum_w_freq_roots = sum(n_roots.values())
        prob_roots = dict((root, w_freq/sum_w_freq_roots) for root, w_freq in n_roots.items())
        #
        sum_w_freq_pats = sum(n_pats.values())
        prob_pats = dict((pat, w_freq/sum_w_freq_pats) for pat, w_freq in n_pats.items())
        #
        prob_trans_on_feat = dict(((trans, feat), w_freq/n_feats[feat]) for (trans, feat), w_freq in n_trans.items())
        return prob_roots, prob_pats, prob_trans_on_feat
    
    def __e_m_step(self, word_cand_feats_probs, prob_roots, prob_pats, prob_trans_on_feat):
        '''
        E&M at the same time, output f_i, theta_i+1
        '''
        n_roots = {}
        n_pats = {}
        n_feats = {}
        n_trans = {}
        word_root_procs_1 = []
        #
        for word, cand_feats_probs in word_cand_feats_probs:
            if len(cand_feats_probs) == 0:
                word_root_procs_1.append((word, cand_feats_probs))
                continue
            probs_1 = []
            for _prob_old, (root, pat, trans, feat) in cand_feats_probs:
                prob_r = prob_roots[root]
                prob_p = prob_pats[pat]
                prob_1 = prob_r * prob_p
                for t in trans:
                    prob_1 *= prob_trans_on_feat[(t, feat)]
                probs_1.append(prob_1)
            prob_sum_1 = sum(probs_1)
            probs_1 = [prob_1 / prob_sum_1 for prob_1 in probs_1]
            cand_feats_probs_1 = sorted([(prob_1, x[1]) for prob_1, x in zip(probs_1, cand_feats_probs)], key=lambda x: -x[0])
            word_root_procs_1.append((word, cand_feats_probs_1))
            for prob_1, (root, pat, trans, feat) in cand_feats_probs_1:
                if root in n_roots: n_roots[root] += prob_1
                else: n_roots[root] = prob_1
                #
                if pat in n_pats: n_pats[pat] += prob_1
                else: n_pats[pat] = prob_1
                #
                for t in trans:
                    if (t, feat) in n_trans: n_trans[(t, feat)] += prob_1
                    else: n_trans[(t, feat)] = prob_1
                #
                if feat in n_feats: n_feats[feat] += prob_1
                else: n_feats[feat] = prob_1
        #
        sum_w_freq_roots = sum(n_roots.values())
        prob_roots_1 = dict((root, w_freq/sum_w_freq_roots) for root, w_freq in n_roots.items())
        #
        sum_w_freq_pats = sum(n_pats.values())
        prob_pats_1 = dict((pat, w_freq/sum_w_freq_pats) for pat, w_freq in n_pats.items())
        #
        prob_trans_on_feat_1 = dict(((trans, feat), w_freq/n_feats[feat]) for (trans, feat), w_freq in n_trans.items())
        return word_root_procs_1, prob_roots_1, prob_pats_1, prob_trans_on_feat_1
        
    def estimate(self, word_cand_feats, max_iter=1):
        '''
        '''
        word_cand_feats_probs = self.__set_prior_uniform(word_cand_feats)
        prob_roots, prob_pats, prob_trans_on_feat = self.__m_step(word_cand_feats_probs)
        for _ in range(max_iter):
            word_cand_feats_probs = self.__e_step(word_cand_feats, prob_roots, prob_pats, prob_trans_on_feat)
            prob_roots, prob_pats, prob_trans_on_feat = self.__m_step(word_cand_feats_probs)
        return prob_roots, prob_pats, prob_trans_on_feat
    
        
        
    
    





