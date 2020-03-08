# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:49:47 2019

@author: Syed Hassan Ali
"""

import math

class Probability:
    
    
    def __init__(self):
        pass
    
    
    def conditional_probability(self,tokenize_words,n_gram_words):
        p={}
        i=n_gram_words[0][1]
        i_1=n_gram_words[0][0]
        p[(i,i_1)]=n_gram_words[1]/tokenize_words[1]
        return p
        
        
    def calculate_probabilities(self,tokenize_words,n_gram_words):
        p=[]
        for key,val in n_gram_words.items():
            if key[0] in tokenize_words.keys():
                p.append(self.conditional_probability([key[0],tokenize_words[key[0]]],[key,val]))
                
        return p        
        
    