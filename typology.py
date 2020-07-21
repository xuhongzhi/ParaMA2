'''
Created on Jan 16, 2018

@author: xh
'''

from enum import Enum
from languages import LanguageCatalog


class MorphType(Enum):
    AUTOMATIC = 'aut'
    PREFIXATION = 'pref'
    INFIXATION = 'inf'
    SUFFIXATION = 'suf'
    COMPOUNDING = 'comp'
    REDUPLICATION = 'red'
    LPARTIALCOPY = 'lptcp'
    RPARTIALCOPY = 'rptcp'
    VOWELHARMONY = 'vowh'
    TEMPLATIC = 'tpl'
    FINALVOWEL = 'fv'


class StemChangeType(Enum):
    NON = 'non'
    INS = 'ins'
    GEM = 'gem'
    DEL = 'del'
    DEGEM = 'degem'
    SUB = 'sub'
    VOW = 'vow'
    
    
class StemChangePosition(Enum):
    LEFT_BOUNDARY = 'l'
    RIGHT_BOUNDARY = 'r'
    NONBOUNDARY = 'm'
    INF_B_RIGHT_BOUNDARY = 'b_r'
    INF_E_LEFT_BOUNDARY = 'e_l'
    INF_B_RIGHT_NONBOUNDARY = 'b_m'
    INF_E_LEFT_NONBOUNDARY = 'e_m'
    LEFT_VOWEL = 'l_v'
    RIGHT_VOWEL = 'r_v'
    INF_B_RIGHT_VOWEL = 'b_r_v'
    INF_E_LEFT_VOWEL = 'e_l_v'


class MorphTypology():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        morph_features = {}
        morph_features[MorphType.PREFIXATION] = True
        morph_features[MorphType.INFIXATION] = True
        morph_features[MorphType.SUFFIXATION] = True
        morph_features[MorphType.COMPOUNDING] = True
        morph_features[MorphType.REDUPLICATION] = True
        morph_features[MorphType.LPARTIALCOPY] = True
        morph_features[MorphType.RPARTIALCOPY] = False   # Not attested in most languages
        morph_features[MorphType.TEMPLATIC] = False      # Not supported yet
        morph_features[MorphType.VOWELHARMONY] = False   # Not supported yet
        morph_features[MorphType.FINALVOWEL] = False     # Not supported yet
        self.__morph_features = morph_features
        # Stem Changes
        stem_change_features = {}
        stem_change_features[StemChangeType.INS] = True
        stem_change_features[StemChangeType.GEM] = True
        stem_change_features[StemChangeType.DEL] = True
        stem_change_features[StemChangeType.DEGEM] = True
        stem_change_features[StemChangeType.SUB] = True
        stem_change_features[StemChangeType.VOW] = True
        self.__stem_change_features = stem_change_features
        # Stem Change Positions
        stem_change_positions = {}
        stem_change_positions[StemChangePosition.LEFT_BOUNDARY] = True
        stem_change_positions[StemChangePosition.RIGHT_BOUNDARY] = True
        stem_change_positions[StemChangePosition.LEFT_VOWEL] = True
        stem_change_positions[StemChangePosition.RIGHT_VOWEL] = True
        stem_change_positions[StemChangePosition.INF_B_RIGHT_BOUNDARY] = True
        stem_change_positions[StemChangePosition.INF_E_LEFT_BOUNDARY] = True
        stem_change_positions[StemChangePosition.NONBOUNDARY] = False
        stem_change_positions[StemChangePosition.INF_B_RIGHT_NONBOUNDARY] = False
        stem_change_positions[StemChangePosition.INF_E_LEFT_NONBOUNDARY] = False
        self.__stem_change_positions = stem_change_positions
    
    def set_feature(self, feat, val):
        if not feat in self.__morph_features:
            print('Feature name not found: %s' % (feat.value))
            return
        self.__morph_features[feat] = val
    
    def set_stem_change_feat(self, schange, val):
        if not schange in self.__stem_change_features:
            return
        self.__stem_change_features[schange] = val
    
    def set_stem_change_position(self, schange_pos, val):
        if not schange_pos in self.__stem_change_positions:
            return
        self.__stem_change_positions[schange_pos] = val
    
    def has_morph_feature(self, morph_type):
        if not morph_type in self.__morph_features:
            return False
        return self.__morph_features[morph_type]
    
    def has_stem_change_feature(self, stem_change_type):
        if not stem_change_type in self.__stem_change_features:
            return False
        return self.__stem_change_features[stem_change_type]
    
    def is_valid_stem_change_position(self, stem_change_position):
        if not stem_change_position in self.__stem_change_positions:
            return False
        return self.__stem_change_positions[stem_change_position]
    
    def print_features(self):
        for morph_feat, val in self.__morph_features.items():
            print('%s = %s' % (morph_feat.value, val))
        for stem_change_feat, val in self.__stem_change_features.items():
            print('%s = %s' % (stem_change_feat.value, val))
        for stem_change_pos, val in self.__stem_change_positions.items():
            print('%s = %s' % (stem_change_pos.value, val))
    

def get_gold_features(lang):
    typo_feature = MorphTypology()
    typo_feature.set_feature(MorphType.LPARTIALCOPY, False)
    typo_feature.set_feature(MorphType.RPARTIALCOPY, False)
    typo_feature.set_stem_change_position(StemChangePosition.NONBOUNDARY, False)
    typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_NONBOUNDARY, False)
    typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_NONBOUNDARY, False)
    if lang == LanguageCatalog.Akan:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, True)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, False)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, False)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, False)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, False)
    elif lang == LanguageCatalog.Hindi:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, False)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, True)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, False)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, False)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, False)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, False)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, False)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Hungarian:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, False)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Indonesian:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, True)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Russian:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, False)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Spanish:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, False)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Swahili:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, True)
        typo_feature.set_feature(MorphType.REDUPLICATION, True)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Tagalog:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, True)
        typo_feature.set_feature(MorphType.REDUPLICATION, True)
        typo_feature.set_feature(MorphType.LPARTIALCOPY, True)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, False)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, False)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, False)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, False)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, False)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, False)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    elif lang == LanguageCatalog.Tamil:
        typo_feature.set_feature(MorphType.SUFFIXATION, True)
        typo_feature.set_feature(MorphType.PREFIXATION, True)
        typo_feature.set_feature(MorphType.INFIXATION, False)
        typo_feature.set_feature(MorphType.REDUPLICATION, False)
        #
        typo_feature.set_stem_change_feat(StemChangeType.INS, True)
        typo_feature.set_stem_change_feat(StemChangeType.GEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEL, True)
        typo_feature.set_stem_change_feat(StemChangeType.DEGEM, True)
        typo_feature.set_stem_change_feat(StemChangeType.SUB, True)
        typo_feature.set_stem_change_feat(StemChangeType.VOW, True)
        #
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.LEFT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_BOUNDARY, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_B_RIGHT_VOWEL, True)
        typo_feature.set_stem_change_position(StemChangePosition.INF_E_LEFT_VOWEL, True)
    else:
        print('Warning! Not recognized language: %s' % lang)
    return typo_feature























