# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 01:27:25 2019

@author: Syed Hassan Ali
"""

import time as t

from tkinter import *

from tkinter import ttk
from PIL import ImageTk,Image


from com.vsa.gui.libraries import tktable
#from com.vsa.gui.plots.plot import Plot
from com.vsa.gui.handler.event_handler import EventHandler
#from com.vsa.gui.handler.datahandler import DataHandler
from com.vsa.utilities.helper import Helper
from com.vsa.gui.plotgui import PlotGUI
from com.vsa.metrics.HalsteadMetrics import HalsteadMetrics
from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.plagiarism_techniques.euclidean_distance import Euclidean_Distance
from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.gui.thread import CustomThread
from com.vsa.multiple_files.csv_generator import CSVGenerator
from com.vsa.utilities.directories import Directory
from com.vsa.dataset_handler.dataset_handler import DatasetHandler

class GUI:

    def __init__(self):
        self.eventhandler=EventHandler()
        #self.datahandler=DataHandler()
        #self.plot=Plot()
        self.root=Tk()
        self.root.geometry('1024x600')
        self.root.resizable(1,1)
        self.root.title('Code Cloner')
        self.mainFrame=Frame(self.root)
        
        self.mainFrame.pack(expand=YES,fill=BOTH,pady=5)
        
        self.initFrames(self.mainFrame)
        self.plotGui = PlotGUI()
        self.initGUI()
        #plot=Plot()
        #plot.plot_pie(data=[1,2,3,4],labels=['A','B','C','D'],master=self.bottomframe)      
        #self.create_tester_gui()
        #self.create_menubar()
        #self.place_image(self.root, path = 'C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\gui\\images\\background1.jpg')
        self.mainFrame.configure(background='gray')
        
        self.root.attributes('-alpha',1)
        
        #self.root.configure(background='black')
        self.root.mainloop()
        #self.filename=filedialog.askopenfile()
        
        
    def initGUI(self):
        self.create_menubar()
        self.plagiarism_result(self.topframe)
        '''
        place logo
        '''
        self.place_image(master = self.left_top_imgframe , path = 'C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\gui\\images\\logo.png')
        self.main_heading(self.left_top_imgframe)
        self.create_tester_gui()
        self.create_chart_window_gui()
        self.create_feature_window_gui()
        self.create_dir_tree(self.left_dir_frame)
        
    def initFrames(self,root):
        self.left_dir_frame = Frame(root,highlightbackground='black',highlightthickness=1,bd=1)
        self.left_top_imgframe=Frame(root,highlightbackground='black',highlightthickness=1,bd=1)
        self.leftframe=Frame(root,highlightbackground='black',highlightthickness=1,bd=1)
        self.rightframe=Frame(root,highlightbackground='black',highlightthickness=1,bd=1)
        self.topframe=Frame(root,highlightbackground='black',highlightthickness=1,bd=1)
        self.bottomframe=Frame(root,highlightbackground='black',highlightthickness=1,bd=1,width=250)
        
        self.left_top_imgframe.pack(side=TOP,fill=BOTH)
        self.left_dir_frame.pack(side=LEFT,fill=BOTH,expand=YES)
        self.leftframe.pack(side=LEFT,fill=BOTH,padx=5,pady=5)
        self.topframe.pack(side=TOP,pady=5)
        '''
        middle window is not pack
        '''
        #self.bottomframe.pack(side=LEFT,fill=BOTH,padx=5,expand=1)
        
        self.rightframe.pack(side=RIGHT,fill=BOTH,expand=1)
        #self.place_image(self.root,path='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\gui\\images\\background1.jpg')
    
    def main_heading(self,master):
        main_headinglabel=Label(master,text="CODE CLONER",font=(Helper.fontstyle,Helper.mainheading_label_size))
        font=(Helper.fontstyle,Helper.headingfontsize)
        main_headinglabel.pack(side=LEFT,expand=1,fill=Y)
        
    def place_image(self,master,path):
        canvas=Canvas(master,height=80)
        
        #image=PhotoImage(file = path)
        try:    
            opImage=Image.open(path)
            #opImage.resize=((0.1,0.1),Image.ANTIALIAS)
            #opImage.resize((pixels_x, pixels_y)
            canvas.image = ImageTk.PhotoImage(opImage.resize((150,80),Image.ANTIALIAS))
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
        self.resultlabel=Label(master,text='0% PLAGIARISM FOUND',font=(Helper.fontstyle,Helper.resultfontsize),width=500)
        self.resultlabel.pack(side=TOP,fill=X,expand=1)
        
        self.progressbar=ttk.Progressbar(master,orient=HORIZONTAL,length=100,mode='determinate')
        self.progressbar.pack(fill=X)
        #self.run_progessbar()
    
    def run_progessbar(self):
        self.progressbar['maximum']=100
        for i in range(101):
            self.progressbar['value']=i
            self.progressbar.update()
            t.sleep(0.1)            
        
        self.progressbar['value']=0
        self.progressbar.start()
        
        '''
        left plagiarism test window methods
        '''
        
    def create_tester_gui(self):
        testerframe = Frame(self.leftframe)
        testerframe.pack(fill=BOTH,pady=5,expand=1)

        notelabel = Label(testerframe,text=Helper.note,font=(Helper.fontstyle,Helper.buttonfontsize))
        notelabel.pack(side=TOP,expand=1)
        
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
        
        btn_test=Button(testerframe,text='TEST PLAGIARISM',height=2)
        btn_test.config(font=(Helper.fontstylebold,Helper.buttonfontsize))
        btn_test.bind('<Button-1>',self.set_on_plagiarism_test)#_,rb_metrics=self.rb_metrics))
        
        btn_test.pack(side=BOTTOM,fill=X,expand=1)
        #btn_test.event_add(Event_Handler.set_on_plagiarism_test(self.rb_metrics))
        
    def open_srcfile_buttons(self,master):
       # st = Styling()
        #st.apply_on_button()
        
        srclabel1 = Label(master,text='Source File 1 : Not Selected')
        browsebtn1 = Button(master,text='Browse',command = lambda : self.eventhandler.set_on_browse(self.dir_tree1))
        
        srclabel1.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        browsebtn1.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        srclabel1.pack(side=TOP,expand=1)
        browsebtn1.pack(side=TOP,expand=1)
        
        srclabel2=Label(master,text='Source File 2 : Not Selected')
        browsebtn2=Button(master,text='Browse',command = lambda : self.eventhandler.set_on_browse(self.dir_tree2))

        srclabel2.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        browsebtn2.config(font=(Helper.fontstyle,Helper.buttonfontsize))
        
        srclabel2.pack(side=TOP,expand=1)
        browsebtn2.pack(side=TOP,expand=1)

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
        
        cosine.pack(side=TOP,fill=X,expand=1)
        eucl.pack(side=TOP,fill=X,pady=5,expand=1)

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
        featureframe = Frame(self.rightframe)
        featureframe.pack(fill=BOTH,expand=1)
        
        featureheadinglbl = Label(featureframe,text='FEATURE FREQUENCY',font=(Helper.fontstyle,Helper.headingfontsize))
        featureheadinglbl.pack()
        
        '''
        uncomment this to show frequency in listbox
        '''
        #self.create_listbox(featureframe)
        
        self.tv_file1 = self.create_table(featureframe)
        self.tv_file2 = self.create_table(featureframe)
        
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
        frame=Frame(master)
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
            tv.insert('', 'end',text=i, values=(key,data[key][0]))

    def create_dir_tree(self,master):
        
        frame1 = Frame(master)
        frame1.pack(side=TOP, expand=1, fill=BOTH)
        self.dir_tree1 = ttk.Treeview(frame1)
        self.dir_tree1.heading('#0',text='Project 1  Directory', anchor=W)
        parent_dir1 = self.dir_tree1.insert('', text='Project', index = 1)

        sub_pckg1 = self.dir_tree1.insert(parent_dir1,text = 'packages' ,index = 2)
        
        self.dir_tree1.insert(sub_pckg1,text = 'source code', index = 1)
        self.dir_tree1.pack(side = LEFT)
        
        '''
        second project directory
        '''
        
        frame2 = Frame(master)
        frame2.pack(side=TOP,expand = 1 ,fill =BOTH)
        
        self.dir_tree2 = ttk.Treeview(frame2)
        self.dir_tree2.heading('#0', text='Project 2 Directory', anchor=W)
        parent_dir2 = self.dir_tree2.insert('', text='Project', index = 1)
        
        sub_pckg2 = self.dir_tree2.insert(parent_dir2,text = 'packages' ,index = 2)
        
        self.dir_tree2.insert(sub_pckg2, text='source code', index = 1)
        
        self.dir_tree2.pack(side=LEFT)
        
        
    '''
    Event 
    '''
     
    def set_on_plagiarism_test(self,_):
       self.run_progessbar()
       #self.progressbar.start()
       #self.progressbar.update()
       #thread=threading.Thread(name='thread',target=self.test,args=())#,daemon=True)
       self.thread=CustomThread()
       #self.thread.start()
       
       f1='C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\project1\\'
       
       f2='C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\project2\\'

       self.test(f1,f2)
       self.thread.stop()
       #thread.start()
       #thread.run()
       #thread._delete()
       #self.test()
       
       #self.set_listbox()
       
       self.progressbar.stop()
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
        dataset_handler=DatasetHandler()
         #if self.cosineTech:
        #    techStr='Cosine'
        techStr='cosine'
        #filepath1='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\sample_resource\\Main.java'
        #filepath2='C:\\Users\\Syed Hassan Ali\\Desktop\\VSA-Project\\VSA_Project-master\\com\\vsa\\sample_resource\\MDP.java'
        
        filepath1=self.eventhandler.path1
        filepath2=self.eventhandler.path2
        #filepath1=path1
        #filepath2=path2

        dirs1 = Directory.search_directories(filepath1,'.java')
        dirs2 = Directory.search_directories(filepath2,'.java')
        
        if dirs1 is not None: #and not dirs1.empty():
            #if len(name.strip())>0:
            dirs1 = dirs1[:len(dirs1)-2]
        
        if dirs2 is not None: #and not dirs2.empty():
            dirs2 = dirs2[:len(dirs2)-2]
        
        #res=self.datahandler.test_plagiarism(filepath1=filepath1,filepath2=filepath2,isNgram=self.isNgram,techStr=techStr)
        #print(res)
        
        if self.isNgram:    
            n=int(self.ngramentry.get())
            metrics = NGram_Metrics(n)
        else:
            metrics = HalsteadMetrics()
        
        if self.rb_tech.get() == 1:
            tech = CosineDistance()
        elif self.rb_tech.get() == 2:
            tech = Euclidean_Distance()
        
        CSVGenerator.generate_multiples_csv(filepath1,metrics)
        CSVGenerator.generate_multiples_csv(filepath2,metrics, project_no=2)
        
        CSVGenerator.merge_all_csvs('C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\')
        CSVGenerator.merge_all_csvs('C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\',project_no=2)
        
        self.tester = Plagiarism_Tester()
        df1 = dataset_handler.read_csv(file_name = ['project1.csv'] ,address = 'C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\project1\\')
        df2 = dataset_handler.read_csv(file_name = ['project2.csv'] ,address = 'C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\datasets\\project2\\')
        
        #print(df1[0].values[0])

        feature1 = [x for x in df1[0].values]
        feature2 = [x for x in df2[0].values]
        
        res = self.tester.run_test(metrics = metrics ,plagiarism_technique = tech , features=[feature1,feature2],is_project = True)        
                    
        #res = self.tester.run_test(metrics,tech)
        
        res=float("{0:.2f}".format(res*100))
        self.resultlabel['text']=str(res)+'%'+'PLAGIARISM FOUND'
        
        if self.tester.feature1 is not None and self.tester.feature2 is not None:
            self.plotGui.feature1 = self.tester.feature1
            self.plotGui.feature2 = self.tester.feature2
            
            self.feature1=self.tester.feature1
            self.feature2=self.tester.feature2
            #self.progressbar.stop()
        
        self.feature1 = df1[0]
        self.feature2 = df2[0]
    
if __name__=="__main__":
    
    GUI()