# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 12:33:21 2019

@author: Administrator
"""
import numpy as np
import pandas as pd
import math 
import copy

class DatasetHandler:
    
    def __init__(self):
        self.datasets=[]
        self.pre_process_ds=[]
        
    def pre_process_dataset(self,datasets):
        
        self.datasets=datasets
        self.data_frame=[]
        
        for data_set in self.datasets:
            self.data_frame.append(pd.DataFrame(data_set))
       
        for df in self.data_frame:
            for key in df.keys():
               df[key].replace(to_replace=math.nan,value=df[key].mean(),inplace=True)
           
        #self.pre_process_ds=self.data_frame
        
        return self.data_frame
    
    
    def generate_csv(self, file_name, data_frames, address='datasets\\', features=[]):
        
        features_dict = {}
        
        try:
           # for i in range(0,len(data_frames)): 
                
                for feature in features:
                    features_dict[str(feature)] = float(0.0) 

                for j in range(0,len(data_frames)):
                    for key in data_frames[j].columns:
                        
                        if key.__str__().lower() in features_dict.keys():
                            features_dict[key.__str__().lower()] = float(data_frames[j][key][0])
  #                          print(data_frames[j][key][0])
                    
                    df = pd.DataFrame([features_dict])
                    df.to_csv(address+str(file_name[j]))
                                
               # df = [x for x in data_frames[i].columns if x in features_dict.keys()]
               
                #data_frames[i].to_csv(address+str(file_name[i]))
        except Exception as e:
            print(e)
    
    def read_csv(self, file_name, address='datasets\\'):
        pre_process_ds=[]

        print('No of files:', len(file_name))
        try:
            
            for i in range(0,len(file_name)):
                if len(file_name[i].strip())>0:
                    df = pd.read_csv(address+str(file_name[i]))
                    pre_process_ds.append(df)
                    print(address + str(file_name[i]))
        except Exception as e:
            print(e)
        return pre_process_ds
    
    def get_equal_dim_dataset(self,pre_process_ds):
        pre_process_ds=copy.deepcopy(pre_process_ds)
        #print(self.data_frame)
        
        #self.pre_process_ds=np.array(self.pre_process_ds)
        #print('zer0',self.pre_process_ds[0])
        min_val=pre_process_ds[0].shape[1]
        #print('min val',min_val)
        for ds in pre_process_ds:
            if min_val>ds.shape[1]:
                min_val=ds.shape[1]
        #print('before ',self.pre_process_ds)   
        features=[]
        for i in range(len(pre_process_ds)):
            ds=np.array(pre_process_ds[i])
            features.append(ds[1:2,:min_val])
        
        pre_process_ds=features
           # print('after',self.pre_process_ds)
        return pre_process_ds
    
    
    def extract_same_features(self,pre_process_datasets):
        pre_process_ds=copy.deepcopy(pre_process_datasets)
        smaller_index=0
        greater_index=1
        if len(pre_process_ds[0].keys())>len(pre_process_ds[1].keys()):
            smaller_index=1
            greater_index=0
        for key in pre_process_ds[greater_index].keys():
            if key not in pre_process_ds[smaller_index].keys():
               del pre_process_ds[greater_index][key]
               
        for key in pre_process_ds[smaller_index].keys():
            if key not in pre_process_ds[greater_index].keys():
                del pre_process_ds[smaller_index][key]
            
        return pre_process_ds
            
        
        
        
            
    