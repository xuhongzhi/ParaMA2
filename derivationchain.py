'''
Created on Apr 6, 2018

@author: xh
'''
from typology import MorphType
from morphprocess import Automic

class DerivationNode():
    '''
    A graph node
    '''
    
    def __init__(self, word, parent_node=None, proc=None):
        self.__word = word
        self.__parent_node = parent_node  # word's root
        self.__proc = proc
        self.__child_nodes = []           # list of words that has this word as root
    
    def add_child(self, child_node):
        self.__child_nodes.append(child_node)
    
    def remove_child(self, child_node):
        self.__child_nodes.remove(child_node)
    
    def set_parent(self, parent_node, proc):
        self.__parent_node = parent_node
        self.__proc = proc
    
    def parent(self):
        return self.__parent_node
    
    def word(self):
        return self.__word
    
    def proc(self):
        return self.__proc
    
    def is_root(self):
        return not self.__parent_node
    
    def is_leaf(self):
        return not self.__child_nodes
    
    def children(self):
        return self.__child_nodes


class DerivationChain():
    '''
    Create chains of derivational relations between words, which together form a big tree
    '''
    
    
    def __init__(self, word_root_procs):
        '''
        Constructor
        '''
        self.__word_root_procs = word_root_procs
        self.__create()
        self.__cut_circles()
        self.__organize()
        self.__get_derivation_chain_groups()
        self.__get_chain_length_dist()
    
    def __create(self):
        word_node_indx = {}
        for word, (root, proc) in self.__word_root_procs:
            # Automatic words
            if word == root or proc.morph_type() == MorphType.AUTOMATIC:
                if not word in word_node_indx:
                    word_node = DerivationNode(word)
                    word_node_indx[word] = word_node
                continue
            #
            if root in word_node_indx:
                root_node = word_node_indx[root]
            else:
                root_node = DerivationNode(root)
                word_node_indx[root] = root_node
            if word in word_node_indx:
                word_node = word_node_indx[word]
                word_node.set_parent(root_node, proc)
            else:
                word_node = DerivationNode(word, root_node, proc)
                word_node_indx[word] = word_node
            root_node.add_child(word_node)
        self.__word_node_indx = word_node_indx 
    
    def __cut_circles(self):
        for _word, word_node in self.__word_node_indx.items():
            if word_node.is_root():
                continue
            if word_node.is_leaf():
                continue
            node = word_node
            chain = []
            #-------------debug only-----------
            chain_words = set()
            #-------------debug only-----------
            found_circle = False
            while node:
                if node.word() in chain_words:
                    found_circle = True
                    break
                chain_words.add(node.word())
                chain.append(node)
                node = node.parent()
            if found_circle:
                root_node = chain[0]
                for node in chain[1:]:
                    if len(node.word()) <= len(root_node.word()) and len(node.children()) >= len(root_node.children()):
                        root_node = node
                root_node.parent().remove_child(root_node)
                root_node.set_parent(None, None)
    
    def __organize(self):
        leaf_nodes = {}
        root_nodes = {}
        mid_nodes = {}
        automic_nodes = {}
        for word, word_node in self.__word_node_indx.items():
            if word_node.is_root() and word_node.is_leaf():
                automic_nodes[word] = word_node
                continue
            if word_node.is_root():
                root_nodes[word] = word_node
                continue
            if word_node.is_leaf():
                leaf_nodes[word] = word_node
                continue
            mid_nodes[word] = word_node
        self.__leaf_nodes = leaf_nodes
        self.__root_nodes = root_nodes
        self.__mid_nodes = mid_nodes
        self.__automic_nodes = automic_nodes
    
        
    def __get_derivation_chain(self, word):
        if not word in self.__word_node_indx:
            return []
        word_node = self.__word_node_indx[word]
        node = word_node
        chain = []
        #-------------debug only-----------
        chain_words = set()
        #-------------debug only-----------
        while node:
            if node.word() in chain_words:
                print('Chain circle found!! (%s) + %s' % (', '.join([cnode.word() for cnode in chain]), node.word()))
                break
            chain_words.add(node.word())
            chain.append(node)
            node = node.parent()
        return chain
    
    def __get_derivation_chain_groups(self):
        chain_pat_groups = {}
        for word in self.__leaf_nodes:
            chain_nodes = self.__get_derivation_chain(word)
            word_chain = []
            change_chain = []
            pat_chain = []
            for node in chain_nodes:
                word_chain.append(node.word())
                proc = node.proc()
                if proc:
                    pat_chain.append(proc.pat())
                    change_chain.append(proc.change_key())
            pat_chain_tup = tuple(pat_chain)
            if pat_chain_tup in chain_pat_groups:
                chain_pat_groups[pat_chain_tup].append(tuple(zip(word_chain, change_chain)))
            else:
                chain_pat_groups[pat_chain_tup] = [tuple(zip(word_chain, change_chain))]
        self.__chain_pat_groups = chain_pat_groups
    
    def __get_chain_length_dist(self):
        chain_length_dist = {}
        for word in self.__leaf_nodes:
            chain_nodes = self.__get_derivation_chain(word)
            chain_len = len(chain_nodes)
            if chain_len in chain_length_dist:
                chain_length_dist[chain_len] += 1
            else:
                chain_length_dist[chain_len] = 1
        sorted_chain_len_dist = sorted(chain_length_dist.items(), key=lambda x: x[0])
        self.__chain_len_dist = sorted_chain_len_dist

    def get_derivation_chain_pats(self, word):
        if not word in self.__word_node_indx:
            return []
        word_node = self.__word_node_indx[word]
        node = word_node
        chain = []
        while node.parent():
            chain.append(node.proc().pat())
            node = node.parent()
        return chain
    
    def get_segmentation(self, word):
        '''
        Algorithm:
            Creating Index:
            -------------------------------------------------------
            word: m a g k u m a k a i n    # mag-
            indx: 0 1 2 3 4 5 6 7 8 9 10   # mag-<root>
            root:       k u m a k a i n    # -um-
                        0 1 2 3 4 5 6 7    # <root[0,0+1]>-um-<root[1,5+1]>
            root:       k     a k a i n    # bX_X
                        0     1 2 3 4 5    # <RED-root[0,1+1]>-<root>
            root:             k a i n      # X
                              0 1 2 3
            -------------------------------------------------------
            word: s t o p p i n g          # DUP-p, -ing
            indx: 0 1 2 3 4 5 6 7          # <root:DUP-root[3]>-ing
            root: s t o p
                  0 1 2 3
            -------------------------------------------------------
            word: c a r r i e d           # SUB-y-i, -ed
            indx: 0 1 2 3 4 5 6           # <root:SUB-root[4]-4>-ed
            root: c a r r y
                  0 1 2 3 4
            -------------------------------------------------------
            word: s e r i a l i z   i n g   # DEL-3, -ing
            indx: 0 1 2 3 4 5 6 7   8 9 10  # <root:DEL-root[8]>-ing
            root: s e r i a l i z e         # -ize
                  0 1 2 3 4 5 6 7 8         # <root>-ize
            root: s e r i a l
                  0 1 2 3 4 5
            -------------------------------------------------------
            seg(w) = w | proc(w, seg(r)) | comp(w, seg(r1), seg(r2))
            proc(w, r) = suf(w, r) | pref(w, r) | inf(w, r) | red(w, r) | red_lp(w, r) | red_rp(w, r) | tpl(w, r)
            suf(w, r) = stem_change(r)-<suf>
            pref(w, r) = <pref>-stem_change(r)
            inf(w, r) = stem_change(b_r)-<inf>-stem_change(e_r)
            red(w, r) = stem_change_1(r)-stem_change_2(r)
            red_lp(w, r) = b(r)-stem_change(r)
            red_rp(w, r) = stem_change(r)-e(r)
            tpl(w, r) = con(r)[0]-vow(r)[0]-...-con(r)[n]-vow(r)[n]
            comp(w, r1, r2) = stem_change_1(r1)-stem_change_2(r2)
        '''
        if not word in self.__word_node_indx:
            proc = Automic()
            word_seg = (word,)
            root_seg = word_seg
            return word_seg, [('__'.join(root_seg), proc.pat(), proc.change_key())]
        word_node = self.__word_node_indx[word]
        root_node = word_node.parent()
        if not root_node:
            proc = Automic()
            word_seg = (word,)
            root_seg = word_seg
            return word_seg, [('__'.join(root_seg), proc.pat(), proc.change_key())]
        try:
            root_seg, components = self.get_segmentation(root_node.word())
            component =  ('__'.join(root_seg), word_node.proc().pat(), word_node.proc().change_key())
            components_1 = components.copy()
            components_1.append(component)
            return word_node.proc().apply2seg(root_seg), components_1
        except Exception as ex:
            #print('components: %s' % (str(components)))
            print('word(%s): root_seg(%s): %s' % (word, ' '.join(root_seg), word_node.proc().pat()))
            print(ex)
            #raise Exception(ex)
            proc = Automic()
            word_seg = (word,)
            root_seg = word_seg
            return word_seg, [('__'.join(root_seg), proc.pat(), proc.change_key())]
            
    
    def print_statistics(self):
        print('-------------Derivational Chain Statistics------------')
        print('Automatic roots: %s' % (len(self.__automic_nodes)))
        print('Non-automic root nodes: %s' % (len(self.__root_nodes)))
        print('Leaf nodes: %s' % (len(self.__leaf_nodes)))
        print('Middle nodes: %s' % (len(self.__mid_nodes)))
        print('Chain Length Distribution:')
        for chain_len, freq in self.__chain_len_dist:
            print(' Length %s: %s' % (chain_len, freq))
    
    def save_chain_groups(self, outfile):
        fouts_len = {}
        sorted_chain_pat_groups = sorted(self.__chain_pat_groups.items(), key=lambda x: -len(x[1]))
        for chain_pat_tup, word_change_list in sorted_chain_pat_groups:
            chain_len = len(chain_pat_tup)
            if chain_len in fouts_len:
                fout = fouts_len[chain_len]
            else:
                fout = open(outfile + '_len%s.txt' % (chain_len), 'w', -1, 'utf-8')
                fouts_len[chain_len] = fout
            fout.write('Chain: (%s) (count: %s)\n' % (', '.join(chain_pat_tup), len(word_change_list)))
            fout.write('-------------------------------------------------\n')
            for word_changes in word_change_list:
                chain_str = ' '.join(['(%s, %s)' % (word, change) for word, change in word_changes])
                fout.write(' %s\n' % chain_str)
            fout.write('-------------------------------------------------\n')
        fout.close()
    






















