# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 04:45:17 2019

@author: Syed Hassan Ali
"""

class Helper:
    
    def __init__(self):
        pass
    
    
    fontstyle='Century gothic'
    fontstylebold='Century gothic bold'
    headingfontsize=14
    buttonfontsize=10
    resultfontsize=20
    mainheading_label_size=18
    
    buttonforecolor=''
    
    
    histogram='Histogram'
    barchart='BarChart'
    piechart='PieChart'
    plot='Plot'
    scatter='ScatterPlot'
    note='Note: The plagiarism will\n be tested of source\nfile 2 with file 1.\nSo make sure to \nselect the right order '
    note=''
    
    filenames=None
    
    dir1_filenames = None
    
    def change_filenames(src1,src2):
        global filenames
        if filenames is not None:
            if filenames[0] is not None:
                src1['text']='Source file 1: '+filenames[0]
            if filenames[1] is not None:
                src2['text']='Source file 2: '+filenames[1]
                
                
    def get_filenames(dirs):
        name = [x.split('\\')[len(x.split('\\'))-1] for x in dirs]
        return name
        
class StylingIds:
    
    btn_browse_id = 'btn_browser'
    btn_browse_id = 'btn_test'