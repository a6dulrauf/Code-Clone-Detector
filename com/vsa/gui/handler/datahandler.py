# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:16:05 2019

@author: Syed Hassan Ali
"""

from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.plagiarism_techniques.euclidean_distance import Euclidean_Distance
from com.vsa.plagiarism_tester import Plagiarism_Tester
class DataHandler:
    
    
    def __init__(self):
        
        self.listboxfile1=None
        self.listboxfile2=None
        self.result=None
        self.chartdata=None
        self.plagiarismdata=None
        
        
    def test_plagiarism(self,filepath1,filepath2,isNgram,techStr,n=1):
        if isNgram:    
            metrics = NGram_Metrics(n)
        else:
            metrics = HalsteadMetrics()
        
        if techStr == 'cosine':
            tech = CosineDistance()
        else:
            tech = Euclidean_Distance()
        
        tester = Plagiarism_Tester(filepath1,filepath2)
        res=tester.run_test(metrics,tech)
        return res*100 
        
        
        
    def pieplot_data(self,feature1,feature2):
        data=[]
        keys=[]
        for key in feature1.keys():     
            if key in feature2.keys():
                if feature1[key][0] != 0 and feature2[key][0] != 0:
                    keys.append(key)
                    data.append(feature2[key][0]/feature1[key][0])
        return [data,keys]
        


