# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 03:38:45 2019

@author: Syed Hassan Ali
"""
from com.vsa.dataset_handler.dataset_handler import DatasetHandler
from com.vsa.multiple_files.csv_generator import CSVGenerator
from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.utilities.directories import Directory

class ProjectClone:

    def __init__(self):
        pass
    
    def test_project_clone(self, file_names, dirs, metrics, tech, username):
        tester = Plagiarism_Tester()
        dataset_handler = DatasetHandler()

        self.generate_csvs(file_paths=dirs, username=username, metrics=metrics)

        file_paths = [Directory.get_directory_of('com/vsa/datasets/'+username+'/project1'),
                      Directory.get_directory_of('com/vsa/datasets/'+username+'/project2')]

        df_projects = []
        for i in range(0, len(file_paths)):
            df_projects.append(dataset_handler.read_csv(file_name=[file_names[i]], address=file_paths[i]))

        feature1 = [x for x in df_projects[0][0].values]
        feature2 = [x for x in df_projects[1][0].values]

        res = tester.run_test(metrics=metrics, plagiarism_technique=tech,
                              features=[feature1, feature2], is_project=True)

        self.features = [df_projects[0][0], df_projects[1][0]]

        return res

    def generate_csvs(self, username, file_paths, metrics):

        CSVGenerator.generate_multiples_csv(file_paths[0], metrics, username=username)
        CSVGenerator.generate_multiples_csv(file_paths[1], metrics, username=username, project_no=2)

        CSVGenerator.merge_all_csvs(Directory.get_directory_of('com/vsa/datasets/'+username+'/multiple_csv_project1'),
                                    username=username)
        CSVGenerator.merge_all_csvs(Directory.get_directory_of('com/vsa/datasets/'+username+'/multiple_csv_project2'),
                                    username=username, project_no=2)







    
    