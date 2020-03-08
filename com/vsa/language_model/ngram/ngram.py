# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:29:45 2019

@author: Syed Hassan Ali
"""
from com.vsa.language_model.probability.probability import Probability
import nltk

class NGram:
    
    def __init__(self):
        pass
    
    def list_to_string(self,n_gram_list):
        s=''
        for i in n_gram_list:
            s=s+i+" "
        return s
    
    def tokenize(self,words):
        return nltk.word_tokenize(words)
    
    def n_gram(self,tokenize_words,n=2):
        return nltk.ngrams(tokenize_words,n)
    
    
    def frequency(self,n_gram_words):
        for words in n_gram_words:
            f=nltk.FreqDist(n_gram_words)
        return f
    
        
        
if __name__=="__main__":
    n = NGram()
    t_words = n.tokenize("hope you enjoyed that AI is the new electricity hope you enjoyed that")
    print(t_words)
    f1=n.frequency(t_words)
    #print(f1.__str__,"\n\n\n\n\n")
    bigram=n.n_gram(t_words,2)
    for b in bigram:
        print(b)
    
    #f=n.frequency(bigram)
    
    #print(f.__str__)
    p=Probability()
    print()
    prob=p.calculate_probabilities(f1,f)
    
    
    
       
        