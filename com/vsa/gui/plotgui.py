
"""
Created on 09 15 2019 7:29 AM

@author = Syed Hassan Ali
"""

from tkinter import *
from com.vsa.gui.plots.plot import Plot
from com.vsa.gui.handler.datahandler import DataHandler
from com.vsa.utilities.messagebox import Messages
from com.vsa.utilities.messagebox import MessageBox

class PlotGUI:

    def __init__(self):
        self.plot=Plot()
    
        self.feature1=None
        self.feature2=None
    
    def openWindow(self):
        
        root=Tk()
        root.geometry('1024x512')
        chartFrame=Frame(root)
        chartFrame.pack(fill=BOTH)
        return [root,chartFrame]
        
    
        
    def draw_hist(self):
    
        #plot.plot_hist(master[1],[1,2,3,5,7])
        
        if self.feature1 is not None and self.feature2 is not None: 
            plot=Plot()
            master=self.openWindow()
            plot.plot_hist(master[1],self.feature1.values[0])
            #frame=Frame(root)
            #frame.pack(fill=BOTH)
            plot.plot_hist(frame,self.feature2.values[0])
            master[0].mainloop()
        #else:
         #   MessageBox.show_message(Messages.warningType,'Please Test Plagiarism.')

    def draw_pie(self):
        
        if self.feature1 is not None and self.feature2 is not None:  
            plot = Plot()
            master = self.openWindow()
            data = DataHandler.pieplot_data(DataHandler,self.feature1,self.feature2)
            plot.plot_pie(master[1],data[0],labels=data[1])
            master[0].mainloop()
        else:
            MessageBox.show_message(Messages.warningType,'Please Test Plagiarism.')


    def draw_plot(self):
        
        if self.feature1 is not None and self.feature2 is not None:  
            plot = Plot()
            master = self.openWindow()
            plot.plot(master = master[1],x1 = self.feature1.keys(),y1=self.feature1.values[0],x2=self.feature2.keys(),y2=self.feature2.values[0])
            master[0].mainloop()
        else:
            MessageBox.show_message(Messages.warningType,'Please Test Plagiarism.')

        
            
    




