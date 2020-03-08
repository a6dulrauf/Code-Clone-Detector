# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 23:53:07 2019

@author: Syed Hassan Ali
"""
import pandas as pd
from com.vsa.dataset_handler.dataset_handler import DatasetHandler
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.elements.features import Features
from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
from com.vsa.utilities.directories import Directory

class CSVGenerator:
    
    '''
    def __init__(self):
        pass
    
    '''    
    
    @staticmethod
    def generate_multiples_csv(dirs, metrics, username, project_no=1, web=False):

        file_path = Directory.search_directories(dirs, '.java')
        dataset_handler = None

        filenames=[]

        if dataset_handler is None:
            dataset_handler = DatasetHandler()
        datasets = []

        for path in file_path:
            if len(path.strip()) > 0:
                p = path.replace('/', '\\')
                datasets.append(metrics.run(p))
                name = p.split('\\')[len(p.split('\\'))-1].replace('.java', '.csv')
                if name.strip() != "":
                    filenames.append(name)#f.replace('.java','.csv'))

            #filenames=['a.csv','b.csv','d.csv','c.csv','e.csv']

        dataframes = dataset_handler.pre_process_dataset(datasets)
        feature = Features.features
        if type(metrics) is NGram_Metrics:    
            feature = Features.get_feature_combinations(Features.features, metrics.n)
        elif type(metrics) is HalsteadMetrics:
            feature = Features.features
        if project_no == 1:
            dataset_handler.generate_csv(file_name=filenames, data_frames = dataframes, address=Directory.get_directory_of('com/vsa/datasets/'+username+'/multiple_csv_project1'), features=feature)
        elif project_no == 2:
            dataset_handler.generate_csv(file_name=filenames, data_frames = dataframes, address=Directory.get_directory_of('com/vsa/datasets/'+username+'/multiple_csv_project2'), features=feature)

    @staticmethod  
    def merge_all_csvs(path, username, project_no=1, web=False):
        
        dirs = Directory.search_directories(path, '.csv')
        dataset_handler = DatasetHandler()
        #print(dirs)
        name = [x.split('\\')[len(x.split('\\'))-1] for x in dirs]
        print(name)
        dfs=dataset_handler.read_csv(file_name=name, address=path)
        
        values = {}
        for key in dfs[0].columns:
            val = 0
            #values.append([])
            for df in dfs:
                if key in df.columns:
                   #print(df[key])
                    val = val + df[key].values[0]
                    #print(df[key])
            
            values[key] = val
            
        #print(values)
        df = pd.DataFrame([values])
        if project_no == 1:    
            df.to_csv(Directory.get_directory_of('com/vsa/datasets/'+username+'/project1')+'project1.csv')
        elif project_no == 2:
            df.to_csv(Directory.get_directory_of('com/vsa/datasets/'+username+'/project2')+'project2.csv')
     
    