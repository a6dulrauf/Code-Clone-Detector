# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:44:02 2019

@author: Syed Hassan Ali
"""

import abc

class Language_Model:
    
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def tokenize(self,words):
        raise NotImplementedError
        
    @abc.abstractmethod
    def n_gram(self,tokenize_words,n=2):
        raise NotImplementedError
        
        