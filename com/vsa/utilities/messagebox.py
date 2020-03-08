# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 04:34:17 2019

@author: Syed Hassan Ali
"""
from tkinter import messagebox
class Messages:
    
    infoType='Info'
    warningType='Warning'
    errorType='Error'

class MessageBox:
    
    
    def __init__(self):
        pass
    
    
    def show_message(msgType,msg):
        if msgType is Messages.infoType:    
            messagebox.showinfo(title=msgType,message=msg)
        elif msgType is Messages.errorType:
            messagebox.showerror(title=msgType,message=msg)
        elif msgType is Messages.warningType:
            messagebox.showwarning(title=msgType,message=msg)
        