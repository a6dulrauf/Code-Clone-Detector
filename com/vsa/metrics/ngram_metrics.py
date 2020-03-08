# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 13:17:23 2019

@author: ACE
"""

from com.vsa.language_model.ngram.ngram import NGram
from com.vsa.file_handler.file_handler import File_Handler

class NGram_Metrics:

    def __init__(self, n=1):
        self.ngram = NGram()
        self.n = n
        
    def get_n(self):
        return self.n
    
    def run(self, file_path):
        lines=File_Handler.read_file_bi_gram(file_path)
        lines=File_Handler.normalize(lines)
        #print(lines)
        if len(lines) != 0:
            t_words=self.ngram.tokenize(lines)
            n_words=self.ngram.n_gram(t_words,self.n)

            return [self.ngram.frequency(n_words)]