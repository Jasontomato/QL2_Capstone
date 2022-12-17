from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
from modelFuc import *

class TkDemo():
    def __init__(self):
        master = Tk()
        master.title('SmartAlpha')
       

        # 文字 (Label)
        title = Label(master, text='SmartAlpha Price Strategy Simulation System', font='15', bg='white', fg='red')
        title.pack()

        # 问题1 产品ID
        frame1 = Frame(master)
        frame1.pack(fill=X)
        # 问题
        label1 = Label(frame1, text='1. Please input the Product Id')
        label1.grid(row=1, column=0)
        # 输入框 (Entry)
        self.pid = StringVar()
        self.entrypid = Entry(frame1, textvariable=self.pid)
        self.entrypid.grid(row=1, column=1)
        # 按钮  (Button)
        btn1 = Button(frame1, text='OK', command=self.getPid)
        btn1.grid(row=1, column=3)

    
         # 问题2 平台名称
  
        # 问题
        label2 = Label(frame1, text='2. Please input the Platform')
        label2.grid(row=2, column=0, sticky=W)
        # 输入框 (Entry)
        self.platname = StringVar()
        self.entryplt = Entry(frame1, textvariable=self.platname)
        self.entryplt.grid(row=2, column=1)
        # 按钮  (Button)
        btn2 = Button(frame1, text='OK', command=self.getPlt)
        btn2.grid(row=2, column=3)

        # 问题3 demand 参数
 
        # 问题
        label3 = Label(frame1, text='3. Cost Percentage')
        label3.grid(row=3, column=0,sticky=W)
        # 滑动条 (Scale)
        self.cstPtg = StringVar()
        self.scale1 = Scale(frame1, from_=0, to=100, orient=HORIZONTAL, resolution=1)   # 默认垂直
        self.scale1.grid(row=3, column=1,columnspan=2)
        # 按钮  (Button)
        btn3 = Button(frame1, text='OK', command=self.getcost)
        btn3.grid(row=3, column=3)
               
        # 展示1  Strategy radio button
        frame2 = Frame(master)
        frame2.pack(fill=X)
        # 说明 是策略
        label4 = Label(frame2, text='4. Show Strategy')
        label4.grid(row=1, column=0,sticky=W)
        # listbox
        self.listbox = Listbox(frame2,height=5,width=35)
        self.listbox.grid(row=1, column=1,sticky=W)
        for item in ["Strategy1", "Strategy2", 'Strategy3', 'Strategy4', 'Strategy5']:
            self.listbox.insert(END, StrategyName(item))
       
        frame3 = Frame(master)
        frame3.pack(fill=X)
        # 展示2  输出Logo
 
        # 问题
        label5 = Label(frame2, text='Best Strategy Display')
        label5.grid(row=2, column=1)
        # Canvas (/label)
        self.image1 = Image.open("./Logo.jpg")
        resize_img = self.image1.resize((50,50))
        self.test = ImageTk.PhotoImage(resize_img)
    
        self.label_img = Label(frame2,image=self.test)
        self.label_img.grid(row=3,column=0,sticky=W)

        # # 策略说明  (Message)
        self.msgStgy = StringVar()
        self.Msg1 = Text(frame2,height=5,width=30)
        self.Msg1.grid(row=3,column=1)
    


        master.mainloop()


    def getPid(self):
        self.pid =  self.entrypid.get()
        print(self.pid)
        return

    def getPlt(self):
        self.platname =  self.entryplt.get()
        print(self.platname)
        return 
    
    def getname():
        return

    def getcost(self):
        self.cstPtg = self.scale1.get()/100.0
        print(self.cstPtg)
        
        straKey,stravalue = workflow(self.platname,self.pid,self.cstPtg)
        self.listbox.select_set(int(straKey[-1])-1) #select best strategy
        Description = 'Best Strategy:'+ straKey + '\n'+ 'Cumulative Profit:'+stravalue+ '\n'+'Description:'+StrategyDic(straKey)
        self.Msg1.insert(1.0,Description)

        # return

   
TkDemo()
