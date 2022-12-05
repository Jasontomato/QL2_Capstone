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
        frame2 = Frame(master)
        frame2.pack(fill=X)
        # 问题
        label2 = Label(frame2, text='2. Please input the Platform')
        label2.grid(row=1, column=0)
        # 输入框 (Entry)
        self.platname = StringVar()
        self.entryplt = Entry(frame2, textvariable=self.platname)
        self.entryplt.grid(row=1, column=1)
        # 按钮  (Button)
        btn2 = Button(frame2, text='OK', command=self.getPlt)
        btn2.grid(row=1, column=3)

        # 问题3 demand 参数
        frame3 = Frame(master)
        frame3.pack(fill=X)
        # 问题
        label3 = Label(frame3, text='3. Cost Percentage')
        label3.grid(row=1, column=0)
        # 滑动条 (Scale)
        self.cstPtg = StringVar()
        self.scale1 = Scale(frame3, from_=0, to=100, orient=HORIZONTAL, resolution=1)   # 默认垂直
        self.scale1.grid(row=1, column=1)
        # 按钮  (Button)
        btn3 = Button(frame3, text='OK', command=self.getcost)
        btn3.grid(row=1, column=2)
               
        # 展示1  Strategy radio button
        frame4 = Frame(master)
        frame4.pack(fill=X)
        # 说明 是策略
        label4 = Label(frame4, text='4. Show Strategy')
        label4.grid(row=1, column=0)
        # listbox
        self.listbox = Listbox(frame4)
        self.listbox.grid(row=1, column=1)
        for item in ["Strategy1", "Strategy2", 'Strategy3', 'Strategy4', 'Strategy5']:
            self.listbox.insert(END, item)
        # # 按钮  (Button)
        # getage = Button(frame4, text='OK', command=self.getcost)
        # getage.grid(row=1, column=2)

        # 展示2  输出图片
        frame5 = Frame(master)
        frame5.pack(fill=X)
        # 问题
        label5 = Label(frame5, text='Best Strategy Display')
        label5.grid(row=1, column=0)
        # Canvas (/label)
        self.image1 = Image.open("./output/bestStrategy.png")
        resize_img = self.image1.resize((400,500))
        self.test = ImageTk.PhotoImage(resize_img)
    
        #self.label_img = Label(frame5,image=self.test)
        #self.label_img.grid(row=2,column=0)
    


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
        self.cstPtg = self.scale1.get()
        print(self.cstPtg)
        self.listbox.select_set(2)
        workflow(self.platname,self.pid,self.cstPtg)

        # # set img 1 on Canvas (/label)
        # self.image1 = Image.open("./output/bestStrategy.png")
        # resize_img = self.image1.resize((400,500))
        # self.test = ImageTk.PhotoImage(resize_img)
        # # self.label_img = Label(frame5,image=self.test)
        # return

    def openWindow(self):
        newWindow = Toplevel(master)
 
    # sets the title of the
    # Toplevel widget
        newWindow.title("New Window")
 
    # sets the geometry of toplevel
        newWindow.geometry("200x200")
 
    # A Label widget to show in toplevel
        Label(newWindow,
            text ="This is a new window").pack()
        return

TkDemo()
