'''
Created on Nov 15, 2018

@author: xh
'''

from enum import Enum

class LanguageCatalog(Enum):
    '''
    '''
    
    Akan = 'aka'
    Hindi = 'hin'
    Hungarian = 'hun'
    Indonesian = 'ind'
    Russian = 'rus'
    Spanish = 'spa'
    Swahili = 'swa'
    Tamil = 'tam'
    Tagalog = 'tgl'
    
    English = 'eng'
    Turkish = 'tur'
    Finnish = 'fin'
    
    Other = 'other'

class Language():
    '''
    Language Meta Information
    '''


    def __init__(self, name, lang_code, consonants={}, vowels={}, alphabet={}, typology = None, lexicon = {}):
        '''
        '''
        self.__name = name
        self.__code = lang_code
        self.__consonants = consonants
        self.__vowels = vowels
        self.__alphabet = alphabet
        self.__typology = typology
        self.__lexicon = lexicon
    
    
    def all_consonants(self):
        return sorted(self.__consonants)
    
    def all_vowels(self):
        return sorted(self.__vowels)
    
    def alphabet_list(self):
        return sorted(self.__alphabet)
    
    def lexical_words(self):
        return sorted(self.__lexicon)
    
    def get_typology(self):
        return self.__typology
    
    def is_vowel(self, ch):
        return ch in self.__vowels
    
    def is_consonant(self, ch):
        return ch in self.__consonants
    
    def is_in_alphabet(self, ch):
        return ch in self.__alphabet
    
    def is_in_lexicon(self, word):
        return word in self.__lexicon
    
    def name(self):
        return self.__name
    
    def filter_alphabetic_words(self, word_list, keep_hyphen=True, keep_apos=True):
        filtered_word_list = []
        for word in word_list:
            is_alphabetic = True
            for i in range(len(word)):
                ch = word[i]
                if i > 0 and i < len(word) - 1 and keep_hyphen and ch == '-':
                    continue
                if ch == '\'' and keep_apos:
                    continue
                if not ch in self.__alphabet:
                    is_alphabetic = False
                    break
            if is_alphabetic:
                filtered_word_list.append(word)
        return filtered_word_list

class English(Language):
    def __init__(self):
        '''
        '''
        name = 'English' 
        lang_code = 'eng'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)

class Turkish(Language):
    def __init__(self):
        '''
        '''
        name = 'Turkish' 
        lang_code = 'tur'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
        
class Finnish(Language):
    def __init__(self):
        '''
        '''
        name = 'Finnish' 
        lang_code = 'fin'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZŠšŽž')
        vowels =  set('aeiouAEIOUÅåÄäÖö')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZÅåÄäÖöŠšŽž')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)

class Akan(Language):
    def __init__(self):
        '''
        '''
        name = 'Akan' 
        lang_code = 'aka'
        consonants = set('bdBDfghkFGHKlmnLMNprsPRStwyTWY')
        vowels =  set('aeAEɛƐiIoOuUɔƆ')
        alphabet = set('abdeABDEɛƐfghikFGHIKlmnLMNoprsOPRStuwyTUWYɔƆ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    

class Hindi(Language):
    def __init__(self):
        '''
        '''
        name = 'Hindi' 
        lang_code = 'hin'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    

class Hungarian(Language):
    def __init__(self):
        '''
        '''
        name = 'Hungarian' 
        lang_code = 'hun'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOUáÁéÉíÍóÓöÖőŐüÜúÚűŰ')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁéÉíÍóÓöÖőŐüÜúÚűŰ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)


class Indonesian(Language):
    def __init__(self):
        '''
        '''
        name = 'Indonesian' 
        lang_code = 'ind'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    

class Russian(Language):
    def __init__(self):
        '''
        '''
        name = 'Russian' 
        lang_code = 'rus'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    

class Spanish(Language):
    def __init__(self):
        '''
        '''
        name = 'Spanish' 
        lang_code = 'spa'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZñÑ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZñÑ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    


class Swahili(Language):
    def __init__(self):
        '''
        Eng - xq
        '''
        name = 'Swahili' 
        lang_code = 'swa'
        consonants = set('bcdfghjklmnprstvwyzBCDFGHJKLMNPRSTVWYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnoprstuvwyzABCDEFGHIJKLMNOPRSTUVWYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    


class Tagalog(Language):
    def __init__(self):
        '''
        '''
        name = 'Tagalog' 
        lang_code = 'tag'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)
    

class Tamil(Language):
    def __init__(self):
        '''
        '''
        name = 'Tamil' 
        lang_code = 'tam'
        consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
        vowels =  set('aeiouAEIOU')
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        typology = None
        super().__init__(name, lang_code, consonants, vowels, alphabet, typology)

class OtherLanguage(Language):
    def __init__(self):
        '''
        '''
        name = 'Other' 
        lang_code = 'na'
        super().__init__(name, lang_code)
    
    def filter_alphabetic_words(self, word_list, keep_hyphen=True, keep_apos=True):
        return list(word_list)
    
def create_language(lang):
    #lang = LanguageCatalog(lang_code)
    if lang == LanguageCatalog.English:
        return English()
    if lang == LanguageCatalog.Turkish:
        return Turkish()
    if lang == LanguageCatalog.Finnish:
        return Finnish()
    if lang == LanguageCatalog.Akan:
        return Akan()
    if lang == LanguageCatalog.Hindi:
        return Hindi()
    if lang == LanguageCatalog.Hungarian:
        return Hungarian()
    if lang == LanguageCatalog.Indonesian:
        return Indonesian()
    if lang == LanguageCatalog.Russian:
        return Russian()
    if lang == LanguageCatalog.Spanish:
        return Spanish()
    if lang == LanguageCatalog.Swahili:
        return Swahili()
    if lang == LanguageCatalog.Tagalog:
        return Tagalog()
    if lang == LanguageCatalog.Tamil:
        return Tamil()
    print('| Warning! Not recognized language: %s' % lang)
    return OtherLanguage()
    































