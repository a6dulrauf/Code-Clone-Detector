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
    
    def set_on_browse(self, treeview, slot=1, exts='.java'):
        filename = filedialog.askdirectory()
        if not filename:            # dialog cancelled
            return
        if slot == 2:
            self.path2 = filename
        else:
            self.path1 = filename

        dirs = Directory.search_directories(filename, ext=exts)
        self.load_data_in_tv(treeview, dirs)

    def load_data_in_tv(self, treeview, dirs):
        for item in treeview.get_children():
            treeview.delete(item)
        parent_dir = treeview.insert('', text='Selected files', index=1)
        for name in Helper.get_filenames(dirs):
            if name and name.strip():
                treeview.insert(parent_dir, text=name, index=2)
    
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
        