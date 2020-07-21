'''
Created on May 9, 2018

@author: xh
'''
from languages import LanguageCatalog

class Parameter():
    '''
    '''
    
    def __init__(self):
        # minimum ste length
        self.min_word_freq = 1
        self.min_stem_len = 3
        # minimum partial copy length
        self.min_partialcopy_len = 2
        self.max_partialcopy_len = 4
        # maximum & minimum suffix length
        self.max_suf_len = 6
        self.min_suf_len = 1
        # maximum & minimum prefix length
        self.max_pref_len = 6
        self.min_pref_len = 1
        # maximum & minimum infix length
        self.max_inf_len = 3
        self.min_inf_len = 2
        # Use paradigm pruning (Suggested ON)
        self.do_pruning = True
        # Search compounding (not used yet)
        self.do_compounding = False
        # Explicitly process special chars： - '
        self.do_hyphen = False
        self.do_apostrophe = False
        self.apostrophe_char = '\''
        # Case sensitive
        self.case_sensitive = True
        # Input gold affixes
        self.infile_gold_prefixes = None
        self.infile_gold_infixes = None
        self.infile_gold_suffixes = None
        
        #Output test segmentation
        self.outfile_seg = None
        self.outfile_schange = None
    
    def print_all(self):
        print('-------------Parameters---------------')
        print('do_pruning: %s' % self.do_pruning)
        print('do_compounding: %s' % self.do_compounding)
        print('do_hyphen: %s' % self.do_hyphen)
        print('do_apostrophe: %s' % self.do_apostrophe)
        print('case_sensitive: %s' % self.case_sensitive)
        print('min_stem_len: %s' % self.min_stem_len)
        print('min_partialcopy_len: %s' % self.min_partialcopy_len)
        print('max_partialcopy_len: %s' % self.max_partialcopy_len)
        print('max_suf_len: %s' % self.max_suf_len)
        print('min_suf_len: %s' % self.min_suf_len)
        print('max_pref_len: %s' % self.max_pref_len)
        print('min_pref_len: %s' % self.min_pref_len)
        print('max_inf_len: %s' % self.max_inf_len)
        print('min_inf_len: %s' % self.min_inf_len)
        print('--------------------------------------')
    

def get_best_parameter(lang):
    params = Parameter()
    # minimum partial copy length
    params.min_partialcopy_len = 2
    params.max_partialcopy_len = 4
    # maximum & minimum infix length
    params.max_inf_len = 3
    params.min_inf_len = 2
    if lang == LanguageCatalog.Akan:
        params.min_word_freq = 1
        params.min_stem_len = 2
        # maximum & minimum suffix length
        params.max_suf_len = 5
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 5
        params.min_pref_len = 1
        params.case_sensitive = True
    elif lang == LanguageCatalog.Hindi:
        params.min_word_freq = 1
        params.min_stem_len = 3
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = True
    elif lang == LanguageCatalog.Hungarian:
        params.min_word_freq = 1
        params.min_stem_len = 3
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = False
    elif lang == LanguageCatalog.Indonesian:
        params.min_word_freq = 1
        params.min_stem_len = 4
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 2
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = True
    elif lang == LanguageCatalog.Russian:
        params.min_word_freq = 1
        params.min_stem_len = 3
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = False
    elif lang == LanguageCatalog.Spanish:
        params.min_word_freq = 1
        params.min_stem_len = 3
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = False
    elif lang == LanguageCatalog.Swahili:
        params.min_word_freq = 1
        params.min_stem_len = 3
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = True
    elif lang == LanguageCatalog.Tagalog:
        params.min_word_freq = 1
        params.min_stem_len = 4
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 1
        params.case_sensitive = True
    elif lang == LanguageCatalog.Tamil:
        params.min_word_freq = 1
        params.min_stem_len = 4
        # maximum & minimum suffix length
        params.max_suf_len = 6
        params.min_suf_len = 1
        # maximum & minimum prefix length
        params.max_pref_len = 6
        params.min_pref_len = 2
        params.case_sensitive = False
    return params



















