'''
Created on Apr 26, 2018

@author: xh
'''

from typology import MorphType
from stemchange import NonChange

class _MorphProcess():
    '''
    A specific morphological process
    '''
    
    def __init__(self, morph_type):
        self.__morph_type = morph_type
    
    def morph_type(self):
        return self.__morph_type

class Automic(_MorphProcess):
    '''
    '''
    
    def __init__(self):
        super().__init__(MorphType.AUTOMATIC)
        self.__stem_change = NonChange()
        self.__pat = 'X'
    
    def apply(self, root):
        return root
    
    def apply2seg(self, root_seg):
        return root_seg
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return (self.__stem_change,)
    
    def change_key(self):
        return self.__stem_change.key()
    

class Prefixation(_MorphProcess):
    '''
    '''
    
    def __init__(self, stem_change, pref):
        super().__init__(MorphType.PREFIXATION)
        self.__stem_change = stem_change
        self.__pref = pref
        self.__pat = '<%s>_X' % self.__pref 
    
    def apply(self, root):
        return self.__pref + self.__stem_change.apply(root)
    
    def apply2seg(self, root_seg):
        return (self.__pref,) + self.__stem_change.apply2seg(root_seg)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return (self.__stem_change,)

    def change_key(self):
        return self.__stem_change.key()


class Suffixation(_MorphProcess):
    '''
    '''
    
    def __init__(self, stem_change, suf):
        super().__init__(MorphType.SUFFIXATION)
        self.__stem_change = stem_change
        self.__suf = suf
        self.__pat = 'X_<%s>' % self.__suf
    
    def apply(self, root):
        return self.__stem_change.apply(root) + self.__suf
    
    def apply2seg(self, root_seg):
        return self.__stem_change.apply2seg(root_seg) + (self.__suf,)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return (self.__stem_change,)
    
    def change_key(self):
        return self.__stem_change.key()



class Infixation(_MorphProcess):
    '''
    '''

    def __init__(self, stem_change, inf, indx):
        super().__init__(MorphType.INFIXATION)
        self.__stem_change = stem_change
        self.__inf = inf
        self.__indx = indx
        self.__pat = 'bX_<%s>_eX' % self.__inf
    
    
    def __split_word(self, word):
        if self.__indx > len(word):
            raise Exception('Word index error: %s' % self.__indx)
        return word[:self.__indx], word[self.__indx:]
     
    def __split_seg(self, seg):
        '''
        Given a segmented root, add an extra segmentation at position <indx> and generate a new segmentation,
        and return it with the corresponding seg index
        Example:
            root_seg: (ka, kain)
            infix: -um-, index:1
            (ka, kain) -> (k, ), (a, kain)
            + (um) -> (k, um, a, kain) 
        '''
        r_indx = 0
        for i in range(len(seg)):
            sub_len = len(seg[i])
            sub_indx = self.__indx - r_indx
            if sub_indx < sub_len:
                return tuple(seg[:i]) + (seg[i][:sub_indx],), (seg[i][sub_indx:],) + tuple(seg[i+1:])
            elif sub_indx == sub_len:
                return tuple(seg[:i+1]), tuple(seg[i+1:])
            r_indx += sub_len
        raise Exception('Segment index error: %s' % self.__indx)
    
    def apply(self, root):
        b_root, e_root = self.__split_word(root)
        b_root_1, e_root_1 = self.__stem_change.apply(b_root, e_root)
        return b_root_1 + self.__inf + e_root_1
    
    def apply2seg(self, root_seg):
        b_root_seg, e_root_seg = self.__split_seg(root_seg)
        try:
            b_root_seg_1, e_root_seg_1 = self.__stem_change.apply2seg(b_root_seg, e_root_seg)
            return b_root_seg_1 + (self.__inf,) + e_root_seg_1
        except Exception as ex:
            print('----------------exception-----------------')
            print('root seg: (%s)' % (', '.join(root_seg)))
            print('Stem change: %s' % (self.__stem_change.key()))
            print('b root seg: (%s)' % (', '.join(b_root_seg)))
            print('e root seg: (%s)' % (', '.join(e_root_seg)))
            #print(ex)
            print('-----------------------------------------')
            raise Exception(ex)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return (self.__stem_change,)
    
    def change_key(self):
        return self.__stem_change.key()



class Reduplication(_MorphProcess):
    '''
    '''

    def __init__(self, stem_change_b, stem_change_e):
        super().__init__(MorphType.REDUPLICATION)
        self.__stem_change_b = stem_change_b
        self.__stem_change_e = stem_change_e
        self.__pat = 'X_X'
    
    def apply(self, root):
        return self.__stem_change_b.apply(root) + self.__stem_change_e.apply(root) 
    
    def apply2seg(self, root_seg):
        return self.__stem_change_b.apply2seg(root_seg) + self.__stem_change_e.apply2seg(root_seg)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return (self.__stem_change_b, self.__stem_change_e)
    
    def change_key(self):
        return '%s | %s' % (self.__stem_change_b.key(), self.__stem_change_e.key())



class LeftPartialCopy(_MorphProcess):
    '''
    '''
    
    def __init__(self, stem_change_b, stem_change, indx):
        super().__init__(MorphType.LPARTIALCOPY)
        self.__stem_change_b = stem_change_b
        self.__stem_change = stem_change
        self.__indx = indx
        self.__pat = 'bX_X'
    
    
    def __b_word(self, word):
        if self.__indx > len(word):
            raise Exception('Word index error: %s' % self.__indx)
        return word[:self.__indx]
     
    def __b_seg(self, seg):
        '''
        Example:
            root_seg: (mag, kain), indx = 2
            (mag, kain) -> (ma, ), (g, kain)
            return (ma, )
        '''
        r_indx = 0
        for i in range(len(seg)):
            sub_len = len(seg[i])
            sub_indx = self.__indx - r_indx
            if sub_indx <= sub_len:
                #return tuple(seg[:i]) + (seg[i][:sub_indx],), (seg[i][sub_indx:],) + tuple(seg[i+1:])
                return tuple(seg[:i]) + (seg[i][:sub_indx],)
            r_indx += sub_len
        raise Exception('Segment index error: %s' % self.__indx)
    
    
    def apply(self, root):
        return self.__b_word(root) + self.__stem_change.apply(root)
    
    def apply2seg(self, root_seg):
        return self.__b_seg(root_seg) + self.__stem_change.apply2seg(root_seg)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return self.__stem_change_b, self.__stem_change
    
    def change_key(self):
        return '%s | %s' % (self.__stem_change_b.key(), self.__stem_change.key())


class RightPartialCopy(_MorphProcess):
    '''
    '''
    
    def __init__(self, stem_change, stem_change_e, indx):
        super().__init__(MorphType.RPARTIALCOPY)
        self.__stem_change = stem_change
        self.__stem_change_e = stem_change_e
        self.__indx = indx
        self.__pat = 'X_eX'
    
    def __e_word(self, word):
        if self.__indx > len(word):
            raise Exception('Word index error: %s' % self.__indx)
        return word[self.__indx:]
     
    def __e_seg(self, seg):
        '''
        Example:
            root_seg: (mag, kain), indx = 2
            (mag, kain) -> (ma, ), (g, kain)
            return (ma, )
        '''
        r_indx = 0
        for i in range(len(seg)):
            sub_len = len(seg[i])
            sub_indx = self.__indx - r_indx
            if sub_indx <= sub_len:
                #return tuple(seg[:i]) + (seg[i][:sub_indx],), (seg[i][sub_indx:],) + tuple(seg[i+1:])
                return (seg[i][sub_indx:],) + tuple(seg[i+1:])
            r_indx += sub_len
        raise Exception('Segment index error: %s' % self.__indx)
    
    def apply(self, root):
        return self.__stem_change.apply(root) + self.__e_word(root)
    
    def apply2seg(self, root_seg):
        return self.__stem_change.apply2seg(root_seg) + self.__e_seg(root_seg)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return self.__stem_change, self.__stem_change_e
    
    def change_key(self):
        return '%s | %s' % (self.__stem_change.key(), self.__stem_change_e.key())


class Compounding(_MorphProcess):
    '''
    '''
    
    def __init__(self, stem_change_l, stem_change_r):
        super().__init__(MorphType.COMPOUNDING)
        self.__stem_change_l = stem_change_l
        self.__stem_change_r = stem_change_r
        self.__pat = 'X_Y'
    
    def apply(self, root_l, root_r):
        return self.__stem_change_l.apply(root_l) + self.__stem_change_r.apply(root_r)
    
    def apply2seg(self, root_seg_l, root_seg_r):
        return self.__stem_change_l.apply2seg(root_seg_l) + self.__stem_change_r.apply2seg(root_seg_r)
    
    def pat(self):
        return self.__pat
    
    def change(self):
        return self.__stem_change_l, self.__stem_change_r
    
    def change_key(self):
        return '%s | %s' % (self.__stem_change_l.key(), self.__stem_change_r.key())

def parse_morph_type(pat_str):
    if pat_str == 'X':
        return MorphType.AUTOMATIC
    if pat_str == 'X_Y':
        return MorphType.COMPOUNDING
    if pat_str == 'bX_X':
        return MorphType.LPARTIALCOPY
    if pat_str == 'X_eX':
        return MorphType.RPARTIALCOPY
    if pat_str == 'X_X':
        return MorphType.REDUPLICATION
    if pat_str.startswith('<') and pat_str.endswith('>_X'):
        return MorphType.PREFIXATION
    if pat_str.startswith('X_<') and pat_str.endswith('>'):
        return MorphType.SUFFIXATION
    if pat_str.startswith('bX_<') and pat_str.endswith('>_eX'):
        return MorphType.INFIXATION
    return None












