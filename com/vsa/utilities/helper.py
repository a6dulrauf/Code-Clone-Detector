# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 04:45:17 2019

@author: Syed Hassan Ali
"""

class Helper:
    
    def __init__(self):
        pass
    
    
    # Typography — macOS/Linux-safe families (Tk falls back gracefully)
    fontstyle='Helvetica Neue'
    fontstylebold='Helvetica Neue'
    monofont='Menlo'
    headingfontsize=13
    buttonfontsize=11
    resultfontsize=34
    mainheading_label_size=20

    buttonforecolor=''

    # Brand palette (matches the web app)
    INK='#0C0F1A'
    PAPER='#F4F5F7'
    SURFACE='#FFFFFF'
    MUTED='#59606E'
    LINE='#E5E8EF'
    BRAND='#4F46E5'
    BRAND_INK='#3A32C4'
    MATCH='#059669'
    
    
    histogram='Histogram'
    barchart='BarChart'
    piechart='PieChart'
    plot='Plot'
    scatter='ScatterPlot'
    note='No code handy? Browse the bundled demo projects:\nsamples/demo-projects/project-a  and  project-b'
    
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
        import os
        return [os.path.basename(x) for x in dirs]
        
class StylingIds:
    
    btn_browse_id = 'btn_browser'
    btn_browse_id = 'btn_test'