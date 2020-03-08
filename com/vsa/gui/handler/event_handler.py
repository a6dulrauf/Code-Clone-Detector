# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:48:11 2019

@author: Syed Hassan Ali
"""

from tkinter import filedialog

from com.vsa.gui.handler.datahandler import DataHandler
from com.vsa.utilities.helper import Helper
from com.vsa.utilities.directories import Directory
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.gui.internal_clone_gui import InternalCloneGUI


class EventHandler:
    
    def __init__(self):
        self.datahandler=DataHandler()
        self.path1=None
        self.path2=None
    
    def set_on_browse(self,treeview):
        filename=filedialog.askdirectory()
        #path=os.path.abspath(filename.__name__)

        if self.path1 is None and filename is not None:
            self.path1=filename
        elif filename is not None:    
            self.path2=filename
        
        #print(type(filename))
        #if isinstance(filename, str):
        #if type(filename) == 'str':
         #   print(filename)
          #  self.path1 = filename
            #Directory.search_directories()
        #else:
         #   print('asdas')
        #Helper.filenames=self.__str__()
       # filename=['D:\\SchoolData\\Summer -18\\Data Structures & Algorithms\\Projects\\NeuralNetwork\\NeuralNetwork\\src\\domain\\NeuralNetwork.java']
        
        dirs=Directory.search_directories(filename,ext = '.java')
        
       # print(dirs)
        m = NGram_Metrics()
        #CSVGenerator.generate_multiples_csv(file_path=dirs, metrics=m)
        self.load_data_in_tv(treeview,dirs)
        
        f='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\datasets\\'
        #CSVGenerator.merge_all_csvs(f)
    
    def load_data_in_tv(self,treeview,dirs):
        names=Helper.get_filenames(dirs)
        print(names)
        treeview.heading('#0',text = 'Project 1  Directory')
        parent_dir = treeview.insert('',text = 'Project 1' ,index = 1)
        
        for name in names:
            #if len(name.strip())>0:
                treeview.insert(parent_dir,text = name ,index = 2)
    
    def set_on_plagiarism_test(self):
        pass
    
    def set_on_internal_clone(self, project_no):    
        internal_clone_gui = InternalCloneGUI(project_no = project_no) 
    
    def __str__(self):
        name1 = name2 = None
        if self.path1 is not None:
            name1=self.path1.split('/')[len(self.path1.split('/'))-1]
        if self.path2 is not None:
            name2=self.path2.split('/')[len(self.path2.split('/'))-1]
        return [name1, name2]
        