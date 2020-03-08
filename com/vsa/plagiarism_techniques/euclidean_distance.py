# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:23:58 2019

@author: Administrator
"""
from scipy.spatial import distance 

class Euclidean_Distance:
    
    
    def __init__(self):
        pass
    
    
    def test_palgiarism(self,dataset_1,dataset_2):
        self.dataset_1=dataset_1
        self.dataset_2=dataset_2
        if self.dataset_1 is not None and self.dataset_2 is not None:
            result=distance.euclidean(self.dataset_1,self.dataset_2)
            return float(result)