# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 02:58:37 2019

@author: Syed Hassan Ali
"""

from tkinter import *
from tkinter import ttk

class ScrollFrame(ttk.Frame):
    
    def __init__(self, master):
        Frame.__init__(self,master)
        
        self.vScrollBar = Scrollbar(self, orient='vertical')
        #self.sizeGrip = ttk.Sizegrip(self)
        self.canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.vScrollBar.set)
        
        self.vScrollBar.config(command=self.canvas.yview)
        
    def pack(self):
        
        self.vScrollBar.pack(side=RIGHT, fill=Y, expand=FALSE)
        #self.sizegrip.pack(in_ = self.hscrollbar, side = BOTTOM, anchor = "se")
        self.canvas.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=TRUE)
        Frame.pack(self)
    
    def getFrame(self):
        return self.canvas
        
        