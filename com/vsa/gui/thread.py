# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 04:59:30 2019

@author: Syed Hassan Ali
"""

import threading

class CustomThread(threading.Thread):
    
    def __init__(self):
        super(CustomThread,self).__init__()
        self.stop_event=threading.Event()
    def stop(self):
        self.stop_event.set()
        
    def is_stop(self):
        self.stop_event.is_set()
        
    def start(self):
        self.start()
        
    
    
