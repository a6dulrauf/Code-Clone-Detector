# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 07:18:23 2019

@author: Syed Hassan Ali
"""
from tkinter import TOP,BOTH,BOTTOM
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
    


class Plot:
    
    
    def __init__(self):
        self.figure((5,5),100)
        self.canvas=None
    
    def figure(self,size,dpi):
        self.fig=Figure(figsize=size,dpi=dpi)
        #fig.add_subplot(111)
        
    def canvas(self,fig,master,side=TOP):
        if self.canvas is not None:
            return self.canvas
        
        
        
            
    def canvas_draw(self,fig,master,side=TOP):
        self.canvas=FigureCanvasTkAgg(fig,master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM,fill=BOTH,padx=10,pady=10)
    
    def canvas_delete(self):
        self.canvas.get_tk_widget().delete()
    def plot_hist(self,master,data=[]):
        #self.figure(size=(3,3),dpi=100)
        self.fig.add_subplot(111).hist(data)
        self.canvas_draw(self.fig,master=master)
        
    def plot_pie(self,master,data=[],labels=[]):
        #self.figure(size=(3,3),dpi=100)
        self.fig.add_subplot(111).pie(data,labels=labels,autopct='%.2f%%')
        self.fig.legend()
        #self.fig.canvas.mpl_connect()
        
        #self.canvas.SetScrollbar(HORIZONTAL, 0, 5, self.scroll_range)
        self.canvas_draw(self.fig,master=master)
        
    def scatter_plot(self,master,x=[],y=[]):
        self.fig.add_subplot(111).scatter(x,y)
        self.canvas_draw(self.fig,master=master)
    
    def plot(self,master,x1=[],y1=[],x2=[],y2=[]):
        self.fig.add_subplot(111).plot(x1,y1,color='red')
        #self.fig.add_subplot(111).plot(x2,y2,'green')
        self.canvas_draw(self.fig,master=master)
        
    def func(evt):
        
        if legend.contains(evt):
            bbox = legend.get_bbox_to_anchor()
            bbox = Bbox.from_bounds(bbox.x0, bbox.y0+d[evt.button], bbox.width, bbox.height)
            tr = legend.axes.transAxes.inverted()
            legend.set_bbox_to_anchor(bbox.transformed(tr))
            fig.canvas.draw_idle()
            
