# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 00:50:34 2019

@author: Syed Hassan Ali
"""

from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
from com.vsa.dataset_handler.dataset_handler import DatasetHandler
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.elements.features import Features
from com.vsa.utilities.directories import Directory


class Plagiarism_Tester:
    
    
    def __init__(self,file1_path = '' ,file2_path = '' ,ds1_name='d1.csv',ds2_name='d2.csv'):
        
        self.file1_path=file1_path
        self.file2_path=file2_path
        self.ds1_name=ds1_name
        self.ds2_name=ds2_name
        self.feature1 = None
        self.feature2 = None
        
        
    def run_test(self,metrics,plagiarism_technique,is_project=True ,features=[]):
        if not is_project:    
            features = self.make_data_for_test(metrics)
        else:
            features = features
        res = plagiarism_technique.test_palgiarism(features[0],features[1])
        return float(res)
    
    
    def make_data_for_test(self,metrics):
        '''
        Read the source files
        '''
        #halstead=HalsteadMetrics('')
        ds1=metrics.run(self.file1_path)
        ds2=metrics.run(self.file2_path)
        
        '''
        1-pre process data
        2-generate csv of pre-process data
        3-read csv and extract those features which both file contains
        4-make both of them dimensionally equal
        5-
        '''
        
        '''
        '''
        dataset_handler=DatasetHandler()
        data_frames=dataset_handler.pre_process_dataset([ds1,ds2])
        
        '''
        '''
        if type(metrics) is NGram_Metrics:    
            feature = Features.get_feature_combinations(Features.features,metrics.n)
        elif type(metrics) is HalsteadMetrics:
            feature=Features.features
        #feature=Features.features
        #print(feature)
        dataset_dir = Directory.path(str('datasets'))
        dataset_handler.generate_csv([self.ds1_name,self.ds2_name],data_frames,features=feature,address =dataset_dir)#='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\datasets\\')
        '''
        '''
        datasets=dataset_handler.read_csv([self.ds1_name,self.ds2_name],address =dataset_dir)#='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\datasets\\')
  
        #same_features_ds=dataset_handler.extract_same_features(datasets)
        
        #dataset_handler.generate_csv(['same_d1.csv','same_d2.csv'],same_features_ds,'datasets\\same_features\\')
        '''
        '''
        #eq_dim_ds=dataset_handler.get_equal_dim_dataset(same_features_ds)
        
        #print('sdasbdasndbnasbdmbasm',len(datasets))
       
        feature1=[x for x in datasets[0].values]
        feature2=[x for x in datasets[1].values]

        self.feature1=datasets[0]
        self.feature2=datasets[1]
        #print(feature1)
        
        return [feature1,feature2]
    
    
    
        
if __name__=="__main__":

    file1="sample_resource\\Main.java"
    file2="sample_resource\\MDP.java"
    
    
    #file1='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\sample_resource\\Main.java'
        
    p_tester =Plagiarism_Tester(file1,file1)
    plagiarism_technique=CosineDistance()
    #plagiarism_technique=Euclidean_Distance()
    #metrics=HalsteadMetrics()
    metrics=NGram_Metrics(2)
    res=p_tester.run_test(metrics,plagiarism_technique)
    print('Result',res)
    
    s=['S','H','A']
    sr=str(s)+str(s.reverse())
    print(Features.get_feature_combinations(s,2))
    
    
    
    
    
    
    
    
