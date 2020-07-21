'''
Created on Dec 10, 2018

@author: xh
'''
from morphprocess import Reduplication, LeftPartialCopy, RightPartialCopy, Prefixation, Suffixation, Infixation, Compounding
from stemchange import NonChange, DelChange, DegemChange, GemChange, InsChange, SubChange, VowChange, NonChangeInf, GemChangeInf, DegemChangeInf, InsChangeInf, DelChangeInf, SubChangeInf, VowChangeInf
from typology import StemChangePosition, MorphType, StemChangeType


class UniCandGen():
    '''
    Insertion: applies to Reduplication (Full and Partial) only at boundaries
    Deletion: applies to Affixation, Full Reduplication only at boundaries
    Gemination: applies to Affixation, Reduplication for leftmost and rightmost consonants
    Degemination: same as Gemination
    Substitution: applies to Affixation, Reduplication for leftmost and rightmost consonants/vowels or (at boundaries for possible changes from consonant to vowel and vise versa
    '''
    
    def __init__(self, lang, morph_typology, params, lexicon, prefs={}, sufs={}, infs={}):
        #self.__typo_feats = typo_feats
        #---------- Language specific parameters ----------
        self.__lang = lang.name()
        self.__vowels = set(lang.all_vowels())
        self.__consonants = set(lang.all_consonants())
        # --------- Morphological Typology ----------------
        self.__reduplication = morph_typology.has_morph_feature(MorphType.REDUPLICATION)
        self.__left_reduplication = morph_typology.has_morph_feature(MorphType.LPARTIALCOPY)
        self.__right_reduplication = morph_typology.has_morph_feature(MorphType.RPARTIALCOPY)
        self.__prefixation = morph_typology.has_morph_feature(MorphType.PREFIXATION)
        self.__suffixation = morph_typology.has_morph_feature(MorphType.SUFFIXATION)
        self.__infixation = morph_typology.has_morph_feature(MorphType.INFIXATION)
        self.__compounding = morph_typology.has_morph_feature(MorphType.COMPOUNDING)
        self.__final_vowel = morph_typology.has_morph_feature(MorphType.FINALVOWEL)
        self.__templatic = morph_typology.has_morph_feature(MorphType.TEMPLATIC)
        self.__vowel_harmony = morph_typology.has_morph_feature(MorphType.VOWELHARMONY)
        # --------- Stem Change Typology ------------------
        self.__stem_r_ins = morph_typology.is_valid_stem_change_position(StemChangePosition.RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.INS)
        self.__stem_r_del = morph_typology.is_valid_stem_change_position(StemChangePosition.RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEL)
        self.__stem_r_gem = morph_typology.is_valid_stem_change_position(StemChangePosition.RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.GEM)
        self.__stem_r_degem = morph_typology.is_valid_stem_change_position(StemChangePosition.RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEGEM)
        self.__stem_r_sub = morph_typology.is_valid_stem_change_position(StemChangePosition.RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.SUB)
        self.__stem_r_vow = morph_typology.is_valid_stem_change_position(StemChangePosition.RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.VOW)
        self.__stem_l_ins = morph_typology.is_valid_stem_change_position(StemChangePosition.LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.INS)
        self.__stem_l_del = morph_typology.is_valid_stem_change_position(StemChangePosition.LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEL)
        self.__stem_l_gem = morph_typology.is_valid_stem_change_position(StemChangePosition.LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.GEM)
        self.__stem_l_degem = morph_typology.is_valid_stem_change_position(StemChangePosition.LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEGEM)
        self.__stem_l_sub = morph_typology.is_valid_stem_change_position(StemChangePosition.LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.SUB)
        self.__stem_l_vow = morph_typology.is_valid_stem_change_position(StemChangePosition.LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.VOW)
        self.__stem_inf_b_ins = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.INS)
        self.__stem_inf_b_del = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEL)
        self.__stem_inf_b_gem = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.GEM)
        self.__stem_inf_b_degem = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEGEM)
        self.__stem_inf_b_sub = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.SUB)
        self.__stem_inf_b_vow = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL) and morph_typology.has_stem_change_feature(StemChangeType.VOW)
        self.__stem_inf_e_ins = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.INS)
        self.__stem_inf_e_del = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEL)
        self.__stem_inf_e_gem = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.GEM)
        self.__stem_inf_e_degem = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.DEGEM)
        self.__stem_inf_e_sub = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY) and morph_typology.has_stem_change_feature(StemChangeType.SUB)
        self.__stem_inf_e_vow = morph_typology.is_valid_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL) and morph_typology.has_stem_change_feature(StemChangeType.VOW)
        self.__compounding_stem_change = False
        # --------- Search Algorithm Parameters -------------
        #self.__attested_root = True
        self.__min_stem_len = params.min_stem_len
        self.__min_cpy_len = params.min_partialcopy_len
        self.__min_pref_len = params.min_pref_len
        self.__min_suf_len = params.min_suf_len
        self.__min_inf_len = params.min_inf_len
        self.__max_cpy_len = params.max_partialcopy_len
        self.__max_pref_len = params.max_pref_len
        self.__max_suf_len = params.max_suf_len
        self.__max_inf_len = params.max_inf_len
        # ----------- Private Attributes --------------------
        self.__lexicon = lexicon
        self.__prefs = prefs
        self.__sufs = sufs
        self.__infs = infs
        self.__create_index()
        
    
    def __do_reduplication(self):
        return self.__reduplication
    
    def __do_left_reduplication(self):
        return self.__left_reduplication
    
    def __do_right_reduplication(self):
        return self.__right_reduplication
    
    def __do_prefixation(self):
        return self.__prefixation
    
    def __do_suffixation(self):
        return self.__suffixation
    
    def __do_infixation(self):
        return self.__infixation
    
    def __do_compounding(self):
        return self.__compounding
    
    def __do_final_vowel(self):
        return self.__final_vowel
    
    def __do_templatic(self):
        return self.__templatic
    
    def __do_vowel_harmony(self):
        return self.__vowel_harmony
    
    def __do_compounding_stem_change(self):
        return self.__compounding_stem_change
    
    def __do_r_gemination(self):
        return self.__stem_r_gem
    
    def __do_l_gemination(self):
        return self.__stem_l_gem
    
    def __do_r_insertion(self):
        return self.__stem_r_ins
    
    def __do_l_insertion(self):
        return self.__stem_l_ins
    
    def __do_r_degemination(self):
        return self.__stem_r_degem
    
    def __do_l_degemination(self):
        return self.__stem_l_degem
    
    def __do_r_deletion(self):
        return self.__stem_r_del
    
    def __do_l_deletion(self):
        return self.__stem_l_del
    
    def __do_r_substitution(self):
        return self.__stem_r_sub
    
    def __do_l_substitution(self):
        return self.__stem_l_sub
    
    def __do_r_vow_change(self):
        return self.__stem_r_vow
    
    def __do_l_vow_change(self):
        return self.__stem_l_vow
    
    def __do_inf_b_gemination(self):
        return self.__stem_inf_b_gem
    
    def __do_inf_e_gemination(self):
        return self.__stem_inf_e_gem
    
    def __do_inf_b_insertion(self):
        return self.__stem_inf_b_ins
    
    def __do_inf_e_insertion(self):
        return self.__stem_inf_e_ins
    
    def __do_inf_b_degemination(self):
        return self.__stem_inf_b_degem
    
    def __do_inf_e_degemination(self):
        return self.__stem_inf_e_degem
    
    def __do_inf_b_deletion(self):
        return self.__stem_inf_b_del
    
    def __do_inf_e_deletion(self):
        return self.__stem_inf_e_del
    
    def __do_inf_b_substitution(self):
        return self.__stem_inf_b_sub
    
    def __do_inf_e_substitution(self):
        return self.__stem_inf_e_sub
    
    def __do_inf_b_vow_change(self):
        return self.__stem_inf_b_vow
    
    def __do_inf_e_vow_change(self):
        return self.__stem_inf_e_vow
    
    def __is_vowel(self, ch):
        return ch in self.__vowels
    
    def __is_consonant(self, ch):
        return ch in self.__consonants
    
        
    def __indx_vowel_r(self, word):
        for i in range(len(word) - 1, -1, -1):
            if self.__is_vowel(word[i]):
                return i
        return -1
    
    def __indx_vowel_l(self, word):
        for i in range(len(word)):
            if self.__is_vowel(word[i]):
                return i
        return -1
    
    
    def __create_index(self):
        '''
        Create index for Deletion (Substitution), Degemination, Vowel change at non-boundaries (leftmost & rightmost vowels)
        Insertion, Gemination, don't need index
        '''
        if self.__do_l_deletion() or self.__do_l_substitution():
            self.__del_sub_l_indx = self.__create_del_sub_l_indx(self.__lexicon)
            #print('del_sub_l: %s' % str(self.__del_sub_l_indx))
        if self.__do_r_deletion() or self.__do_r_substitution():
            self.__del_sub_r_indx = self.__create_del_sub_r_indx(self.__lexicon)
            #print('del_sub_r: %s' % str(self.__del_sub_r_indx))
        if self.__do_l_vow_change():
            self.__vow_l_indx = self.__create_vow_l_indx(self.__lexicon)
            #print('vow_l: %s' % str(self.__vow_l_indx))
        if self.__do_r_vow_change():
            self.__vow_r_indx = self.__create_vow_r_indx(self.__lexicon)
            #print('vow_r: %s' % str(self.__vow_r_indx))
        if self.__do_inf_b_deletion() or self.__do_inf_b_substitution():
            self.__del_sub_inf_b_indx = self.__create_del_sub_inf_b_indx(self.__lexicon)
            #print('del_sub_inf_b: %s' % str(self.__del_sub_inf_b_indx))
        if self.__do_inf_e_deletion() or self.__do_inf_e_substitution():
            self.__del_sub_inf_e_indx = self.__create_del_sub_inf_e_indx(self.__lexicon)
            #print('del_sub_inf_e: %s' % str(self.__del_sub_inf_e_indx))
        if self.__do_inf_b_vow_change():
            self.__vow_inf_b_indx = self.__create_vow_inf_b_indx(self.__lexicon)
            #print('vow_inf_b: %s' % str(self.__vow_inf_b_indx))
        if self.__do_inf_e_vow_change():
            self.__vow_inf_e_indx = self.__create_vow_inf_e_indx(self.__lexicon)
            #print('vow_inf_e: %s' % str(self.__vow_inf_e_indx))
        
    def __create_del_sub_l_indx(self, lexicon):
        del_sub_l_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len + 1:
                continue
            if len(word) < 2 or word[0] == word[1]:
                continue
            ch = word[0]
            stem = word[1:]
            cand = (word, ch)
            if stem in del_sub_l_indx:
                del_sub_l_indx[stem].append(cand)
            else:
                del_sub_l_indx[stem] = [cand]
        return del_sub_l_indx
    
    def __create_del_sub_r_indx(self, lexicon):
        del_sub_r_indx = {}
        for word in lexicon:
            if len(word) < 2 or word[-1] == word[-2]:
                continue
            if len(word) < self.__min_stem_len + 1:
                continue
            ch = word[-1]
            stem = word[:-1]
            cand = (word, ch)
            if stem in del_sub_r_indx:
                del_sub_r_indx[stem].append(cand)
            else:
                del_sub_r_indx[stem] = [cand]
        return del_sub_r_indx
    
    def __create_vow_l_indx(self, lexicon):
        vow_l_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len or len(word) < 3:
                continue
            indx = self.__indx_vowel_l(word)
            if indx <= 0 or indx >= len(word) - 1:
                continue
            stem_pat = (word[:indx], word[indx + 1:])
            ch = word[indx]
            cand = (word, ch)
            if stem_pat in vow_l_indx:
                vow_l_indx[stem_pat].append(cand)
            else:
                vow_l_indx[stem_pat] = [cand]
        return vow_l_indx
    
    def __create_vow_r_indx(self, lexicon):
        vow_r_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len or len(word) < 3:
                continue
            indx = self.__indx_vowel_r(word)
            if indx <= 0 or indx >= len(word) - 1:
                continue
            stem_pat = (word[:indx], word[indx + 1:])
            ch = word[indx]
            cand = (word, ch)
            if stem_pat in vow_r_indx:
                vow_r_indx[stem_pat].append(cand)
            else:
                vow_r_indx[stem_pat] = [cand]
        return vow_r_indx
    
    def __create_del_sub_inf_b_indx(self, lexicon):
        del_sub_inf_b_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len or len(word) < 3:
                continue
            for i in range(2, len(word)):
                bx = word[:i]
                ex = word[i:]
                ch = bx[-1]
                stem_pat = (bx[:-1], ex)
                cand = (word, ch)
                if stem_pat in del_sub_inf_b_indx:
                    del_sub_inf_b_indx[stem_pat].append(cand)
                else:
                    del_sub_inf_b_indx[stem_pat] = [cand]
        return del_sub_inf_b_indx
    
    def __create_del_sub_inf_e_indx(self, lexicon):
        del_sub_inf_e_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len or len(word) < 3:
                continue
            for i in range(1, len(word)-1):
                bx = word[:i]
                ex = word[i:]
                ch = ex[0]
                stem_pat = (bx, ex[1:])
                cand = (word, ch)
                if stem_pat in del_sub_inf_e_indx:
                    del_sub_inf_e_indx[stem_pat].append(cand)
                else:
                    del_sub_inf_e_indx[stem_pat] = [cand]
        return del_sub_inf_e_indx
    
    def __create_vow_inf_b_indx(self, lexicon):
        vow_inf_b_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len or len(word) < 4:
                continue
            for i in range(3, len(word)):
                bx = word[:i]
                ex = word[i:]
                vow_r_indx = self.__indx_vowel_r(bx)
                if vow_r_indx <= 0 or vow_r_indx >= len(bx) - 1:
                    continue
                stem_pat = ((bx[:vow_r_indx], bx[vow_r_indx + 1:]), ex)
                ch = bx[vow_r_indx]
                cand = (word, ch)
                if stem_pat in vow_inf_b_indx:
                    vow_inf_b_indx[stem_pat].append(cand)
                else:
                    vow_inf_b_indx[stem_pat] = [cand]
        return vow_inf_b_indx
    
    def __create_vow_inf_e_indx(self, lexicon):
        vow_inf_e_indx = {}
        for word in lexicon:
            if len(word) < self.__min_stem_len or len(word) < 4:
                continue
            for i in range(1, len(word)-2):
                bx = word[:i]
                ex = word[i:]
                vow_l_indx = self.__indx_vowel_l(ex)
                if vow_l_indx <= 0 or vow_l_indx >= len(ex) - 1:
                    continue
                stem_pat = (bx, (ex[:vow_l_indx], ex[vow_l_indx + 1:]))
                ch = ex[vow_l_indx]
                cand = (word, ch)
                if stem_pat in vow_inf_e_indx:
                    vow_inf_e_indx[stem_pat].append(cand)
                else:
                    vow_inf_e_indx[stem_pat] = [cand]
        return vow_inf_e_indx
    
    def __get_root_cands_r_del(self, stem):
        cand_roots = []
        if not self.__do_r_deletion() or not stem in self.__del_sub_r_indx or len(stem) < self.__min_stem_len:
            return cand_roots
        for root, ch in self.__del_sub_r_indx[stem]:
            s_change = DelChange(ch, StemChangePosition.RIGHT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cands_l_del(self, stem):
        cand_roots = []
        if not self.__do_l_deletion() or not stem in self.__del_sub_l_indx or len(stem) < self.__min_stem_len:
            return cand_roots
        for root, ch in self.__del_sub_l_indx[stem]:
            s_change = DelChange(ch, StemChangePosition.LEFT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    
    def __get_root_cands_r_sub(self, stem):
        cand_roots = []
        if not self.__do_r_substitution() or len(stem) < self.__min_stem_len:
            return cand_roots
        stem_key = stem[:-1]
        if not stem_key in self.__del_sub_r_indx:
            return cand_roots
        ch1 = stem[-1]
        for root, ch0 in self.__del_sub_r_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = SubChange(ch0, ch1, StemChangePosition.RIGHT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cands_l_sub(self, stem):
        cand_roots = []
        if not self.__do_l_substitution() or len(stem) < self.__min_stem_len:
            return cand_roots
        stem_key = stem[1:]
        if not stem_key in self.__del_sub_l_indx:
            return cand_roots
        ch1 = stem[0]
        for root, ch0 in self.__del_sub_l_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = SubChange(ch0, ch1, StemChangePosition.LEFT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cands_r_vow(self, stem):
        # Vowel change at the boundaries are not considered here
        cand_roots = []
        if not self.__do_r_vow_change() or len(stem) < self.__min_stem_len  or len(stem) < 3:
            return cand_roots
        vow_r_indx = self.__indx_vowel_r(stem)
        if vow_r_indx <= 0 or vow_r_indx >= len(stem) - 1:
            return cand_roots
        stem_key = (stem[:vow_r_indx], stem[vow_r_indx+1:])
        if not stem_key in self.__vow_r_indx:
            return cand_roots
        ch1 = stem[vow_r_indx]
        for root, ch0 in self.__vow_r_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = VowChange(ch0, ch1, StemChangePosition.RIGHT_VOWEL, vow_r_indx)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cands_l_vow(self, stem):
        # Vowel change at the boundaries are not considered here
        cand_roots = []
        if not self.__do_l_vow_change() or len(stem) < self.__min_stem_len  or len(stem) < 3:
            return cand_roots
        vow_l_indx = self.__indx_vowel_l(stem)
        if vow_l_indx <= 0 or vow_l_indx >= len(stem) - 1:
            return cand_roots
        stem_key = (stem[:vow_l_indx], stem[vow_l_indx+1:])
        if not stem_key in self.__vow_l_indx:
            return cand_roots
        ch1 = stem[vow_l_indx]
        for root, ch0 in self.__vow_l_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = VowChange(ch0, ch1, StemChangePosition.LEFT_VOWEL, vow_l_indx)
            cand_roots.append((root, s_change))
        return cand_roots

    def __get_root_cand_inf_b_del(self, b_stem, e_stem):
        cand_roots = []
        if not self.__do_inf_b_deletion() or len(b_stem) + len(e_stem) < self.__min_stem_len:
            return cand_roots
        stem_key = (b_stem, e_stem)
        if not stem_key in self.__del_sub_inf_b_indx:
            return cand_roots
        for root, ch in self.__del_sub_inf_b_indx[stem_key]:
            s_change = DelChangeInf(ch, StemChangePosition.INF_B_RIGHT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cand_inf_e_del(self, b_stem, e_stem):
        cand_roots = []
        if not self.__do_inf_e_deletion() or len(b_stem) + len(e_stem) < self.__min_stem_len:
            return cand_roots
        stem_key = (b_stem, e_stem)
        if not stem_key in self.__del_sub_inf_e_indx:
            return cand_roots
        for root, ch in self.__del_sub_inf_e_indx[stem_key]:
            s_change = DelChangeInf(ch, StemChangePosition.INF_E_LEFT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
        
    def __get_root_cand_inf_b_sub(self, b_stem, e_stem):
        cand_roots = []
        if not self.__do_inf_b_substitution() or len(b_stem) + len(e_stem) < self.__min_stem_len or len(b_stem) < 2:
            return cand_roots
        stem_key = (b_stem[:-1], e_stem)
        if not stem_key in self.__del_sub_inf_b_indx:
            return cand_roots
        ch1 = b_stem[-1]
        for root, ch0 in self.__del_sub_inf_b_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = SubChangeInf(ch0, ch1, StemChangePosition.INF_B_RIGHT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cand_inf_e_sub(self, b_stem, e_stem):
        cand_roots = []
        if not self.__do_inf_e_substitution() or len(b_stem) + len(e_stem) < self.__min_stem_len or len(e_stem) < 2:
            return cand_roots
        stem_key = (b_stem, e_stem[1:])
        if not stem_key in self.__del_sub_inf_e_indx:
            return cand_roots
        ch1 = e_stem[0]
        for root, ch0 in self.__del_sub_inf_e_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = SubChangeInf(ch0, ch1, StemChangePosition.INF_E_LEFT_BOUNDARY)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cand_inf_b_vow(self, b_stem, e_stem):
        cand_roots = []
        if not self.__do_inf_b_vow_change() or len(b_stem) + len(e_stem) < self.__min_stem_len or len(b_stem) < 3:
            return cand_roots
        vow_r_indx = self.__indx_vowel_r(b_stem)
        if vow_r_indx <= 0 or vow_r_indx >= len(b_stem) - 1:
            return cand_roots
        stem_key = ((b_stem[:vow_r_indx], b_stem[vow_r_indx+1:]), e_stem)
        if not stem_key in self.__vow_inf_b_indx:
            return cand_roots
        ch1 = b_stem[vow_r_indx]
        for root, ch0 in self.__vow_inf_b_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = VowChangeInf(ch0, ch1, StemChangePosition.INF_B_RIGHT_VOWEL, vow_r_indx)
            cand_roots.append((root, s_change))
        return cand_roots
    
    def __get_root_cand_inf_e_vow(self, b_stem, e_stem):
        cand_roots = []
        if not self.__do_inf_e_vow_change() or len(b_stem) + len(e_stem) < self.__min_stem_len or len(e_stem) < 3:
            return cand_roots
        vow_l_indx = self.__indx_vowel_l(e_stem)
        if vow_l_indx <= 0 or vow_l_indx >= len(e_stem) - 1:
            return cand_roots
        stem_key = (b_stem, (e_stem[:vow_l_indx], b_stem[vow_l_indx+1:]))
        if not stem_key in self.__vow_inf_b_indx:
            return cand_roots
        ch1 = e_stem[vow_l_indx]
        for root, ch0 in self.__vow_inf_e_indx[stem_key]:
            if ch0 == ch1:
                continue
            s_change = VowChangeInf(ch0, ch1, StemChangePosition.INF_E_LEFT_VOWEL, vow_l_indx)
            cand_roots.append((root, s_change))
        return cand_roots
    
        
    def __is_suffix(self, suf):
        return suf in self.__sufs
    
    def __is_prefix(self, pref):
        return pref in self.__prefs
    
    def __is_infix(self, inf):
        return inf in self.__infs
    
    def __is_in_lexicon(self, word):
        return word in self.__lexicon
    
#     def __index_cand(self, cand, cand_indx):
#         pass
    
    def __find_cand(self, cand_pats, cond=lambda x: False):
        for cand in cand_pats:
            if cond(cand): return cand
        return None
    
    def get_candidate_compounding(self, word):
        cand_comp_pats = []
        for i in range(self.__min_stem_len, len(word) - self.__min_stem_len):
            stem_0 = word[:i]
            stem_1 = word[i:]
            if self.__is_in_lexicon(stem_0) and self.__is_in_lexicon(stem_1):
                root_l = stem_0
                s_change_l = NonChange()
                root_r = stem_1
                s_change_r = NonChange()
                proc = Compounding(s_change_l, s_change_r)
                cand = ((root_l, root_r), proc)
                cand_comp_pats.append(cand)
        if len(cand_comp_pats) > 0:
            return cand_comp_pats
        if not self.__do_compounding_stem_change():
            return cand_comp_pats
        cand_comp_pats = []
        for i in range(self.__min_stem_len, len(word) - self.__min_stem_len):
            stem_0 = word[:i]
            stem_1 = word[i:]
            if self.__is_in_lexicon(stem_0):
                if self.__do_l_gemination() and len(stem_1) > self.__min_stem_len and stem_1[0] == stem_1[1] and self.__is_in_lexicon(stem_1[1:]):
                    root_r = stem_1[1:]
                    ch = stem_1[0]
                    s_change_r = GemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                    s_change_l = NonChange()
                    root_l = stem_0
                    proc = Compounding(s_change_l, s_change_r)
                    cand = ((root_l, root_r), proc)
                    cand_comp_pats.append(cand)
                if self.__do_l_degemination() and self.__is_in_lexicon(stem_1[0] + stem_1):
                    root_r = stem_1[0] + stem_1
                    ch = stem_1[0]
                    s_change_r = DegemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                    s_change_l = NonChange()
                    root_l = stem_0
                    proc = Compounding(s_change_l, s_change_r)
                    cand = ((root_l, root_r), proc)
                    cand_comp_pats.append(cand)
                if self.__do_l_insertion() and stem_1[0] != stem_1[1] and len(stem_1) > self.__min_stem_len and self.__is_in_lexicon(stem_1[1:]):
                    root_r = stem_1[1:]
                    ch = stem_1[0]
                    s_change_r = InsChange(ch, StemChangePosition.LEFT_BOUNDARY)
                    s_change_l = NonChange()
                    root_l = stem_0
                    proc = Compounding(s_change_l, s_change_r)
                    cand = ((root_l, root_r), proc)
                    cand_comp_pats.append(cand)
                if self.__do_l_deletion():
                    cand_roots_l_del = self.__get_root_cands_l_del(stem_1)
                    for root_r, s_change_r in cand_roots_l_del:
                        s_change_l = NonChange()
                        root_l = stem_0
                        proc = Compounding(s_change_l, s_change_r)
                        cand = ((root_l, root_r), proc)
                        cand_comp_pats.append(cand)
                if self.__do_l_substitution():
                    cand_roots_l_sub = self.__get_root_cands_l_sub(stem_1)
                    for root_r, s_change_r in cand_roots_l_sub:
                        s_change_l = NonChange()
                        root_l = stem_0
                        proc = Compounding(s_change_l, s_change_r)
                        cand = ((root_l, root_r), proc)
                        cand_comp_pats.append(cand)
                if self.__do_l_vow_change():
                    cand_roots_l_vow = self.__get_root_cands_l_vow(stem_1)
                    for root_r, s_change_r in cand_roots_l_vow:
                        s_change_l = NonChange()
                        root_l = stem_0
                        proc = Compounding(s_change_l, s_change_r)
                        cand = ((root_l, root_r), proc)
                        cand_comp_pats.append(cand)
            elif self.__is_in_lexicon(stem_1):
                if self.__do_r_gemination() and len(stem_0) > self.__min_stem_len and stem_0[-1] == stem_0[-2] and self.__is_in_lexicon(stem_0[:-1]):
                    root_l = stem_0[:-1]
                    ch = stem_0[-1]
                    s_change_l = GemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                    s_change_r = NonChange()
                    root_r = stem_1
                    proc = Compounding(s_change_l, s_change_r)
                    cand = ((root_l, root_r), proc)
                    cand_comp_pats.append(cand)
                if self.__do_r_degemination() and self.__is_in_lexicon(stem_0 + stem_0[-1]):
                    root_l = stem_0 + stem_0[-1]
                    ch = stem_0[-1]
                    s_change_l = DegemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                    s_change_r = NonChange()
                    root_r = stem_1
                    proc = Compounding(s_change_l, s_change_r)
                    cand = ((root_l, root_r), proc)
                    cand_comp_pats.append(cand)
                if self.__do_r_insertion() and stem_0[-1] != stem_0[-2] and len(stem_0) > self.__min_stem_len and self.__is_in_lexicon(stem_0[:-1]):
                    root_l = stem_0[:-1]
                    ch = stem_0[-1]
                    s_change_l = InsChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                    s_change_r = NonChange()
                    root_r = stem_1
                    proc = Compounding(s_change_l, s_change_r)
                    cand = ((root_l, root_r), proc)
                    cand_comp_pats.append(cand)
                if self.__do_r_deletion():
                    cand_roots_r_del = self.__get_root_cands_r_del(stem_0)
                    for root_l, s_change_l in cand_roots_r_del:
                        s_change_r = NonChange()
                        root_r = stem_1
                        proc = Compounding(s_change_l, s_change_r)
                        cand = ((root_l, root_r), proc)
                        cand_comp_pats.append(cand)
                if self.__do_r_substitution():
                    cand_roots_r_sub = self.__get_root_cands_r_sub(stem_0)
                    for root_l, s_change_l in cand_roots_r_sub:
                        s_change_r = NonChange()
                        root_r = stem_1
                        proc = Compounding(s_change_l, s_change_r)
                        cand = ((root_l, root_r), proc)
                        cand_comp_pats.append(cand)
                if self.__do_r_vow_change():
                    cand_roots_r_vow = self.__get_root_cands_r_vow(stem_0)
                    for root_l, s_change_l in cand_roots_r_vow:
                        s_change_r = NonChange()
                        root_r = stem_1
                        proc = Compounding(s_change_l, s_change_r)
                        cand = ((root_l, root_r), proc)
                        cand_comp_pats.append(cand)
            else:
                pass
        return cand_comp_pats
    
    def get_candidate_analyses(self, word):
        cand_pats = []
        if len(word) <= self.__min_stem_len:
            #cand_pats.append((word, Automic()))
            return cand_pats
        #------------------- 
        # Generate full reduplication: possibly with stem changes 
        #-------------------
        cand_red_pats = []
        if self.__do_reduplication() and len(word) >= 2 * self.__min_stem_len:
            word_len = len(word)
            if word_len % 2 == 0:
                m_indx = word_len // 2
                stem_0 = word[:m_indx]
                stem_1 = word[m_indx:]
                # If the two parts are exactly the same
                if stem_0 == stem_1:
                    # If the root is required to be attested
                    b_change = NonChange()
                    e_change = NonChange()
                    proc = Reduplication(b_change, e_change)
                    root = stem_0
                    cand = (root, proc)
                    cand_red_pats.append(cand)
                    if self.__is_in_lexicon(stem_0):
                        # THis is very confident, no more analysis
                        return cand_red_pats
                    else:
                        # Add to pseudo lexicon
                        pass
            else:
                m_indx = word_len // 2
                stem_0 = word[:m_indx]
                ch = word[m_indx]
                stem_1 = word[m_indx + 1:]
                if stem_0 == stem_1 and self.__is_in_lexicon(stem_0):
                    if ch == stem_0[-1] and self.__do_r_gemination():
                        b_change = GemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                        e_change = NonChange()
                        proc = Reduplication(b_change, e_change)
                        root = stem_0
                        cand = (root, proc)
                        cand_red_pats.append(cand)
                    if ch == stem_1[0] and self.__do_l_gemination():
                        b_change = NonChange()
                        e_change = GemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                        proc = Reduplication(b_change, e_change)
                        root = stem_0
                        cand = (root, proc)
                        cand_red_pats.append(cand)
                    if ch != stem_0[-1] and ch != stem_1[0]:
                        if self.__do_l_insertion():
                            b_change = NonChange()
                            e_change = InsChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            proc = Reduplication(b_change, e_change)
                            root = stem_0
                            cand = (root, proc)
                            cand_red_pats.append(cand)
                        elif self.__do_r_insertion():
                            b_change = InsChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            e_change = NonChange()
                            proc = Reduplication(b_change, e_change)
                            root = stem_0
                            cand = (root, proc)
                            cand_red_pats.append(cand)
                    return cand_red_pats
        cand_pref_pats = []
        if self.__do_prefixation():
            for i in range(self.__min_pref_len, 1 + min(self.__max_pref_len, len(word) - self.__min_stem_len)):
                pref = word[:i]
                stem = word[i:]
                if self.__is_prefix(pref) and self.__is_in_lexicon(stem):
                    s_change = NonChange()
                    root = stem
                    proc = Prefixation(s_change, pref)
                    cand = (root, proc)
                    cand_pref_pats.append(cand)
                    # Index the candidate for other search
                    #self.__index_cand(cand, cand_indx)
        cand_suf_pats = []
        if self.__do_suffixation():
            for i in range(max(self.__min_stem_len, len(word) - self.__max_suf_len), len(word) - self.__min_suf_len + 1):
                stem = word[:i]
                suf = word[i:]
                if self.__is_suffix(suf) and self.__is_in_lexicon(stem):
                    s_change = NonChange()
                    root = stem
                    proc = Suffixation(s_change, suf)
                    cand = (root, proc)
                    cand_suf_pats.append(cand)
                    # Index the candidate for other search
                    #self.__index_cand(cand, cand_indx)
        cand_suf_fv_pats = []
        if self.__do_suffixation() and self.__do_final_vowel():
            #cand_suf_fv_pats.append()
            pass
        cand_left_red_pats = []
        if self.__do_left_reduplication():
            #-----------------
            # Left reduplication without stem changes 
            #-----------------
            for i in range(self.__min_cpy_len, 1 + min(self.__max_cpy_len, len(word) - self.__min_stem_len, len(word) // 2)):
                bx = word[:i]
                x = word[i:]
                if not x.startswith(bx):
                    continue
                if not self.__is_in_lexicon(x):
                    continue
                if self.__find_cand(cand_suf_pats, cond=lambda x: len(x[0]) >= 2 * i):
                    # Suffixation first. Heuristic: Partial reduplication is always inside the suffixation, closer to root 
                    continue
                b_change = NonChange()
                s_change = NonChange()
                root = x
                indx = i
                proc = LeftPartialCopy(b_change, s_change, indx)
                cand = (root, proc)
                cand_left_red_pats.append(cand)
        cand_right_red_pats = []
        if self.__do_right_reduplication():
            #-----------------
            # Right reduplication without stem changes 
            #-----------------
            for i in range(max(self.__min_stem_len, len(word) - self.__max_cpy_len, len(word) // 2), len(word) - self.__min_cpy_len):
                x = word[:i]
                ex = word[i:]
                if not x.endswith(ex):
                    continue
                if not self.__is_in_lexicon(x):
                    continue
                if self.__find_cand(cand_pref_pats, cond=lambda x: len(x[0]) >= 2 * len(ex)):
                    # Prefixation first. Heuristic: Partial reduplication is always inside the suffixation, closer to root 
                    continue
                # (lp.1.) Go to the next position directly
                b_change = NonChange()
                s_change = NonChange()
                root = x
                indx = i
                proc = RightPartialCopy(b_change, s_change, indx)
                cand = (root, proc)
                cand_right_red_pats.append(cand)
        cand_inf_pats = []
        if self.__do_infixation():
            bad_j = set()
            for i in range(1, len(word) - self.__min_stem_len - self.__min_inf_len + 1):
                bx = word[:i]
                if self.__do_prefixation() and self.__is_prefix(bx) and self.__is_in_lexicon(word[i:]):
                    continue
                for j in range(i + self.__min_inf_len, 1 + min(i + self.__max_inf_len, len(word) + i - self.__min_stem_len, len(word) - 1)):
                    if j in bad_j:
                        continue
                    inf = word[i:j]
                    ex = word[j:]
                    stem = bx + ex
                    if not self.__is_infix(inf):
                        continue
                    if not self.__is_in_lexicon(stem):
                        continue
                    if self.__do_suffixation() and self.__is_suffix(ex) and self.__is_in_lexicon(word[:j]):
                        bad_j.add(j)
                        continue
                    if self.__do_final_vowel() and j == len(word) - 1 and self.__is_vowel(word[j]) and self.__find_cand(cand_suf_fv_pats, cond=lambda x: len(x[0] < j)):
                        bad_j.add(j)
                        continue
                    s_change = NonChangeInf()
                    root = stem
                    indx = i
                    proc = Infixation(s_change, inf, indx)
                    cand = (root, proc)
                    cand_inf_pats.append(cand)
        # Generating candidate analyses with possible stem changes
        cand_b_red_sub_pats = []
        cand_b_red_vow_pats = []
        cand_b_red_del_pats = []
        cand_b_red_degem_pats = []
        cand_e_red_sub_pats = []
        cand_e_red_vow_pats = []
        cand_e_red_del_pats = []
        cand_e_red_degem_pats = []
        if self.__do_reduplication() and len(word) >= 2 * self.__min_stem_len:
            if len(word) % 2 == 0:
                m_indx = len(word) // 2
                stem_0 = word[:m_indx]
                stem_1 = word[m_indx:]
                if stem_0 == stem_1:
                    pass
                else:
                    if self.__do_r_substitution() and stem_0[:-1] == stem_1[:-1] and self.__is_in_lexicon(stem_1):
                        # Substitution on the left
                        ch0 = stem_1[-1]
                        ch1 = stem_0[-1]
                        # It has been guaranteed ch0 != ch1
                        pos = StemChangePosition.RIGHT_BOUNDARY
                        b_change = SubChange(ch0, ch1, pos)
                        e_change = NonChange()
                        proc = Reduplication(b_change, e_change)
                        root = stem_1
                        cand = (root, proc)
                        cand_b_red_sub_pats.append(cand)
                    if self.__do_l_substitution() and stem_0[1:] == stem_1[1:] and self.__is_in_lexicon(stem_0):
                        # Substitution on the right
                        ch0 = stem_0[0]
                        ch1 = stem_1[0]
                        # It has been guaranteed ch0 != ch1
                        pos = StemChangePosition.LEFT_BOUNDARY
                        b_change = NonChange()
                        e_change = SubChange(ch0, ch1, pos)
                        proc = Reduplication(b_change, e_change)
                        root = stem_0
                        cand = (root, proc)
                        cand_e_red_sub_pats.append(cand)
                    if self.__do_r_vow_change() and self.__is_in_lexicon(stem_1):
                        r_vow_indx = self.__indx_vowel_r(stem_0)
                        if r_vow_indx > 0 and r_vow_indx < len(stem_0) - 1 and stem_0[:r_vow_indx] == stem_1[:r_vow_indx] and stem_0[r_vow_indx + 1:] == stem_1[r_vow_indx + 1:]:
                            ch0 = stem_1[r_vow_indx]
                            ch1 = stem_0[r_vow_indx]
                            # It has been guaranteed ch0 != ch1
                            b_change = VowChange(ch0, ch1, StemChangePosition.RIGHT_VOWEL, r_vow_indx)
                            e_change = NonChange()
                            proc = Reduplication(b_change, e_change)
                            root = stem_1
                            cand = (root, proc)
                            cand_b_red_vow_pats.append(cand)
                    if self.__do_l_vow_change() and self.__is_in_lexicon(stem_0):
                        l_vow_indx = self.__indx_vowel_l(stem_1)
                        if l_vow_indx > 0 and l_vow_indx < len(stem_1) - 1 and stem_0[:l_vow_indx] == stem_1[:l_vow_indx] and stem_0[l_vow_indx + 1:] == stem_1[l_vow_indx + 1:]:
                            ch0 = stem_0[l_vow_indx]
                            ch1 = stem_1[l_vow_indx]
                            # It has been guaranteed ch0 != ch1
                            b_change = NonChange()
                            e_change = VowChange(ch0, ch1, StemChangePosition.LEFT_VOWEL, l_vow_indx)
                            proc = Reduplication(b_change, e_change)
                            root = stem_0
                            cand = (root, proc)
                            cand_e_red_vow_pats.append(cand)
            else:
                l_indx = len(word) // 2
                r_indx = l_indx + 1
                stem_l_0 = word[:l_indx]
                stem_l_1 = word[l_indx:]
                stem_r_0 = word[:r_indx]
                stem_r_1 = word[r_indx:]
                ch = word[l_indx]
                if stem_l_0 == stem_r_1:
                    pass
                else:
                    # Exclude: <pref> x x and x x <suf>
                    if stem_l_1[:-1] == stem_l_0 and self.__is_in_lexicon(stem_l_1):
                        if not (self.__do_suffixation() and self.__is_suffix(stem_l_1[-1])): # and (self.__is_in_lexicon(stem_l_0) or self.__is_in_lexicon(word[:-1]))):
                            if stem_l_1[-1] == stem_l_1[-2]:
                                # Degemination
                                if self.__do_r_degemination():
                                    ch = stem_l_1[-1]
                                    b_change = DegemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                                    e_change = NonChange()
                                    proc = Reduplication(b_change, e_change)
                                    root = stem_l_1
                                    cand = (root, proc)
                                    cand_b_red_degem_pats.append(cand)
                            else:
                                # Deletion
                                if self.__do_r_deletion():
                                    ch = stem_l_1[-1]
                                    b_change = DelChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                                    e_change = NonChange()
                                    proc = Reduplication(b_change, e_change)
                                    root = stem_l_1
                                    cand = (root, proc)
                                    cand_b_red_del_pats.append(cand)
                    if stem_r_0[1:] == stem_r_1 and self.__is_in_lexicon(stem_r_0):
                        if not (self.__do_prefixation() and self.__is_prefix(stem_l_1[-1])): # and (self.__is_in_lexicon(stem_r_1) or self.__is_in_lexicon(word[1:]))):
                            if stem_r_0[0] == stem_r_0[1]:
                                if self.__do_l_degemination():
                                    ch = stem_r_0[0]
                                    b_change = NonChange()
                                    e_change = DegemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                                    proc = Reduplication(b_change, e_change)
                                    root = stem_l_1
                                    cand = (root, proc)
                                    cand_e_red_degem_pats.append(cand)
                            else:
                                if self.__do_l_deletion():
                                    ch = stem_r_0[0]
                                    b_change = NonChange()
                                    e_change = DelChange(ch, StemChangePosition.LEFT_BOUNDARY)
                                    proc = Reduplication(b_change, e_change)
                                    root = stem_l_1
                                    cand = (root, proc)
                                    cand_e_red_del_pats.append(cand)
        cand_left_red_b_sub_pats = []
        #-----------------------------------------------------------------
        #cand_left_red_b_ins_pats = []
        #-----------------------------------------------------------------
        cand_left_red_b_gem_pats = []
        #-----------------------------------------------------------------
        #cand_left_red_b_del_pats = []
        #cand_left_red_b_degem_pats = []
        #-----------------------------------------------------------------
        cand_left_red_b_vow_pats = []
        cand_left_red_s_sub_pats = []
        cand_left_red_s_ins_pats = []
        cand_left_red_s_gem_pats = []
        cand_left_red_s_del_pats = []
        cand_left_red_s_degem_pats = []
        cand_left_red_s_vow_pats = []
        #cand_left_red_sc_pats = []
        if self.__do_left_reduplication() and len(cand_left_red_pats) == 0 and len(cand_suf_pats) == 0:
            #-----------------
            # Left reduplication with stem changes 
            #-----------------
            for i in range(self.__min_cpy_len, 1 + min(self.__max_cpy_len, len(word) - self.__min_stem_len, len(word) // 2)):
                bx = word[:i]
                x = word[i:]
                if x.startswith(bx):
                    continue
                if self.__is_in_lexicon(x):
                    if self.__do_prefixation() and self.__is_prefix(bx):
                        continue
                    if x.startswith(bx[:-1]) and len(bx) >= 2:
                        if bx[-1] == bx[-2]:
                            # ex: kaa-kain
                            if self.__do_r_gemination() and len(bx) >= self.__min_cpy_len + 1:
                                ch = bx[-1]
                                b_change = GemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                                s_change = NonChange()
                                root = x
                                indx = len(bx) - 1
                                proc = LeftPartialCopy(b_change, s_change, indx)
                                cand = (root, proc)
                                cand_left_red_b_gem_pats.append(cand)
                        elif bx[-1] == x[0]:
                            # This is a gemination of x on i-1 position
                            pass
                        else:
                            if self.__do_r_substitution():
                                # This is ambiguous here, it could be substitution on bx | insertion on bx | insertion on x
                                # Since this is arbitrary, only one is chosen, unless there is a preferred typological feature 
                                # ex: ku-kain
                                indx = len(bx)
                                ch0 = x[indx-1]
                                ch1 = bx[indx-1]
                                if ch0 != ch1:
                                    b_change = SubChange(ch0, ch1, StemChangePosition.RIGHT_BOUNDARY)
                                    s_change = NonChange()
                                    root = x
                                    proc = LeftPartialCopy(b_change, s_change, indx)
                                    cand = (root, proc)
                                    cand_left_red_b_sub_pats.append(cand)
                    if self.__do_r_vow_change():
                        # Check vowel change in bx
                        # ex: hip-hopic
                        r_vow_indx = self.__indx_vowel_r(bx)
                        if r_vow_indx > 0 and r_vow_indx < len(bx) - 1 and x.startswith(bx[:r_vow_indx] + x[r_vow_indx] + bx[r_vow_indx + 1:]):
                            ch0 = x[r_vow_indx]
                            ch1 = bx[r_vow_indx]
                            if ch0 != ch1:
                                b_change = VowChange(ch0, ch1, StemChangePosition.RIGHT_VOWEL, r_vow_indx)
                                s_change = NonChange()
                                root = x
                                indx = len(bx)
                                proc = LeftPartialCopy(b_change, s_change, indx)
                                cand = (root, proc)
                                cand_left_red_b_vow_pats.append(cand)
                    if False:
                        pass
                if self.__do_prefixation() and self.__is_prefix(bx[0]) and self.__is_in_lexicon(bx[1:] + x):
                    continue
                if len(cand_left_red_b_gem_pats) + len(cand_left_red_b_sub_pats) + len(cand_left_red_b_vow_pats) > 0:
                    continue
                if x[1:].startswith(bx[1:]) and self.__is_in_lexicon(bx[0] + x[1:]):
                    # Substitution on x
                    # (ka-gain, kain)
                    ch0 = bx[0]
                    ch1 = x[0]
                    # It has been guaranteed that ch0 != ch1
                    if ch0 != ch1 and self.__do_l_substitution():
                        b_change = NonChange()
                        s_change = SubChange(ch0, ch1, StemChangePosition.LEFT_BOUNDARY)
                        root = bx[0] + x[1:]
                        indx = len(bx)
                        proc = LeftPartialCopy(b_change, s_change, indx)
                        cand = (root, proc)
                        cand_left_red_s_sub_pats.append(cand)
                if x.startswith(bx[1:]) and self.__is_in_lexicon(bx[0] + x):
                    # Deletion/Degemination on x
                    # (lla-lama, llama)
                    ch = bx[0]
                    if ch == bx[1]:
                        if self.__do_l_degemination():
                            b_change = NonChange()
                            s_change = DegemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            root = bx[0] + x
                            indx = len(bx)
                            proc = LeftPartialCopy(b_change, s_change, indx)
                            cand = (root, proc)
                            cand_left_red_s_degem_pats.append(cand)
                    else:
                        if self.__do_l_deletion():
                            b_change = NonChange()
                            s_change = DelChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            root = bx[0] + x
                            indx = len(bx)
                            proc = LeftPartialCopy(b_change, s_change, indx)
                            cand = (root, proc)
                            cand_left_red_s_del_pats.append(cand)
                if x[1:].startswith(bx) and len(x) > self.__min_stem_len and len(x) - 1 > len(bx) and self.__is_in_lexicon(x[1:]):
                    # ex: (ka-kkain, kain)
                    if x[0] == x[1]:
                        if self.__do_l_gemination():
                            ch = x[0]
                            b_change = NonChange()
                            s_change = GemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            root = x[1:]
                            indx = len(bx)
                            proc = LeftPartialCopy(b_change, s_change, indx)
                            cand = (root, proc)
                            cand_left_red_s_gem_pats.append(cand)
                    else:
                        if self.__do_l_insertion():
                            ch = x[0]
                            b_change = NonChange()
                            s_change = InsChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            root = x[1:]
                            indx = len(bx)
                            proc = LeftPartialCopy(b_change, s_change, indx)
                            cand = (root, proc)
                            cand_left_red_s_ins_pats.append(cand)
                if self.__do_l_vow_change():
                    # Check vowel change stem change on x
                    l_vow_indx = self.__indx_vowel_l(x)
                    if l_vow_indx > 0 and l_vow_indx < len(bx) - 1:
                        ch0 = bx[l_vow_indx]
                        ch1 = x[l_vow_indx]
                        root = x[:l_vow_indx] + ch0 + x[l_vow_indx+1:]
                        if ch0 != ch1 and self.__is_in_lexicon(root) and root.startswith(bx):
                            b_change = NonChange()
                            s_change = VowChange(ch0, ch1, StemChangePosition.LEFT_VOWEL, l_vow_indx)
                            root = x[:l_vow_indx] + bx[l_vow_indx] + x[l_vow_indx+1:]
                            indx = len(bx)
                            proc = LeftPartialCopy(b_change, s_change, indx)
                            cand = (root, proc)
                            cand_left_red_s_vow_pats.append(cand)
        cand_right_red_s_sub_pats = []
        cand_right_red_s_ins_pats = []
        cand_right_red_s_gem_pats = []
        cand_right_red_s_del_pats = []
        cand_right_red_s_degem_pats = []
        cand_right_red_s_vow_pats = []
        cand_right_red_e_sub_pats = []
        #---------------------- Insertion is put on x rather than ex -----
        #cand_right_red_e_ins_pats = []
        #-----------------------------------------------------------------
        cand_right_red_e_gem_pats = []
        #---------------------- No deletion/degemination on ex -----------
        #cand_right_red_e_del_pats = []
        #cand_right_red_e_degem_pats = []
        #-----------------------------------------------------------------
        cand_right_red_e_vow_pats = []
        #cand_right_red_sc_pats = []
        if self.__do_right_reduplication() and len(cand_right_red_pats) == 0 and len(cand_pref_pats) == 0:
            #-----------------
            # Right reduplication with stem changes 
            #-----------------
            for i in range(max(self.__min_stem_len, len(word) - self.__max_cpy_len, len(word) // 2), len(word) - self.__min_cpy_len):
                x = word[:i]
                ex = word[i:]
                if x.endswith(ex):
                    continue
                if self.__is_in_lexicon(x):
                    if self.__do_suffixation() and self.__is_suffix(ex):
                        continue
                    if x.endswith(ex[1:]) and len(ex) >= 2:
                        if ex[0] == ex[1]:
                            # ex: kamon-oon
                            if self.__do_l_gemination() and len(ex) >= self.__min_cpy_len + 1:
                                ch = ex[0]
                                s_change = NonChange()
                                e_change = GemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                                root = x
                                indx = len(x) - len(ex) + 1
                                proc = RightPartialCopy(s_change, e_change, indx)
                                cand = (root, proc)
                                cand_right_red_e_gem_pats.append(cand)
                        elif ex[0] == x[-1]:
                            # This is a gemination of x on i+1 position
                            pass
                        else:
                            if self.__do_l_substitution():
                                # This is ambiguous here, it could be substitution on ex | insertion on ex | insertion on x
                                # Since this is arbitrary, only one is chosen, unless there is a preferred typological feature 
                                # kain-on
                                ch0 = x[0]
                                ch1 = ex[0]
                                if ch0 != ch1:
                                    s_change = NonChange()
                                    e_change = SubChange(ch0, ch1, StemChangePosition.LEFT_BOUNDARY)
                                    root = x
                                    indx = len(x) - len(ex)
                                    proc = RightPartialCopy(s_change, e_change, indx)
                                    cand = (root, proc)
                                    cand_right_red_e_sub_pats.append(cand)
                    if self.__do_l_vow_change():
                        # Check vowel change on ex
                        # ex: (kanmon-men, kamon)
                        l_vow_indx = self.__indx_vowel_l(ex)
                        if l_vow_indx > 0 and l_vow_indx < len(ex) - 1 and x.endswith(ex[:l_vow_indx] + x[l_vow_indx] + ex[l_vow_indx + 1:]):
                            ch0 = x[l_vow_indx]
                            ch1 = ex[l_vow_indx]
                            if ch0 != ch1:
                                s_change = NonChange()
                                e_change = VowChange(ch0, ch1, StemChangePosition.LEFT_VOWEL, l_vow_indx)
                                root = x
                                indx = len(x) - len(ex)
                                proc = RightPartialCopy(s_change, e_change, indx)
                                cand = (root, proc)
                                cand_right_red_e_vow_pats.append(cand)
                    if False:
                        # No deletion/degemination on ex
                        # Insertion is put on x
                        pass
                if self.__do_suffixation() and self.__is_suffix(ex[-1]) and self.__is_in_lexicon(x + ex[:-1]):
                    continue
                if len(cand_right_red_e_gem_pats) + len(cand_right_red_e_sub_pats) + len(cand_right_red_e_vow_pats) > 0:
                    continue
#                 if self.__do_sufixation() and self.__is_suffix(x[-1] + ex) and self.__is_in_lexicon(x[:-1]):
#                     continue
                if self.__do_r_substitution() and x[:-1].endswith(ex[:-1]) and self.__is_in_lexicon(x[:-1] + ex[-1]):
                    # Substitution on right boundary of x
                    # ex: (kaim-in, kain)
                    ch0 = ex[-1]
                    ch1 = x[-1]
                    s_change = SubChange(ch0, ch1, StemChangePosition.RIGHT_BOUNDARY)
                    e_change = NonChange()
                    root = x[:-1] + ex[-1]
                    indx = len(x) - len(ex)
                    proc = RightPartialCopy(s_change, e_change, indx)
                    cand = (root, proc)
                    cand_right_red_s_sub_pats.append(cand)
                if x.endswith(ex[:-1]) and self.__is_in_lexicon(x + ex[-1]):
                    # Deletion/Degemination on x
                    # ex: (kamon-onn, kamonn)
                    ch = ex[-1]
                    if ch == ex[-2]:
                        if self.__do_r_degemination():
                            s_change = DegemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            e_change = NonChange()
                            root = x + ex[-1]
                            indx = len(x) + 1 - len(ex)
                            proc = RightPartialCopy(s_change, e_change, indx)
                            cand = (root, proc)
                            cand_right_red_s_degem_pats.append(cand)
                    else:
                        if self.__do_r_deletion():
                            s_change = DelChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            e_change = NonChange()
                            root = x + ex[-1]
                            indx = len(x) + 1 - len(ex)
                            proc = RightPartialCopy(s_change, e_change, indx)
                            cand = (root, proc)
                            cand_right_red_s_del_pats.append(cand)
                if x[:-1].endswith(ex) and len(x) > self.__min_stem_len and len(x) - 1 > len(ex) and self.__is_in_lexicon(x[:-1]):
                    # ex: (kamonn-on, kamon)
                    if x[-1] == x[-2]:
                        if self.__do_r_gemination():
                            ch = x[-1]
                            s_change = GemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            e_change = NonChange()
                            root = x[:-1]
                            indx = len(x) - 1 - len(ex)
                            proc = RightPartialCopy(s_change, e_change, indx)
                            cand = (root, proc)
                            cand_right_red_s_gem_pats.append(cand)
                    else:
                        if self.__do_r_insertion():
                            ch = x[-1]
                            s_change = InsChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            e_change = NonChange()
                            root = x[:-1]
                            indx = len(x) - 1 - len(ex)
                            proc = RightPartialCopy(s_change, e_change, indx)
                            cand = (root, proc)
                            cand_right_red_s_ins_pats.append(cand)
                if self.__do_r_vow_change():
                    # Check vowel change stem change on x
                    r_vow_indx = self.__indx_vowel_r(x)
                    if r_vow_indx > 0 and r_vow_indx < len(ex) - 1:
                        ch0 = ex[r_vow_indx]
                        ch1 = x[r_vow_indx]
                        root = x[:r_vow_indx] + ch0 + x[r_vow_indx+1:]
                        if ch0 != ch1 and self.__is_in_lexicon(root) and root.endswith(ex):
                            s_change = VowChange(ch0, ch1, StemChangePosition.RIGHT_VOWEL, r_vow_indx)
                            e_change = NonChange()
                            root = x[:r_vow_indx] + ex[r_vow_indx] + x[r_vow_indx+1:]
                            indx = len(x) - len(ex)
                            proc = RightPartialCopy(s_change, e_change, indx)
                            cand = (root, proc)
                            cand_right_red_s_vow_pats.append(cand)
        cand_pref_ins_pats = []
        cand_pref_gem_pats = []
        cand_pref_del_pats = []
        cand_pref_degem_pats = []
        cand_pref_sub_pats = []
        cand_pref_vow_pats = []
        #cand_pref_sc_pats = []
        if self.__do_prefixation():
            for i in range(self.__min_pref_len, 1 + min(self.__max_pref_len, len(word) - self.__min_stem_len)):
                pref = word[:i]
                stem = word[i:]
                if not self.__is_prefix(pref):
                    continue
                if self.__is_in_lexicon(stem):
                    continue
                if not self.__is_prefix(pref + stem[0]) and self.__is_in_lexicon(stem[1:]):
                    if stem[0] == stem[1]:
                        #Gem
                        if self.__do_l_gemination():
                            ch = stem[0]
                            s_change = GemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            root = stem[1:]
                            proc = Prefixation(s_change, pref)
                            cand = (root, proc)
                            cand_pref_gem_pats.append(cand)
                    else:
                        # Ins
                        if self.__do_l_insertion():
                            ch = stem[0]
                            s_change = InsChange(ch, StemChangePosition.LEFT_BOUNDARY)
                            root = stem[1:]
                            proc = Prefixation(s_change, pref)
                            cand = (root, proc)
                            cand_pref_ins_pats.append(cand)
                if self.__do_l_degemination() and stem[0] != pref[-1] and self.__is_in_lexicon(stem[0] + stem):
                    ch = stem[0]
                    s_change = DegemChange(ch, StemChangePosition.LEFT_BOUNDARY)
                    proc = Prefixation(s_change, pref)
                    root = stem[0] + stem
                    cand = (root, proc)
                    cand_pref_degem_pats.append(cand)
                if self.__do_l_deletion() and not (self.__is_prefix(pref[:-1]) and self.__is_in_lexicon(pref[-1] + stem)):
                    cand_roots_l_del = self.__get_root_cands_l_del(stem)
                    for root, s_change in cand_roots_l_del:
                        ch = s_change.ch()
                        if ch == pref or (ch == pref[-1] and self.__is_prefix(pref[:-1])):
                            continue
                        proc = Prefixation(s_change, pref)
                        cand = (root, proc)
                        cand_pref_del_pats.append(cand)
                if self.__do_l_substitution():
                    cand_roots_l_sub = self.__get_root_cands_l_sub(stem)
                    for root, s_change in cand_roots_l_sub:
                        proc = Prefixation(s_change, pref)
                        cand = (root, proc)
                        cand_pref_sub_pats.append(cand)
                if self.__do_l_vow_change():
                    cand_roots_l_vow = self.__get_root_cands_l_vow(stem)
                    for root, s_change in cand_roots_l_vow:
                        proc = Prefixation(s_change, pref)
                        cand = (root, proc)
                        cand_pref_vow_pats.append(cand)
        cand_suf_ins_pats = []
        cand_suf_gem_pats = []
        cand_suf_del_pats = []
        cand_suf_degem_pats = []
        cand_suf_sub_pats = []
        cand_suf_vow_pats = []
        if self.__do_suffixation():
            for i in range(max(self.__min_stem_len, len(word) - self.__max_suf_len), len(word) - self.__min_suf_len + 1):
                stem = word[:i]
                suf = word[i:]
                if not self.__is_suffix(suf):
                    continue
                if self.__is_in_lexicon(stem):
                    continue
                if not self.__is_suffix(stem[-1] + suf) and self.__is_in_lexicon(stem[:-1]):
                    if stem[-1] == stem[-2]:
                        #Gem
                        if self.__do_r_gemination():
                            ch = stem[-1]
                            s_change = GemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            root = stem[:-1]
                            proc = Suffixation(s_change, suf)
                            cand = (root, proc)
                            cand_suf_gem_pats.append(cand)
                    else:
                        # Ins
                        if self.__do_r_insertion():
                            ch = stem[-1]
                            s_change = InsChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                            root = stem[:-1]
                            proc = Suffixation(s_change, suf)
                            cand = (root, proc)
                            cand_suf_ins_pats.append(cand)
                if self.__do_r_degemination() and stem[-1] != suf[0] and self.__is_in_lexicon(stem + stem[-1]):
                    ch = stem[-1]
                    s_change = DegemChange(ch, StemChangePosition.RIGHT_BOUNDARY)
                    proc = Suffixation(s_change, suf)
                    root = stem + stem[-1]
                    cand = (root, proc)
                    cand_suf_degem_pats.append(cand)
                if self.__do_r_deletion() and not (self.__is_suffix(suf[1:]) and self.__is_in_lexicon(stem + suf[0])):
                    cand_roots_r_del = self.__get_root_cands_r_del(stem)
                    for root, s_change in cand_roots_r_del:
                        ch = s_change.ch()
                        if ch == suf or (ch == suf[0] and self.__is_suffix(suf[1:])):
                            continue
                        proc = Suffixation(s_change, suf)
                        cand = (root, proc)
                        cand_suf_del_pats.append(cand)
                if self.__do_r_substitution():
                    cand_roots_r_sub = self.__get_root_cands_r_sub(stem)
                    for root, s_change in cand_roots_r_sub:
                        proc = Suffixation(s_change, suf)
                        cand = (root, proc)
                        cand_suf_sub_pats.append(cand)
                if self.__do_r_vow_change():
                    cand_roots_r_vow = self.__get_root_cands_r_vow(stem)
                    for root, s_change in cand_roots_r_vow:
                        proc = Suffixation(s_change, suf)
                        cand = (root, proc)
                        cand_suf_vow_pats.append(cand)
        if self.__do_suffixation() and self.__do_final_vowel():
            pass
        cand_inf_b_ins_pats = []
        cand_inf_b_gem_pats = []
        cand_inf_b_del_pats = []
        cand_inf_b_degem_pats = []
        cand_inf_b_sub_pats = []
        cand_inf_b_vow_pats = []
        cand_inf_e_ins_pats = []
        cand_inf_e_gem_pats = []
        cand_inf_e_del_pats = []
        cand_inf_e_degem_pats = []
        cand_inf_e_sub_pats = []
        cand_inf_e_vow_pats = []
        if self.__do_infixation():
            #------------------- 
            # Generate Infixation: search left: j < i: c0 c1 c2 ... c_j ... c_i ... c_n-1 (so that heuristic rules can be tested with position j that has been searched)
            #-------------------
            bad_j = set()
            for i in range(1, len(word) - self.__min_stem_len - self.__min_inf_len + 1):
                bx = word[:i]
                if self.__do_prefixation() and self.__is_prefix(bx) and self.__is_in_lexicon(word[i:]):
                    continue
                for j in range(i + self.__min_inf_len, 1 + min(i + self.__max_inf_len, len(word) + i - self.__min_stem_len, len(word) - 1)):
                    if j in bad_j:
                        continue
                    inf = word[i:j]
                    ex = word[j:]
                    stem = bx + ex
                    if not self.__is_infix(inf):
                        continue
                    if self.__is_in_lexicon(stem):
                        #
                        continue
                    if self.__do_suffixation() and self.__is_suffix(ex) and self.__is_in_lexicon(word[:j]):
                        bad_j.add(j)
                        continue
                    if self.__do_final_vowel() and j == len(word) - 1 and self.__is_vowel(word[j]) and self.__find_cand(cand_suf_fv_pats, cond=lambda x: len(x[0] < j)):
                        bad_j.add(j)
                        continue
                    if self.__do_inf_e_degemination() and len(ex) >= 2 and self.__is_in_lexicon(bx + ex[0] + ex) and inf[-1] != ex[0]:
                        ch = ex[0]
                        s_change = DegemChangeInf(ch, StemChangePosition.INF_E_LEFT_BOUNDARY)
                        root = bx + ex[0] + ex
                        indx = i
                        proc = Infixation(s_change, inf, indx)
                        cand = (root, proc)
                        cand_inf_e_degem_pats.append(cand)
                    if self.__do_inf_b_degemination() and len(bx) >=2 and self.__is_in_lexicon(bx + bx[-1] + ex) and inf[0] != bx[-1]:
                        ch = bx[-1]
                        s_change = DegemChangeInf(ch, StemChangePosition.INF_B_RIGHT_BOUNDARY)
                        root = bx + bx[-1] + ex
                        indx = i
                        proc = Infixation(s_change, inf, indx)
                        cand = (root, proc)
                        cand_inf_b_degem_pats.append(cand)
                    if self.__do_inf_e_deletion() and len(ex) >= 2:
                        cand_roots_inf_e_del = self.__get_root_cand_inf_e_del(bx, ex)
                        for root, s_change in cand_roots_inf_e_del:
                            indx = i
                            proc = Infixation(s_change, inf, indx)
                            cand = (root, proc)
                            cand_inf_e_del_pats.append(cand)
                    if self.__do_inf_b_deletion() and len(bx) >= 2:
                        cand_roots_inf_b_del = self.__get_root_cand_inf_b_del(bx, ex)
                        for root, s_change in cand_roots_inf_b_del:
                            indx = i + 1
                            proc = Infixation(s_change, inf, indx)
                            cand = (root, proc)
                            cand_inf_b_del_pats.append(cand)
                    if not self.__is_infix(inf + ex[0]) and len(ex) >= 2 and self.__is_in_lexicon(bx + ex[1:]):
                        if ex[0] != ex[1]:
                            if self.__do_inf_e_insertion() and inf[-1] != ex[0]:
                                ch = ex[0]
                                s_change = InsChangeInf(ch, StemChangePosition.INF_E_LEFT_BOUNDARY)
                                root = bx + ex[1:]
                                indx = i
                                proc = Infixation(s_change, inf, indx)
                                cand = (root, proc)
                                cand_inf_e_ins_pats.append(cand)
                        else:
                            if self.__do_inf_e_gemination() and inf[-1] != ex[0]:
                                ch = ex[0]
                                s_change = GemChangeInf(ch, StemChangePosition.INF_E_LEFT_BOUNDARY)
                                root = bx + ex[1:]
                                indx = i
                                proc = Infixation(s_change, inf, indx)
                                cand = (root, proc)
                                cand_inf_e_gem_pats.append(cand)
                    if not self.__is_infix(bx[-1] + inf) and len(bx) >= 2 and self.__is_in_lexicon(bx[:-1] + ex):
                        if bx[-1] != bx[-2]:
                            if self.__do_inf_b_insertion() and bx[-1] != inf[0]:
                                ch = bx[-1]
                                s_change = InsChangeInf(ch, StemChangePosition.INF_B_RIGHT_BOUNDARY)
                                root = bx[:-1] + ex
                                indx = i - 1
                                proc = Infixation(s_change, inf, indx)
                                cand = (root, proc)
                                cand_inf_b_ins_pats.append(cand)
                        else:
                            if self.__do_inf_b_gemination():
                                ch = bx[-1]
                                s_change = GemChangeInf(ch, StemChangePosition.INF_B_RIGHT_BOUNDARY)
                                root = bx[:-1] + ex
                                indx = i - 1
                                proc = Infixation(s_change, inf, indx)
                                cand = (root, proc)
                                cand_inf_b_gem_pats.append(cand)
                    if self.__do_inf_b_substitution() and len(bx) >= 2:
                        cand_roots_inf_b_sub = self.__get_root_cand_inf_b_sub(bx, ex)
                        for root, s_change in cand_roots_inf_b_sub:
                            indx = i
                            proc = Infixation(s_change, inf, indx)
                            cand = (root, proc)
                            cand_inf_b_sub_pats.append(cand)
                    if self.__do_inf_e_substitution() and len(ex) >= 2:
                        cand_roots_inf_e_sub = self.__get_root_cand_inf_e_sub(bx, ex)
                        for root, s_change in cand_roots_inf_e_sub:
                            indx = i
                            proc = Infixation(s_change, inf, indx)
                            cand = (root, proc)
                            cand_inf_e_sub_pats.append(cand)
                    if self.__do_inf_b_vow_change() and len(bx) >= 3:
                        cand_roots_inf_b_vow = self.__get_root_cand_inf_b_vow(bx, ex)
                        for root, s_change in cand_roots_inf_b_vow:
                            indx = i
                            proc = Infixation(s_change, inf, indx)
                            cand = (root, proc)
                            cand_inf_b_vow_pats.append(cand)
                    if self.__do_inf_e_vow_change() and len(ex) >= 3:
                        cand_roots_inf_e_vow = self.__get_root_cand_inf_e_vow(bx, ex)
                        for root, s_change in cand_roots_inf_e_vow:
                            indx = i
                            proc = Infixation(s_change, inf, indx)
                            cand = (root, proc)
                            cand_inf_e_vow_pats.append(cand)
        #------------------- 
        # Generate Templatic Patterns 
        # Done in future
        #-------------------
        #------------------- 
        # Generate Vowel Harmony
        # VH should be integrated with Prefixation and Suffixation\
        #-------------------
        cand_red_sc_pats = cand_b_red_sub_pats + cand_b_red_vow_pats + cand_b_red_del_pats + cand_b_red_degem_pats + cand_e_red_sub_pats + cand_e_red_vow_pats + cand_e_red_del_pats + cand_e_red_degem_pats
        cand_left_red_sc_pats = cand_left_red_b_sub_pats + cand_left_red_b_gem_pats + cand_left_red_b_vow_pats + cand_left_red_s_sub_pats + cand_left_red_s_ins_pats + cand_left_red_s_gem_pats + cand_left_red_s_del_pats + cand_left_red_s_degem_pats + cand_left_red_s_vow_pats
        cand_right_red_sc_pats = cand_right_red_s_sub_pats + cand_right_red_s_ins_pats + cand_right_red_s_gem_pats + cand_right_red_s_del_pats + cand_right_red_s_degem_pats + cand_right_red_s_vow_pats + cand_right_red_e_sub_pats + cand_right_red_e_gem_pats + cand_right_red_e_vow_pats
        cand_pref_sc_pats = cand_pref_ins_pats + cand_pref_gem_pats + cand_pref_del_pats + cand_pref_degem_pats + cand_pref_sub_pats + cand_pref_vow_pats
        cand_suf_sc_pats = cand_suf_ins_pats + cand_suf_gem_pats + cand_suf_del_pats + cand_suf_degem_pats + cand_suf_sub_pats + cand_suf_vow_pats
        cand_inf_sc_pats = cand_inf_b_ins_pats + cand_inf_b_gem_pats + cand_inf_b_del_pats + cand_inf_b_degem_pats + cand_inf_b_sub_pats + cand_inf_b_vow_pats + cand_inf_e_ins_pats + cand_inf_e_gem_pats + cand_inf_e_del_pats + cand_inf_e_degem_pats + cand_inf_e_sub_pats + cand_inf_e_vow_pats
        cand_pats = cand_red_pats + cand_pref_pats + cand_suf_pats + cand_inf_pats + cand_left_red_pats + cand_right_red_pats + cand_red_sc_pats + cand_left_red_sc_pats + cand_right_red_sc_pats + cand_pref_sc_pats + cand_suf_sc_pats + cand_inf_sc_pats
#         if len(cand_pats) == 0:
#             cand_pats.append((word, Automic()))
        return cand_pats
    
# def test():
#     infix_words = 'kumakain kinakain dinulot'.split()
#     prefix_words = 'makakain unfold reread unskipped'.split()
#     suffix_words = 'folding folks folded skipped running carried sanger folling folmer folms'.split()
#     redup_words = 'omokomo kyerekyere omolomo'.split()
#     l_red_words = 'kakain'.split()
#     r_red_words = ''
#     r_vow_words = ''.split()
#     root_words = 'kain omo kyere fold folk dulot read skip run carry sing'.split()
#     lexicon = set(infix_words + prefix_words + suffix_words + redup_words + l_red_words + root_words)
#     prefs = set('un im re'.split())
#     infs = set('um in'.split())
#     sufs = set('s ing ed er ment'.split())
#     vowels = set('aeiou')
#     morph_typology = MorphTypology()
#     params = Parameter()
#     lang = English()
#     morph_typology.print_features()
#     cand_gen = UniCandGen(lang, morph_typology, params, lexicon, prefs=prefs, infs=infs, sufs=sufs)
#     for word in lexicon:
#         cand_pats = cand_gen.get_candidate_analyses(word)
#         info_str = word + ':'
#         for root, proc in cand_pats:
#             info_str += ' %s(%s, %s, %s)' % (proc.morph_type().value, root, proc.change_key(), proc.pat())
#         print(info_str)
    
 
if __name__ == '__main__':
    #test()
    pass





















