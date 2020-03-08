# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 04:09:04 2019

@author: Syed Hassan Ali
"""

from tkinter import *
from com.vsa.projects_cloning.internal_clone.internal_clone import InternalClone
from com.vsa.utilities.helper import Helper
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from tkinter import ttk
from com.vsa.gui.scroll_frame.scroll_frame import ScrollFrame

class InternalCloneGUI:
    
    def __init__(self, project_no , width='900', height='600'):
        self.project_no = project_no
        self.root = Tk()
        self.root.geometry(width+str('x')+height)
        self.internalClone = InternalClone()
        self.initialize_frames(self.root)
        self.place_heading_label(self.mainFrame)
        
        self.place_scrollbar_mainFrame(self.tableFrame)
        self.test_internal_clone(self.scrollFrame)
        #self.place_scrollbar_mainFrame(self.tableFrame)
        
        self.root.mainloop()
    
    def initialize_frames(self,root):
        self.mainFrame = Frame(root)
        
        #self.canvas = Canvas(self.mainFrame)
        self.tableFrame = ScrollFrame(self.mainFrame) 
        self.tableFrame.pack()
        self.mainFrame.pack()
        
    def place_heading_label(self,master):
        frame = Frame(master)
        label = Label(frame, text = 'INNER PROJECT CLONE',font = (Helper.fontstylebold,Helper.mainheading_label_size))
        frame.pack(expand=YES,fill=BOTH)
        label.pack(expand=YES)
        
    def place_scrollbar_mainFrame(self,master):
        self.scrollFrame = Frame(self.tableFrame.getFrame())
        
        '''
        
        scrollBar = Scrollbar(master, orient = 'vertical', command = self.canvas.yview)
        self.canvas.create_window(0,0,anchor='w', window = master)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand = scrollBar.set)
        self.canvas.pack(fill='both', expand=YES,side='left')
        scrollBar.pack(fill= 'y',side = RIGHT)
        '''
        self.scrollFrame.pack(padx=15, pady=15, expand=TRUE, fill=BOTH)
        
    def create_table_treeview(self,master):

        frame = Frame(master)
        tv=ttk.Treeview(frame)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(Helper.fontstylebold, Helper.buttonfontsize))
        tv['columns'] = ('feature', 'frequency')
        tv.heading("#0", text='S.No', anchor='w')
        tv.column('#0', anchor='w')
        tv.heading("feature", text='Feature')
        tv.column('feature', anchor='center')
        tv.heading("frequency", text='Frequency')
        tv.column('frequency', anchor='center')           
                   
        #tv.grid(sticky=(N,S,W,E))
        
        scrollbar=Scrollbar(frame,orient='vertical',command=tv.yview)
        
        tv.configure(yscrollcommand=scrollbar.set)
        tv.pack(side=LEFT, expand=YES)
        
        scrollbar.pack(side=LEFT,expand=YES,fill=Y)
        frame.pack(side=TOP,expand=YES)
        return tv
    
    def load_tabledata(self,tv,data):
        i=0
        style = ttk.Style()
        
        for key in data.keys():
            i= i+1
            
            style.configure("Treeview.Column", font=(Helper.fontstylebold, Helper.buttonfontsize))
            tv.insert('','end',text=i,values=(key,data[key][0]))
    
    def test_internal_clone(self,master):
        path = None
        if self.project_no == 1:
            path = 'C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\multiple_csv_project1\\'
        elif self.project_no ==2:
            path = 'C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\multiple_csv_project2\\'
            
        result_dict = self.internalClone.test_internal_clone(path,CosineDistance())
        i = 0
        for res in result_dict:
            if res != 'dfs' and res != 'dfsnames':
                label = Label(master, text=str(res)+"  "+str(result_dict[res])+"%", font = (Helper.fontstylebold, Helper.headingfontsize))
                label.pack(side=TOP)
                
                tv = self.create_table_treeview(master)
                if i < len(result_dict['dfs']):    
                    self.load_tabledata(tv,result_dict['dfs'][i])
                i = i + 1

if __name__ == "__main__":
    InternalCloneGUI(1)        
            
    
    
