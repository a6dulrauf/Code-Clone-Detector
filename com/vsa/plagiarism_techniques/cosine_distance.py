# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 12:27:38 2019

@author: Administrator
"""

from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity


class CosineDistance:
    
    
    def __init__(self):
        pass
    
        
    def test_palgiarism(self,data_set1,data_set2):
        self.data_set1=data_set1
        self.data_set2=data_set2
        if self.data_set1!= None and self.data_set2 != None:
            #print(self.data_set1)
            #result = 1 - spatial.distance.cosine(self.data_set1,self.data_set2)
            result=cosine_similarity(self.data_set1,self.data_set2)
            return float(result)