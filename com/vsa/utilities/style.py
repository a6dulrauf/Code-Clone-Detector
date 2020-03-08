# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 04:37:04 2019

@author: Syed Hassan Ali
"""
from tkinter.ttk import *
from com.vsa.utilities.helper import StylingIds

class Styling:
    
    
    def __init__(self):
        self.style=Style()
    
    
    def apply_on_button(self):
        #self.style.configure('btn')
        self.style.map(StylingIds.btn_browse_id, foreground = [('active', '! disabled', 'green')], background = [('active', 'black')]) 
        