# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:53:19 2019

@author: Administrator
"""
from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
from dataset_handler.dataset_handler import DatasetHandler
from plagiarism_techniques.cosine_distance import CosineDistance

import numpy as np
'''
if __name__=='__main__':
    try:
        halstead=HalsteadMetrics('C:\\Users\\Administrator\\Desktop\\Test.java');
       # halstead.calculate_metrics();
        #print(halstead._operators)
       # print(halstead.get_all_operators())
        print('\n\n\n')
        #print(halstead.readFile())
        dataset1=halstead.run_halstead('C:\\Users\\Syed Hassan Ali\eclipse-workspace\LOCMetrics\\src\\metrics\\LOCMetrics.java')
        dataset2=halstead.run_halstead('C:\\Users\\Syed Hassan Ali\eclipse-workspace\LOCMetrics\\src\\metrics\\LOCMetrics.java')
       # print('Dataset\n',dataset1)
        dataset_handler=DatasetHandler()
        
        #dataset_handler.datasets=[dataset1,dataset2]
        dataset_handler.pre_process_dataset([dataset1,dataset2])
        dataset_handler.generate_csv(['d1.csv','d2.csv'])
        
        dataset_handler.read_csv(['d1.csv','d2.csv'])
        
        pre_ds=dataset_handler.get_equal_dim_dataset()
        
        d1=[x for x in pre_ds[0]]
        d2=[x for x in pre_ds[1]]
        
        cosine_d=CosineDistance(d1,d2)
        res=cosine_d.test_palgiarism()
        print('Plagiarism ',res)
        #print('Result',pre_ds)
        #print('DS',dataset_handler.pre_process_ds[0][0])
        
        
    except Exception as e:
        print(e)
        
    '''