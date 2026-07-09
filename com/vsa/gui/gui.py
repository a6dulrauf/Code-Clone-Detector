# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 01:27:25 2019

@author: Syed Hassan Ali
"""

import os
import time as t

from tkinter import *

from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


from com.vsa.gui.libraries import tktable
#from com.vsa.gui.plots.plot import Plot
from com.vsa.gui.handler.event_handler import EventHandler
#from com.vsa.gui.handler.datahandler import DataHandler
from com.vsa.utilities.helper import Helper
from com.vsa.gui.plotgui import PlotGUI
from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.elements import languages
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.plagiarism_techniques.euclidean_distance import Euclidean_Distance
from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.gui.thread import CustomThread
from com.vsa.multiple_files.csv_generator import CSVGenerator
from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
from com.vsa.utilities.directories import Directory
from com.vsa.dataset_handler.dataset_handler import DatasetHandler

class GUI:

    def __init__(self):
        self.eventhandler=EventHandler()
        #self.datahandler=DataHandler()
        #self.plot=Plot()
        self.root=Tk()
        self.root.geometry('1180x820')
        self.root.minsize(1000, 740)
        self.root.resizable(1,1)
        self.root.title('Code Clone Detector')
        self._setup_theme()
        self.mainFrame=Frame(self.root, bg=Helper.PAPER)
        
        self.mainFrame.pack(expand=YES,fill=BOTH,pady=5)
        
        self.initFrames(self.mainFrame)
        self.plotGui = PlotGUI()
        self.initGUI()
        #plot=Plot()
        #plot.plot_pie(data=[1,2,3,4],labels=['A','B','C','D'],master=self.bottomframe)      
        #self.create_tester_gui()
        #self.create_menubar()
        self.mainFrame.configure(background=Helper.PAPER)
        
        self.root.attributes('-alpha',1)
        
        #self.root.configure(background='black')
        self.root.mainloop()
        #self.filename=filedialog.askopenfile()
        
        
    def _setup_theme(self):
        """Apply a modern, cohesive look: recolor classic Tk widgets via the
        palette, and style ttk widgets (tables + accent button) via the clam theme."""
        self.root.configure(bg=Helper.PAPER)
        try:
            self.root.tk_setPalette(background=Helper.PAPER, foreground=Helper.INK,
                                    activeBackground=Helper.LINE, activeForeground=Helper.INK)
        except Exception as e:
            print(e)
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception as e:
            print(e)
        self.style.configure('Accent.TButton', background=Helper.BRAND, foreground='#FFFFFF',
                             font=(Helper.fontstyle, Helper.buttonfontsize, 'bold'),
                             borderwidth=0, relief='flat', padding=(16, 10))
        self.style.map('Accent.TButton',
                       background=[('active', Helper.BRAND_INK), ('pressed', Helper.BRAND_INK)])
        self.style.configure('Treeview', background=Helper.SURFACE, fieldbackground=Helper.SURFACE,
                             foreground=Helper.INK, rowheight=26, borderwidth=0,
                             font=(Helper.fontstyle, 11))
        self.style.configure('Treeview.Heading', background=Helper.PAPER, foreground=Helper.MUTED,
                             font=(Helper.fontstyle, 10, 'bold'), relief='flat')
        self.style.map('Treeview', background=[('selected', Helper.BRAND)],
                       foreground=[('selected', '#FFFFFF')])
        self.style.configure('TProgressbar', background=Helper.BRAND, troughcolor=Helper.LINE,
                             borderwidth=0, thickness=10)

    def initGUI(self):
        self.create_menubar()
        self.plagiarism_result(self.topframe)
        '''
        place logo
        '''
        self.place_image(master = self.left_top_imgframe , path = os.path.join(IMAGES_DIR, 'logo.png'))
        self.main_heading(self.left_top_imgframe)
        self.create_tester_gui()
        self.create_chart_window_gui()
        self.create_feature_window_gui()
        self.create_dir_tree(self.left_dir_frame)
        
    def initFrames(self,root):
        self.left_dir_frame = Frame(root,bg=Helper.PAPER,highlightbackground=Helper.LINE,highlightthickness=1,bd=0)
        self.left_top_imgframe=Frame(root,bg=Helper.PAPER,highlightthickness=0,bd=0)
        self.leftframe=Frame(root,bg=Helper.PAPER,highlightbackground=Helper.LINE,highlightthickness=1,bd=0)
        self.rightframe=Frame(root,bg=Helper.PAPER,highlightbackground=Helper.LINE,highlightthickness=1,bd=0)
        self.topframe=Frame(root,bg=Helper.PAPER,highlightbackground=Helper.LINE,highlightthickness=1,bd=0)
        self.bottomframe=Frame(root,bg=Helper.PAPER,highlightbackground=Helper.LINE,highlightthickness=1,bd=0,width=250)
        
        # Responsive grid: header across the top, a fixed control sidebar
        # (controls + directory trees), and a main area (result card + feature
        # tables) that expands to fill the window when resized.
        root.grid_columnconfigure(0, weight=0, minsize=300)   # sidebar
        root.grid_columnconfigure(1, weight=1)                # main area expands
        root.grid_rowconfigure(2, weight=1)                   # tables / trees row expands

        self.left_top_imgframe.grid(row=0, column=0, columnspan=2, sticky='ew', padx=12, pady=(12,8))
        self.leftframe.grid(row=1, column=0, rowspan=2, sticky='nsew', padx=(12,6), pady=(0,8))
        self.topframe.grid(row=1, column=1, sticky='ew', padx=(6,12), pady=(0,8))
        self.rightframe.grid(row=2, column=1, sticky='nsew', padx=(6,12), pady=(0,8))
        # both project directory trees share a full-width strip along the bottom
        self.left_dir_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=12, pady=(0,12))
        # self.bottomframe (charts) intentionally not shown

    def main_heading(self,master):
        main_headinglabel=Label(master,text="Code Clone Detector",
                                font=(Helper.fontstyle,Helper.mainheading_label_size,'bold'),
                                fg=Helper.INK,bg=Helper.PAPER)
        main_headinglabel.pack(side=LEFT,padx=10)
        
    def place_image(self,master,path):
        canvas=Canvas(master,height=72,width=72,highlightthickness=0,bg=Helper.PAPER)
        
        #image=PhotoImage(file = path)
        try:    
            opImage=Image.open(path)
            #opImage.resize=((0.1,0.1),Image.ANTIALIAS)
            #opImage.resize((pixels_x, pixels_y)
            canvas.image = ImageTk.PhotoImage(opImage.resize((64,64),Image.LANCZOS))
            canvas.create_image(0,0, image=canvas.image, anchor='nw')
            #label=Label(master=master,image=img)
            #label.image=img
            
            #canvas.size=(0,0)
            canvas.pack(side=LEFT,fill=BOTH)
            #label.image.pack()
            #label.place(x=0,y=0)

            #canvas.pack()
        except Exception as e:
            print(e.__str__)
            #label=Label(master,image)
        #label.pack(side=LEFT)
        #canvas.create_image(5 , 5 , anchor = NW , image = image)

    def place_backgroundImage(self,master,path):
        image=Image.open(path)

    def plagiarism_result(self,master):
        caption=Label(master,text='STRUCTURAL SIMILARITY',
                      font=(Helper.fontstyle,10,'bold'),fg=Helper.BRAND,bg=Helper.PAPER)
        caption.pack(side=TOP,fill=X,pady=(12,0))
        self.resultlabel=Label(master,text='—',
                               font=(Helper.monofont,Helper.resultfontsize,'bold'),
                               fg=Helper.INK,bg=Helper.PAPER)
        self.resultlabel.pack(side=TOP,fill=X,pady=(2,10))

        self.progressbar=ttk.Progressbar(master,orient=HORIZONTAL,length=100,mode='determinate')
        self.progressbar.pack(fill=X,padx=14,pady=(0,14))
        #self.run_progessbar()
    
    def run_progessbar(self):
        # Indeterminate animation only. The old version ran a blocking
        # `for i in range(101): sleep(0.1)` loop that froze the UI for ~10s
        # and could not be stopped.
        self.progressbar.config(mode='indeterminate')
        self.progressbar.start(12)
        
        '''
        left plagiarism test window methods
        '''
        
    def create_tester_gui(self):
        testerframe = Frame(self.leftframe)
        testerframe.pack(fill=BOTH,pady=5,expand=1)

        notelabel = Label(testerframe,text=Helper.note,font=(Helper.fontstyle,9),
                          fg=Helper.MUTED,bg=Helper.PAPER,justify='center')
        notelabel.pack(side=TOP,expand=1,pady=(4,2))
        
        langheadinglabel=Label(testerframe,text='Select Language')
        langheadinglabel.config(font=(Helper.fontstylebold,Helper.headingfontsize))
        langheadinglabel.pack(side=TOP,pady=5,expand=1)

        self.language_selector(testerframe)

        fileheadinglabel=Label(testerframe,text='Select Source Files')
        fileheadinglabel.config(font=(Helper.fontstylebold,Helper.headingfontsize))
        fileheadinglabel.pack(side=TOP,pady=5,expand=1)

        self.open_srcfile_buttons(testerframe)

        metricsheadinglabel=Label(testerframe,text='Select Metrics')
        metricsheadinglabel.config(font=(Helper.fontstylebold,Helper.headingfontsize))
        metricsheadinglabel.pack(side=TOP,pady=5,expand=1)
        
        self.metrics_check_buttons(testerframe)
        
        techheadinglabel=Label(testerframe,text='Select Plagiarism Technique')
        techheadinglabel.config(font=(Helper.fontstylebold,Helper.headingfontsize))
        techheadinglabel.pack(side=TOP,pady=5,expand=1)
        
        self.plagiaristech_check_buttons(testerframe)
        
        btn_test=ttk.Button(testerframe,text='TEST PLAGIARISM',style='Accent.TButton',
                            command=lambda: self.set_on_plagiarism_test(None))
        btn_test.pack(side=TOP,fill=X,padx=10,pady=(16,10))
        #btn_test.event_add(Event_Handler.set_on_plagiarism_test(self.rb_metrics))
        
    def language_selector(self, master):
        # Labels ('Java','Python','C++') double as values — languages.get()
        # resolves them case-insensitively (and 'C++' via alias).
        self.language_var = StringVar(master)
        labels = [lbl for _, lbl in languages.options()]
        self.language_var.set(labels[0])
        om = ttk.OptionMenu(master, self.language_var, labels[0], *labels)
        om.pack(side=TOP, expand=1, pady=(0, 4))

    def selected_extensions(self):
        return languages.get(self.language_var.get()).extensions

    def open_srcfile_buttons(self,master):
        self.srclabel1 = Label(master,text='Project 1 : not selected',
                               font=(Helper.fontstyle,Helper.buttonfontsize),
                               fg=Helper.MUTED,bg=Helper.PAPER)
        browsebtn1 = Button(master,text='Browse Project 1',command=lambda: self._browse(1))
        browsebtn1.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        self.srclabel1.pack(side=TOP,expand=1)
        browsebtn1.pack(side=TOP,expand=1,pady=(0,6))

        self.srclabel2 = Label(master,text='Project 2 : not selected',
                               font=(Helper.fontstyle,Helper.buttonfontsize),
                               fg=Helper.MUTED,bg=Helper.PAPER)
        browsebtn2 = Button(master,text='Browse Project 2',command=lambda: self._browse(2))
        browsebtn2.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        self.srclabel2.pack(side=TOP,expand=1)
        browsebtn2.pack(side=TOP,expand=1,pady=(0,6))

    def _browse(self, slot):
        tree = self.dir_tree1 if slot == 1 else self.dir_tree2
        self.eventhandler.set_on_browse(tree, slot, self.selected_extensions())
        path = self.eventhandler.path1 if slot == 1 else self.eventhandler.path2
        label = self.srclabel1 if slot == 1 else self.srclabel2
        if path:
            label['text'] = 'Project %d : %s' % (slot, os.path.basename(path.rstrip('/')))
            label['fg'] = Helper.INK

    def metrics_check_buttons(self,master):
        self.isNgram=False 
        self.rb_metrics=IntVar()
        halstead=Radiobutton(master,text='Halstead metrics',value=1,variable=self.rb_metrics)
        ngram=Radiobutton(master,text='NGram Technique',value=2,variable=self.rb_metrics)
        
        halstead.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        ngram.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        
        #halstead.bind('<Button-1>',self.enable_ngram_entry)
        ngram.bind('<Button-1>',self.enable_ngram_entry)
        
        halstead.pack(side=TOP,expand=1)
        ngram.pack(side=TOP,expand=1)
    
        self.ngram_entry(master)
    
    def enable_ngram_entry(self,_):
        print(self.rb_metrics.get())
        if self.rb_metrics.get() == 2:
            self.isNgram = True
            self.ngramentry['state']='normal'
        else:
            self.ngramentry['state']='disabled'
            self.isNgram = False

    def ngram_entry(self,master):
        self.ngramentry = Entry(master,state='disabled')
        self.ngramentry.pack(side=TOP,expand=1)
        
    def plagiaristech_check_buttons(self,master):
        self.rb_tech = IntVar()
        cosine=Radiobutton(master,text='Cosine Distance',value=1,variable=self.rb_tech)
        eucl=Radiobutton(master,text='Euclidean Distance',value=2,variable=self.rb_tech)

        cosine.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        eucl.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        
        cosine.pack(side=TOP,expand=1)
        eucl.pack(side=TOP,pady=5,expand=1)

        '''
        end of left window
        '''
    '''
    charts window
    '''
    def create_chart_window_gui(self):
        self.chartframe = Frame(self.bottomframe)
        self.chartframe.pack(fill=BOTH,expand=1)
        
        chartheadinglabel = Label(self.chartframe,text='CHARTS',font=(Helper.fontstyle,Helper.headingfontsize))
        chartheadinglabel.pack(side=TOP,fill=X,expand=1)

        self.create_optmenu_datassrc(self.chartframe)
        self.create_optmenu_charts(self.chartframe)
        
    def create_optmenu_datassrc(self,master):
        dataoptlabel = Label(master,text='Select Data Source',font=(Helper.fontstyle,Helper.buttonfontsize))
        dataoptlabel.pack(side=TOP,fill=X,expand=1)
        options=['File 1','File 2','Plagiarism']
        
        optvar=StringVar(master)
        optvar.set(options[0])
        optmenu_datasrc = OptionMenu(master,optvar,*options)
        optmenu_datasrc.pack(side=TOP,expand=1)
        
    def create_optmenu_charts(self,master):
        chartoptlabel = Label(master,text='Select Chart',font=(Helper.fontstyle,Helper.buttonfontsize))
        chartoptlabel.pack(side=TOP,fill=X,expand=1)
        options=[Helper.histogram,Helper.piechart,Helper.plot,Helper.scatter]
        
        self.optvar_chart = StringVar(master)
        self.optvar_chart.set(options[0])
        self.optmenu_charts=OptionMenu(master,self.optvar_chart,*options)
        self.optmenu_charts.pack(side=TOP,pady=10,expand=1)
        
        self.optmenu_charts.bind('<Button-1>',self.set_charts)
    '''
    end of chart window
    '''

    '''
    feature window
    '''
    def create_feature_window_gui(self):
        featureframe = Frame(self.rightframe, bg=Helper.PAPER)
        featureframe.pack(fill=BOTH,expand=1)
        featureframe.grid_columnconfigure(0, weight=1)
        featureframe.grid_rowconfigure(1, weight=1)   # two tables share the
        featureframe.grid_rowconfigure(2, weight=1)   # space 50/50

        featureheadinglbl = Label(featureframe,text='FEATURE FREQUENCY',
                                  font=(Helper.fontstyle,Helper.headingfontsize),
                                  fg=Helper.INK,bg=Helper.PAPER)
        featureheadinglbl.grid(row=0,column=0,pady=(8,4))

        f1, self.tv_file1 = self.create_table(featureframe)
        f1.grid(row=1,column=0,sticky='nsew',padx=12,pady=(0,6))
        f2, self.tv_file2 = self.create_table(featureframe)
        f2.grid(row=2,column=0,sticky='nsew',padx=12,pady=(0,10))
        
    def create_listbox(self,master):
        scrollbar1 = Scrollbar(master,orient='vertical')
        scrollbar2 = Scrollbar(master,orient='vertical')
        
        self.listbox1 = Listbox(master,yscrollcommand=scrollbar1.set)
        self.listbox2 = Listbox(master,yscrollcommand=scrollbar2.set)
        height = 50
        width = 4
    #    for i in range(height): #Rows
     #       for j in range(width): #Columns
                #pass
                #b=Entry(listbox1, text="",width=15)
       #         listbox1.insert(END,str(i)+','+str(j))
      #          listbox2.insert(END,str(i)+','+str(j))
                #b.grid(row=i,column=j)
        scrollbar1.config(command=self.listbox1.yview)
        scrollbar2.config(command=self.listbox2.yview)
        scrollbar1.pack(side=RIGHT,expand=1,fill=Y)
        self.listbox1.pack(side=RIGHT,fill=BOTH,expand=1)
        self.listbox2.pack(side=RIGHT,fill=BOTH,expand=1)
        
        scrollbar2.pack(side=RIGHT,fill=Y,expand=1)

    '''
    end of feature window
    '''
     
    def create_menubar(self):
        menubar = Menu(self.topframe)
        self.topframe.master.master.config(menu=menubar)
        
        filemenu = Menu(menubar)
        filemenu.add_command(label='Open')
        filemenu.add_command(label='Exit',command=self.click_on_exit)
        '''
        tools
        '''
        toolsmenu = Menu(menubar)
        toolsmenu.add_command(label='Project 1 inner clone' , command = lambda : self.eventhandler.set_on_internal_clone(1))
        toolsmenu.add_command(label='Project 2 inner clone' , command = lambda : self.eventhandler.set_on_internal_clone(2))
        
        '''
        visualizations
        '''
        visualizationmenu = Menu(menubar)
        visualizationmenu.add_cascade(label='Histogram',command=self.plotGui.draw_hist)
        visualizationmenu.add_cascade(label='Piechart',command=self.plotGui.draw_pie)
        visualizationmenu.add_cascade(label='Plot Line',command=self.plotGui.draw_plot)
        
        #visualizationmenu.bind(self.plotGui.openWindow())
        
        menubar.add_cascade(label='File',menu=filemenu)
        
        menubar.add_separator()
        menubar.add_cascade(label='Tools',menu=toolsmenu)
        menubar.add_separator()
        menubar.add_cascade(label='Visualization',menu=visualizationmenu)
        menubar.add_separator()
        menubar.add_cascade(label='Help')
        menubar.add_separator()
        menubar.add_cascade(label='About')

    def click_on_exit(self):
        self.root.quit()
        
    def table(self):
        tb=tktable.Table(master=self.rightframe,
                         state='disabled',
                         width=50,
                         titlerows=1,
                         rows=5,
                         cols=3,
                         colwidth=20)
        columns=['A','B','C']
        values=[[1,2,3],[1,2,4],[4,6,32],[23,5,7],[32,6,4]]
        '''
        var = tktable.ArrayVar(self.rightframe)
        
        nrows=0
        ncols=0
        
        for col in columns:
            index=str(nrows)+','+str(ncols)
            var[index]=col
            ncols+=1
        nrows=1
        ncols=0
        
        for row in values:
            for item in rows:
                index=str(nrows)+','+str(ncols)
                var[index]=item
                ncols+=1
            nrows+=1
            ncols=0
            
        tb['variable']=var
        tb.pack()
        '''
    def table2(self,master):
        height = 5
        width = 5
        for i in range(height): #Rows
            for j in range(width): #Columns
                s=StringVar()
                b = Entry(master, state='disabled' , textvariable=s)
                #b.grid(row=i, column=j)
                b.pack()
                
    def create_table(self,master):
        frame=Frame(master, bg=Helper.PAPER)
        tv=ttk.Treeview(frame, height=6)
        tv['columns'] = ('feature', 'frequency')
        tv.heading("#0", text='S.No', anchor='w')
        tv.column('#0', width=60, anchor='w')
        tv.heading("feature", text='Feature')
        tv.column('feature', anchor='center')
        tv.heading("frequency", text='Frequency')
        tv.column('frequency', anchor='center')

        scrollbar=Scrollbar(frame,orient='vertical',command=tv.yview)
        tv.configure(yscrollcommand=scrollbar.set)
        tv.pack(side=LEFT, expand=YES, fill=BOTH)
        scrollbar.pack(side=LEFT, fill=Y)
        return frame, tv
    
    def load_tabledata(self,tv,data):
        i=0
        style = ttk.Style()
        
        for key in data.keys():
            i= i+1
            style.configure("Treeview.Column", font=(Helper.fontstylebold, Helper.buttonfontsize))
            tv.insert('', 'end',text=i, values=(key,data[key][0]))

    def create_dir_tree(self,master):
        
        frame1 = Frame(master, bg=Helper.PAPER)
        frame1.pack(side=LEFT, expand=1, fill=X, padx=(0,6))
        self.dir_tree1 = ttk.Treeview(frame1, height=3)
        self.dir_tree1.heading('#0',text='Project 1 Directory', anchor=W)
        parent_dir1 = self.dir_tree1.insert('', text='Project', index = 1)

        sub_pckg1 = self.dir_tree1.insert(parent_dir1,text = 'packages' ,index = 2)

        self.dir_tree1.insert(sub_pckg1,text = 'source code', index = 1)
        self.dir_tree1.pack(side=LEFT, expand=1, fill=X)

        '''
        second project directory
        '''

        frame2 = Frame(master, bg=Helper.PAPER)
        frame2.pack(side=LEFT, expand=1, fill=X, padx=(6,0))

        self.dir_tree2 = ttk.Treeview(frame2, height=3)
        self.dir_tree2.heading('#0', text='Project 2 Directory', anchor=W)
        parent_dir2 = self.dir_tree2.insert('', text='Project', index = 1)

        sub_pckg2 = self.dir_tree2.insert(parent_dir2,text = 'packages' ,index = 2)

        self.dir_tree2.insert(sub_pckg2, text='source code', index = 1)

        self.dir_tree2.pack(side=LEFT, expand=1, fill=X)
        
        
    '''
    Event 
    '''
     
    def set_on_plagiarism_test(self,_):
        # Validate BEFORE touching the progress bar, so an accidental click with
        # nothing selected just shows the hint (no phantom progress that creeps
        # forward on each repeat).
        if not self.eventhandler.path1 or not self.eventhandler.path2:
            messagebox.showinfo(
                'Select two projects',
                'Browse and select a folder for both Project 1 and Project 2 first.\n\n'
                'No code handy? Use the bundled samples/demo-projects/project-a and project-b.')
            return
        if self.rb_metrics.get() not in (1, 2) or self.rb_tech.get() not in (1, 2):
            messagebox.showinfo(
                'Choose options',
                'Select a metric (Halstead or NGram) and a technique '
                '(Cosine or Euclidean) before running the test.')
            return
        exts = self.selected_extensions()
        for label, p in (('Project 1', self.eventhandler.path1),
                         ('Project 2', self.eventhandler.path2)):
            if not [x for x in Directory.search_directories(p, exts) if x.strip()]:
                messagebox.showinfo(
                    'No source files',
                    'No %s files were found in %s:\n%s\n\n'
                    'Pick a folder that contains %s source files.'
                    % ('/'.join(exts), label, p, '/'.join(exts)))
                return
        self.run_progessbar()
        self.root.update_idletasks()
        ok = False
        try:
            ok = self.test(None, None)
        except Exception as e:
            import traceback; traceback.print_exc()
            messagebox.showerror('Comparison failed', str(e))
        finally:
            # The demo projects compare in a fraction of a second, so an
            # indeterminate bar flickers by unseen. Leave it filled on success
            # as a clear "done" state; reset to empty only when it failed.
            self.progressbar.stop()
            self.progressbar.config(mode='determinate')
            self.progressbar['value'] = 100 if ok else 0
        if ok:
            self.load_tabledata(self.tv_file1, self.feature1)
            self.load_tabledata(self.tv_file2, self.feature2)

    def set_listbox(self):
        self.feature1=self.tester.feature1
        self.feature2=self.tester.feature2
        #print(feature1.items())
        
        for k in self.feature1.keys():
            #for j in range(1,1):    
                self.listbox1.insert(END,'FEATURE:  '+k+'\n')
                
                #print(self.feature1[k][0])
                self.listbox1.insert(END,'FREQUENCY: '+str(self.feature1[k][0])+"\n\n")
                self.listbox1.insert(END,' '+'\n')
            
            
        for k in self.feature2.keys():
            self.listbox2.insert(END,'FEATURE:  '+k+'\n')
               
                #print(self.feature1[k][0])
            self.listbox2.insert(END,'FREQUENCY: '+str(self.feature2[k][0])+"\n\n")
            self.listbox2.insert(END,' '+'\n')
            
    def set_charts(self,_):
        
        chart=self.optvar_chart.get()
        
        self.plot.fig.clf()
        if chart == Helper.histogram:
            data=[]
            self.plot.plot_hist(self.chartframe,data=self.feature1.values[0])
        elif chart == Helper.piechart:
            '''
            data=[]
            keys=[]
            for key in self.feature1.keys():
                if key in  self.feature1:
                    if self.feature1[key][0] !=0 and self.feature2[key][0] !=0:
                        keys.append(key)
                        data.append( self.feature2[key][0]/self.feature1[key][0])
            '''
            data=self.datahandler.pieplot_data(feature1=self.feature1,feature2=self.feature2)
            #print(len(data[0]))
            #print(len(data[1]))
            self.plot.plot_pie(self.chartframe,data=data[0],labels=data[1])
            #self.plot.plot_pie(self.chartframe,data=data,labels=keys)
        elif chart == Helper.scatter:
            self.plot.scatter_plot(self.chartframe,x=self.feature1.values[0],y=self.feature2.values[0])
    
        elif chart==Helper.plot:
            self.plot.plot(self.chartframe,x1=self.feature1.keys(),y1=self.feature1.values[0],x2=self.feature2.keys(),y2=self.feature2.values[0])

    def test(self,f1,f2):
        filepath1=self.eventhandler.path1
        filepath2=self.eventhandler.path2
        if not filepath1 or not filepath2:
            messagebox.showinfo(
                'Select two projects',
                'Browse and select a folder for both Project 1 and Project 2 first.\n\n'
                'No code handy? Use the bundled samples/demo-projects/project-a and project-b.')
            return False

        # Metric: NGram (default) unless Halstead is explicitly chosen.
        if self.rb_metrics.get() == 1:
            metrics = HalsteadMetrics(language=self.language_var.get())
        else:
            try:
                n = int(self.ngramentry.get())
            except (ValueError, TypeError):
                n = 2
            metrics = NGram_Metrics(n, language=self.language_var.get())

        # Technique: Euclidean if chosen, otherwise Cosine (default) so the
        # comparison never crashes on an unset selection.
        tech = Euclidean_Distance() if self.rb_tech.get() == 2 else CosineDistance()

        # Route through the shared, verified project-comparison engine. It
        # cleans its own dataset dirs first, so feature vectors from a previous
        # run can't accumulate and break cosine similarity with a dimension
        # mismatch.
        clone = ProjectClone()
        res = clone.test_project_clone(
            file_names=['project1.csv', 'project2.csv'],
            dirs=[filepath1, filepath2],
            metrics=metrics, tech=tech, username='desktop')

        res = float("{0:.2f}".format(res * 100))
        self.resultlabel['text'] = str(res) + ' %'
        self.resultlabel['fg'] = Helper.MATCH if res >= 95 else Helper.INK

        self.feature1 = clone.features[0]
        self.feature2 = clone.features[1]
        self.plotGui.feature1 = self.feature1
        self.plotGui.feature2 = self.feature2
        return True
    
if __name__=="__main__":
    
    GUI()