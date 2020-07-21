'''
Created on Apr 19, 2018

@author: xh
'''

from typology import StemChangeType, StemChangePosition

class _StemChange():
    '''
    Constraints are imposed here:
        Insertion: the char should not be root[indx-1] or root[indx]
        Gemination: the char should be root[indx-1] and not root[indx]
        Deletion: the char should be root[indx] and not root[indx-1] or root[indx+1]
        Degemination: the char should equal to root[indx-1] and root[indx] but not [indx+1]
        Substitution: the char0 should equal to root[indx] and not char1
    Raise error otherwise
    '''

    def __init__(self):
        '''
        '''
    
    def apply_ins(self, root, ch, indx):
        '''
        '''
        if indx < 0 or indx > len(root):
            raise Exception('Insertion index error for root (%s): %s' % (root, indx))
        if (indx > 0 and root[indx-1] == ch) or (indx < len(root) and root[indx] == ch):
            raise Exception('Insertion does not allow the adjacent chars equal to the inserted one: %s' % ch)
        return root[:indx] + ch + root[indx:]
    
    def apply_gem(self, root, ch, indx):
        '''
        '''
        if indx <= 0 or indx > len(root):
            raise Exception('Gemination index error for root (%s): %s' % (root, indx))
        if root[indx-1] != ch:
            raise Exception('Gemination does not apply: root[%s-1] != %s' % (indx, ch))
#         if (indx < len(root) and root[indx] == ch):
#             raise Exception('Gemination does not apply: root[%s] == %s' % (indx, ch))
        return root[:indx] + ch + root[indx:]
    
    def apply_del(self, root, ch, indx):
        '''
        '''
        if indx < 0 or indx >= len(root):
            raise Exception('Deletion index error for root (%s): %s' % (root, indx))
        if root[indx] != ch:
            raise Exception('Deletion does not apply: root[%s] != %s' % (indx, ch))
        if (indx > 0 and root[indx-1] == ch) or (indx < len(root) - 1 and root[indx+1] == ch):
            raise Exception('Deletion does not allow the adjacent chars equal to the deleted one: %s' % ch)
        return root[:indx] + root[indx+1:]
    
    def apply_degem(self, root, ch, indx):
        '''
        '''
        if indx <= 0 or indx >= len(root):
            raise Exception('Degemination index error for root (%s): %s' % (root, indx))
        if root[indx-1] != ch or root[indx] != ch:
            raise Exception('Degemination does not apply: root[{0}-1] != {1} | root[{0}] != {1}'.format(indx, ch))
        if indx < len(root) - 1 and root[indx+1] == ch:
            raise Exception('Degemination does not apply: char %s must be the right most of the same ones' % ch)
        return root[:indx] + root[indx+1:]

    def apply_sub(self, root, ch0, ch1, indx):
        '''
        '''
        if indx < 0 or indx >= len(root):
            raise Exception('Substitution index error for root (%s): %s' % (root, indx))
        if root[indx] != ch0:
            raise Exception('Substitution does not apply: root (%s) [%s] != %s' % (root, indx, ch0))
        if ch0 == ch1:
            raise Exception('Substitution error: ch0 == ch1')
        return root[:indx] + ch1 + root[indx+1:]
    
    def unapply_ins(self, root, ch, indx):
        '''
        '''
        return self.apply_del(root, ch, indx)
    
    def unapply_gem(self, root, ch, indx):
        '''
        '''
        return self.apply_degem(root, ch, indx)
    
    def unapply_del(self, root, ch, indx):
        '''
        '''
        return self.apply_ins(root, ch, indx)

    def unapply_degem(self, root, ch, indx):
        '''
        '''
        return self.apply_gem(root, ch, indx)
        
    def unapply_sub(self, root, ch0, ch1, indx):
        '''
        '''
        return self.apply_sub(root, ch1, ch0, indx)

 
 
    def __index_seg_sub(self, seg, indx):
        r_indx = 0
        for i in range(len(seg)):
            sub_len = len(seg[i])
            if r_indx + sub_len > indx:
                return i, indx - r_indx
            else:
                r_indx += sub_len
        raise Exception('Segment index error: %s' % indx)
     
     
    def apply2seg_sub(self, seg, ch0, ch1, indx):
        '''
        '''
        if ch0 == ch1:
            raise Exception('Substitution error: ch0 == ch1')
        s_indx, c_indx = self.__index_seg_sub(seg, indx)
        seg_i = seg[s_indx]
        if ch0 != seg_i[c_indx]:
            raise Exception('Substitution does not apply to seg: root (%s) [%s] != %s' % (' '.join(seg), indx, ch0))        
        seg_i_1 = seg_i[:c_indx] + ch1 + seg_i[c_indx:]
        return tuple(seg[:s_indx] + (seg_i_1,) + seg[s_indx+1:])
     
class InsChange(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.INS
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.RIGHT_BOUNDARY:
            self.apply = lambda x: self.apply_ins(x, self.__ch, len(x))
            self.unapply = lambda x: self.unapply_ins(x, self.__ch, len(x)-1)
            self.apply2seg = lambda x: tuple(x[:-1]) + (self.apply_ins(x[-1], self.__ch, len(x[-1])),)
            self.unapply2seg = lambda x: tuple(x[:-1]) + (self.unapply_ins(x[-1], self.__ch, len(x[-1])-1),)
        elif self.__pos == StemChangePosition.LEFT_BOUNDARY:
            self.apply = lambda x: self.apply_ins(x, self.__ch, 0)
            self.unapply = lambda x: self.unapply_ins(x, self.__ch, 0)
            self.apply2seg = lambda x: (self.apply_ins(x[0], self.__ch, 0),) + tuple(x[1:])
            self.unapply2seg = lambda x: (self.unapply_ins(x[0], self.__ch, 0),) + tuple(x[1:])
        else:
            raise Exception("For insertion, the position could only be either left or right boundary.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class GemChange(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.GEM
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.RIGHT_BOUNDARY:
            self.apply = lambda x: self.apply_gem(x, self.__ch, len(x))
            self.unapply = lambda x: self.unapply_gem(x, self.__ch, len(x)-1)
            self.apply2seg = lambda x: tuple(x[:-1]) + (self.apply_gem(x[-1], self.__ch, len(x[-1])),)
            self.unapply2seg = lambda x: tuple(x[:-1]) + (self.unapply_gem(x[-1], self.__ch, len(x[-1])-1),)
        elif self.__pos == StemChangePosition.LEFT_BOUNDARY:
            self.apply = lambda x: self.apply_gem(x, self.__ch, 1)
            self.unapply = lambda x: self.unapply_gem(x, self.__ch, 1)
            self.apply2seg = lambda x: (self.apply_gem(x[0], self.__ch, 1),) + tuple(x[1:])
            self.unapply2seg = lambda x: (self.unapply_gem(x[0], self.__ch, 1),) + tuple(x[1:])
        else:
            raise Exception("For gemination, the position could only be either left or right boundary.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class DelChange(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.DEL
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.RIGHT_BOUNDARY:
            self.apply = lambda x: self.apply_del(x, self.__ch, len(x)-1)
            self.unapply = lambda x: self.unapply_del(x, self.__ch, len(x))
            self.apply2seg = lambda x: tuple(x[:-1]) + (self.apply_del(x[-1], self.__ch, len(x[-1])-1),)
            self.unapply2seg = lambda x: tuple(x[:-1]) + (self.unapply_del(x[-1], self.__ch, len(x[-1])),)
        elif self.__pos == StemChangePosition.LEFT_BOUNDARY:
            self.apply = lambda x: self.apply_del(x, self.__ch, 0)
            self.unapply = lambda x: self.unapply_del(x, self.__ch, 0)
            self.apply2seg = lambda x: (self.apply_del(x[0], self.__ch, 0),) + tuple(x[1:])
            self.unapply2seg = lambda x: (self.unapply_del(x[0], self.__ch, 0),) + tuple(x[1:])
        else:
            raise Exception("For deletion, the position could only be either left or right boundary.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch
    

class DegemChange(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.DEGEM
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.RIGHT_BOUNDARY:
            self.apply = lambda x: self.apply_degem(x, self.__ch, len(x)-1)
            self.unapply = lambda x: self.unapply_degem(x, self.__ch, len(x))
            self.apply2seg = lambda x: tuple(x[:-1]) + (self.apply_degem(x[-1], self.__ch, len(x[-1])-1),)
            self.unapply2seg = lambda x: tuple(x[:-1]) + (self.unapply_degem(x[-1], self.__ch, len(x[-1])),)
        elif self.__pos == StemChangePosition.LEFT_BOUNDARY:
            self.apply = lambda x: self.apply_degem(x, self.__ch, 1)
            self.unapply = lambda x: self.unapply_degem(x, self.__ch, 1)
            self.apply2seg = lambda x: (self.apply_degem(x[0], self.__ch, 1),) + tuple(x[1:])
            self.unapply2seg = lambda x: (self.unapply_degem(x[0], self.__ch, 1),) + tuple(x[1:])
        else:
            raise Exception("For degemination, the position could only be either left or right boundary.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class SubChange(_StemChange):
    
    def __init__(self, ch0, ch1, pos):
        '''
        '''
        self.__type = StemChangeType.SUB
        self.__ch0 = ch0
        self.__ch1 = ch1
        self.__pos = pos
        if self.__pos == StemChangePosition.RIGHT_BOUNDARY:
            self.apply = lambda x: self.apply_sub(x, self.__ch0, self.__ch1, len(x)-1)
            self.unapply = lambda x: self.unapply_sub(x, self.__ch0, self.__ch1, len(x)-1)
            self.apply2seg = lambda x: tuple(x[:-1]) + (self.apply_sub(x[-1], self.__ch0, self.__ch1, len(x[-1])-1),)
            self.unapply2seg = lambda x: tuple(x[:-1]) + (self.unapply_sub(x[-1], self.__ch0, self.__ch1, len(x[-1])-1),)
        elif self.__pos == StemChangePosition.LEFT_BOUNDARY:
            self.apply = lambda x: self.apply_sub(x, self.__ch0, self.__ch1, 0)
            self.unapply = lambda x: self.unapply_sub(x, self.__ch0, self.__ch1, 0)
            self.apply2seg = lambda x: (self.apply_sub(x[0], self.__ch0, self.__ch1, 0),) + tuple(x[1:])
            self.unapply2seg = lambda x: (self.unapply_sub(x[0], self.__ch0, self.__ch1, 0),) + tuple(x[1:])
        else:
            raise Exception("For substitution, the position could only be either left or right boundary.")
        self.__key = '%s:%s-%s:%s' % (self.__type.value, self.__ch0, self.__ch1, self.__pos.value)
    
    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch0, self.__ch1

class VowChange(_StemChange):
    '''
    '''
    def __init__(self, ch0, ch1, pos, indx):
        self.__type = StemChangeType.VOW
        self.__ch0 = ch0
        self.__ch1 = ch1
        self.__pos = pos
        if self.__pos == StemChangePosition.RIGHT_VOWEL or self.__pos == StemChangePosition.LEFT_VOWEL:
            self.apply = lambda x: self.apply_sub(x, self.__ch0, self.__ch1, indx)
            self.unapply = lambda x: self.unapply_sub(x, self.__ch0, self.__ch1, indx)
            self.apply2seg = lambda x: self.apply2seg_sub(x, self.__ch0, self.__ch1, indx)
            self.unapply2seg = lambda x: self.apply2seg_sub(x, self.__ch1, self.__ch0, indx)
        else:
            raise Exception("For Vow Change, the position could only be either left or right most vowel at non-boundaries.")
        self.__key = '%s:%s-%s:%s' % (self.__type.value, self.__ch0, self.__ch1, self.__pos.value)
    
        
    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch0, self.__ch1

    
class NonChange(_StemChange):
    
    def __init__(self):
        '''
        '''
        self.__type = StemChangeType.NON
        self.__pos = None
        self.__ch = ''
        self.__key = '$'
        self.apply = lambda x: x
        self.unapply = lambda x: x
        self.apply2seg = lambda x: x
        self.unapply2seg = lambda x: x
    
    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch


class InsChangeInf(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.INS
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.INF_B_RIGHT_BOUNDARY:
            self.apply = lambda b_x, e_x: (self.apply_ins(b_x, self.__ch, len(b_x)), e_x)
            self.unapply = lambda b_x, e_x: (self.unapply_ins(b_x, self.__ch, len(b_x)-1), e_x)
            self.apply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.apply_ins(b_x[-1], self.__ch, len(b_x[-1])),), e_x)
            self.unapply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.unapply_ins(b_x[-1], self.__ch, len(b_x[-1])-1),), e_x)
        elif self.__pos == StemChangePosition.INF_E_LEFT_BOUNDARY:
            self.apply = lambda b_x, e_x: (b_x, self.apply_ins(e_x, self.__ch, 0))
            self.unapply = lambda b_x, e_x: (b_x, self.unapply_ins(e_x, self.__ch, 0))
            self.apply2seg = lambda b_x, e_x: (b_x, (self.apply_ins(e_x[0], self.__ch, 0),) + tuple(e_x[1:]))
            self.unapply2seg = lambda b_x, e_x: (b_x, (self.unapply_ins(e_x[0], self.__ch, 0),) + tuple(e_x[1:]))
        else:
            raise Exception("For insertion with infixation, the position could only be either left boundary of e_root or right boundary of b_root.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)
    
    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class GemChangeInf(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.GEM
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.INF_B_RIGHT_BOUNDARY:
            self.apply = lambda b_x, e_x: (self.apply_gem(b_x, self.__ch, len(b_x)), e_x)
            self.unapply = lambda b_x, e_x: (self.unapply_gem(b_x, self.__ch, len(b_x)-1), e_x)
            self.apply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.apply_gem(b_x[-1], self.__ch, len(b_x[-1])),), e_x)
            self.unapply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.unapply_gem(b_x[-1], self.__ch, len(b_x[-1])-1),), e_x)
        elif self.__pos == StemChangePosition.INF_E_LEFT_BOUNDARY:
            self.apply = lambda b_x, e_x: (b_x, self.apply_gem(e_x, self.__ch, 1))
            self.unapply = lambda b_x, e_x: (b_x, self.unapply_gem(e_x, self.__ch, 1))
            self.apply2seg = lambda b_x, e_x: (b_x, (self.apply_gem(e_x[0], self.__ch, 1),) + tuple(e_x[1:]))
            self.unapply2seg = lambda b_x, e_x: (b_x, (self.unapply_gem(e_x[0], self.__ch, 1),) + tuple(e_x[1:]))
        else:
            raise Exception("For gemination with infixation, the position could only be either left boundary of e_root or right boundary of b_root.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class DelChangeInf(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.DEL
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.INF_B_RIGHT_BOUNDARY:
            self.apply = lambda b_x, e_x: (self.apply_del(b_x, self.__ch, len(b_x)-1), e_x)
            self.unapply = lambda b_x, e_x: (self.unapply_del(b_x, self.__ch, len(b_x)), e_x)
            self.apply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.apply_del(b_x[-1], self.__ch, len(b_x[-1])-1),), e_x)
            self.unapply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.unapply_del(b_x[-1], self.__ch, len(b_x[-1])),), e_x)
        elif self.__pos == StemChangePosition.INF_E_LEFT_BOUNDARY:
            self.apply = lambda b_x, e_x: (b_x, self.apply_del(e_x, self.__ch, 0))
            self.unapply = lambda b_x, e_x: (b_x, self.unapply_del(e_x, self.__ch, 0))
            self.apply2seg = lambda b_x, e_x: (b_x, (self.apply_del(e_x[0], self.__ch, 0),) + tuple(e_x[1:]))
            self.unapply2seg = lambda b_x, e_x: (b_x, (self.unapply_del(e_x[0], self.__ch, 0),) + tuple(e_x[1:]))
        else:
            raise Exception("For deletion with infixation, the position could only be either left boundary of e_root or right boundary of b_root.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class DegemChangeInf(_StemChange):
    
    def __init__(self, ch, pos):
        '''
        '''
        self.__type = StemChangeType.DEGEM
        self.__ch = ch
        self.__pos = pos
        if self.__pos == StemChangePosition.INF_B_RIGHT_BOUNDARY:
            self.apply = lambda b_x, e_x: (self.apply_degem(b_x, self.__ch, len(b_x)-1), e_x)
            self.unapply = lambda b_x, e_x: (self.unapply_degem(b_x, self.__ch, len(b_x)), e_x)
            self.apply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.apply_degem(b_x[-1], self.__ch, len(b_x[-1])-1),), e_x)
            self.unapply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.unapply_degem(b_x[-1], self.__ch, len(b_x[-1])),), e_x)
        elif self.__pos == StemChangePosition.INF_E_LEFT_BOUNDARY:
            self.apply = lambda b_x, e_x: (b_x, self.apply_degem(e_x, self.__ch, 1))
            self.unapply = lambda b_x, e_x: (b_x, self.unapply_degem(e_x, self.__ch, 1))
            self.apply2seg = lambda b_x, e_x: (b_x, (self.apply_degem(e_x[0], self.__ch, 1),) + tuple(e_x[1:]))
            self.unapply2seg = lambda b_x, e_x: (b_x, (self.unapply_degem(e_x[0], self.__ch, 1),) + tuple(e_x[1:]))
        else:
            raise Exception("For degemination with infixation, the position could only be either left boundary of e_root or right boundary of b_root.")
        self.__key = '%s:%s:%s' % (self.__type.value, self.__ch, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch

class SubChangeInf(_StemChange):
    
    def __init__(self, ch0, ch1, pos):
        '''
        '''
        self.__type = StemChangeType.SUB
        self.__ch0 = ch0
        self.__ch1 = ch1
        self.__pos = pos
        if self.__pos == StemChangePosition.INF_B_RIGHT_BOUNDARY:
            self.apply = lambda b_x, e_x: (self.apply_sub(b_x, self.__ch0, self.__ch1, len(b_x)-1), e_x)
            self.unapply = lambda b_x, e_x: (self.unapply_sub(b_x, self.__ch0, self.__ch1, len(b_x)-1), e_x)
            self.apply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.apply_sub(b_x[-1], self.__ch0, self.__ch1, len(b_x[-1])-1),), e_x)
            self.unapply2seg = lambda b_x, e_x: (tuple(b_x[:-1]) + (self.unapply_sub(b_x[-1], self.__ch0, self.__ch1, len(b_x[-1])-1),), e_x)
        elif self.__pos == StemChangePosition.INF_E_LEFT_BOUNDARY:
            self.apply = lambda b_x, e_x: (b_x, self.apply_sub(e_x, self.__ch0, self.__ch1, 0))
            self.unapply = lambda b_x, e_x: (b_x, self.unapply_sub(e_x, self.__ch0, self.__ch1, 0))
            self.apply2seg = lambda b_x, e_x: (b_x, (self.apply_sub(e_x[0], self.__ch0, self.__ch1, 0),) + tuple(e_x[1:]))
            self.unapply2seg = lambda b_x, e_x: (b_x, (self.unapply_sub(e_x[0], self.__ch0, self.__ch1, 0),) + tuple(e_x[1:]))
        else:
            raise Exception("For substitution with infixation, the position could only be either left boundary of e_root or right boundary of b_root.")
        self.__key = '%s:%s-%s:%s' % (self.__type.value, self.__ch0, self.__ch1, self.__pos.value)

    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch0, self.__ch1

class VowChangeInf(_StemChange):
    '''
    '''
    def __init__(self, ch0, ch1, pos, indx):
        self.__type = StemChangeType.VOW
        self.__ch0 = ch0
        self.__ch1 = ch1
        self.__pos = pos
        if self.__pos == StemChangePosition.INF_B_RIGHT_VOWEL:
            self.apply = lambda b_x, e_x: (self.apply_sub(b_x, self.__ch0, self.__ch1, indx), e_x)
            self.unapply = lambda b_x, e_x: (self.unapply_sub(b_x, self.__ch0, self.__ch1, indx), e_x)
            self.apply2seg = lambda b_x, e_x: (self.apply2seg_sub(b_x, self.__ch0, self.__ch1, indx), e_x)
            self.unapply2seg = lambda b_x, e_x: (self.apply2seg_sub(b_x, self.__ch1, self.__ch0, indx), e_x)
        elif self.__pos == StemChangePosition.INF_E_LEFT_BOUNDARY:
            self.apply = lambda b_x, e_x: (b_x, self.apply_sub(e_x, self.__ch0, self.__ch1, indx))
            self.unapply = lambda b_x, e_x: (b_x, self.unapply_sub(e_x, self.__ch0, self.__ch1, indx))
            self.apply2seg = lambda b_x, e_x: (b_x, self.apply2seg_sub(e_x, self.__ch0, self.__ch1, indx))
            self.unapply2seg = lambda b_x, e_x: (b_x, self.apply2seg_sub(e_x, self.__ch1, self.__ch0, indx))
        else:
            pass
        self.__key = '%s:%s-%s:%s' % (self.__type.value, self.__ch0, self.__ch1, self.__pos.value)
    
    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch0, self.__ch1

class NonChangeInf(_StemChange):
    
    def __init__(self):
        '''
        '''
        self.__type = StemChangeType.NON
        self.__pos = None
        self.__ch = ''
        self.apply = lambda b_x, e_x: (b_x, e_x)
        self.unapply = lambda b_x, e_x: (b_x, e_x)
        self.apply2seg = lambda b_x, e_x: (b_x, e_x)
        self.unapply2seg = lambda b_x, e_x: (b_x, e_x)
        self.__key = '$'
    
    def key(self):
        return self.__key
    
    def type(self):
        return self.__type
    
    def pos(self):
        return self.__pos
    
    def ch(self):
        return self.__ch


def parse_schange_key(schange_key):
    if schange_key == '$':
        return StemChangeType.NON
    schange_str = schange_key.split(':')[0]
    try:
        return StemChangeType(schange_str)
    except Exception:
        return None

#----------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------- Test Units -------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

def test_ins():
    print('Insertion-------------------------------------------')
    sub_changes = InsChange('i', StemChangePosition.RIGHT_BOUNDARY), InsChange('k', StemChangePosition.LEFT_BOUNDARY), InsChange('c', StemChangePosition.LEFT_BOUNDARY)
    w = 'car'
    w_seg = ('carr', 'y')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            wc = sub_change.apply(w)
            print(wc)
            print(sub_change.unapply(wc))
            #print(sub_change.unapply(w))
            wc_seg = sub_change.apply2seg(w_seg) 
            print(wc_seg)
            print(sub_change.unapply2seg(wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_gem():
    print('Gemination-------------------------------------------')
    sub_changes = GemChange('p', StemChangePosition.RIGHT_BOUNDARY), GemChange('s', StemChangePosition.LEFT_BOUNDARY), GemChange('n', StemChangePosition.LEFT_BOUNDARY), GemChange('p', StemChangePosition.LEFT_BOUNDARY)
    w = 'sstop'
    w_seg = ('non', 'stop')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            wc = sub_change.apply(w)
            print(wc)
            print(sub_change.unapply(wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            wc_seg = sub_change.apply2seg(w_seg) 
            print(wc_seg)
            print(sub_change.unapply2seg(wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_del():
    print('Substitution-------------------------------------------')
    sub_changes = DelChange('e', StemChangePosition.RIGHT_BOUNDARY), DelChange('s', StemChangePosition.LEFT_BOUNDARY), DelChange('s', StemChangePosition.RIGHT_BOUNDARY), DelChange('e', StemChangePosition.LEFT_BOUNDARY)
    w = 'sserializee'
    w_seg = ('sserial', 'ize', 'e')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            wc = sub_change.apply(w)
            print(wc)
            print(sub_change.unapply(wc))
            #print(sub_change.unapply(w))
        except Exception as ex:
            print(ex)
        try:
            wc_seg = sub_change.apply2seg(w_seg) 
            print(wc_seg)
            print(sub_change.unapply2seg(wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)
    
def test_degem():
    print('Degemination-------------------------------------------')
    sub_changes = DegemChange('p', StemChangePosition.RIGHT_BOUNDARY), DegemChange('s', StemChangePosition.LEFT_BOUNDARY)
    w = 'stopp'
    w_seg = ('ssun', 'stop', 'p')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            wc = sub_change.apply(w)
            print(wc)
            print(sub_change.unapply(wc))
            #print(sub_change.unapply(w))
        except Exception as ex:
            print(ex)
        try:
            wc_seg = sub_change.apply2seg(w_seg) 
            print(wc_seg)
            print(sub_change.unapply2seg(wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_sub():
    #SUB-y-i
    print('Substitution-------------------------------------------')
    sub_changes = SubChange('y', 'i', StemChangePosition.RIGHT_BOUNDARY), SubChange('c', 'k', StemChangePosition.LEFT_BOUNDARY)
    w = 'carry'
    w_seg = ('carr', 'y')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            wc = sub_change.apply(w)
            print(wc)
            print(sub_change.unapply(wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            wc_seg = sub_change.apply2seg(w_seg) 
            print(wc_seg)
            print(sub_change.unapply2seg(wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)
    
def test_ins_inf():
    print('Insertion-------------------------------------------')
    sub_changes = InsChangeInf('i', StemChangePosition.INF_B_RIGHT_BOUNDARY), InsChangeInf('k', StemChangePosition.INF_E_LEFT_BOUNDARY), InsChangeInf('r', StemChangePosition.INF_E_LEFT_BOUNDARY)
    b_w, e_w = 'ca', 'r'
    b_seg, e_seg = ('ca',), ('rr', 'y')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            b_wc, e_wc = sub_change.apply(b_w, e_w)
            print((b_wc, e_wc))
            print(sub_change.unapply(b_wc, e_wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            b_wc_seg, e_wc_seg = sub_change.apply2seg(b_seg, e_seg) 
            print((b_wc_seg, e_wc_seg))
            print(sub_change.unapply2seg(b_wc_seg, e_wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_gem_inf():
    print('Gemination-------------------------------------------')
    sub_changes = GemChangeInf('a', StemChangePosition.INF_B_RIGHT_BOUNDARY), GemChangeInf('r', StemChangePosition.INF_E_LEFT_BOUNDARY), GemChangeInf('o', StemChangePosition.INF_B_RIGHT_BOUNDARY)
    b_w, e_w = 'ca', 'r'
    b_seg, e_seg = ('ca',), ('rr', 'y')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            b_wc, e_wc = sub_change.apply(b_w, e_w)
            print((b_wc, e_wc))
            print(sub_change.unapply(b_wc, e_wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            b_wc_seg, e_wc_seg = sub_change.apply2seg(b_seg, e_seg) 
            print((b_wc_seg, e_wc_seg))
            print(sub_change.unapply2seg(b_wc_seg, e_wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_del_inf():
    print('Deletion-------------------------------------------')
    sub_changes = DelChangeInf('a', StemChangePosition.INF_B_RIGHT_BOUNDARY), DelChangeInf('o', StemChangePosition.INF_E_LEFT_BOUNDARY), DelChangeInf('o', StemChangePosition.INF_B_RIGHT_BOUNDARY)
    b_w, e_w = 'ca', 'r'
    b_seg, e_seg = ('y',), ('ose',)
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            b_wc, e_wc = sub_change.apply(b_w, e_w)
            print((b_wc, e_wc))
            print(sub_change.unapply(b_wc, e_wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            b_wc_seg, e_wc_seg = sub_change.apply2seg(b_seg, e_seg) 
            print((b_wc_seg, e_wc_seg))
            print(sub_change.unapply2seg(b_wc_seg, e_wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_degem_inf():
    print('Degemination-------------------------------------------')
    sub_changes = DegemChangeInf('a', StemChangePosition.INF_B_RIGHT_BOUNDARY), DegemChangeInf('r', StemChangePosition.INF_E_LEFT_BOUNDARY), DegemChangeInf('o', StemChangePosition.INF_B_RIGHT_BOUNDARY)
    b_w, e_w = 'caa', 'ry'
    b_seg, e_seg = ('ca',), ('rr', 'y')
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            b_wc, e_wc = sub_change.apply(b_w, e_w)
            print((b_wc, e_wc))
            print(sub_change.unapply(b_wc, e_wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            b_wc_seg, e_wc_seg = sub_change.apply2seg(b_seg, e_seg) 
            print((b_wc_seg, e_wc_seg))
            print(sub_change.unapply2seg(b_wc_seg, e_wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)

def test_sub_inf():
    print('Substitution-------------------------------------------')
    sub_changes = SubChangeInf('a', 'e', StemChangePosition.INF_B_RIGHT_BOUNDARY), SubChangeInf('r', 'k', StemChangePosition.INF_E_LEFT_BOUNDARY), SubChangeInf('o', 'u', StemChangePosition.INF_B_RIGHT_BOUNDARY)
    b_w, e_w = 'ca', 'ry'
    b_seg, e_seg = ('y',), ('ose',)
    for sub_change in sub_changes:
        print(sub_change.key())
        try:
            b_wc, e_wc = sub_change.apply(b_w, e_w)
            print((b_wc, e_wc))
            print(sub_change.unapply(b_wc, e_wc))
        except Exception as ex:
            print(ex)
        try:
            #print(sub_change.unapply(w))
            b_wc_seg, e_wc_seg = sub_change.apply2seg(b_seg, e_seg) 
            print((b_wc_seg, e_wc_seg))
            print(sub_change.unapply2seg(b_wc_seg, e_wc_seg))
            #print(sub_change.unapply2seg(w_seg))
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    #test_degem()
    #test_ins_inf()
    #test_gem_inf()
    test_del_inf()
    #test_degem_inf()
    #test_sub_inf()





















