#source, https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application
#Pillow requires download, python3 -m pip install pillow
#Pandas from pip

import color_pulseModified
import color_ShiftMath
import color_Rainbow
import random
import openpyxl
import pandas as pd
import queue
import string
import sys
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
from tkinter.font import Font
from tkinter import *
from tkinter import colorchooser
from threading import Event

'''
Work in progress
    threading for scripts
    
'''

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift

class PageActual(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.list_widgets = []
        self.checkbox = []
        self.myFont = Font(family = "TkDefaultFont", size = 20)
        self.bind('<Configure>',self.resize )
        self.buttonFont = Font(size = 15)
        self.height = 900 #CHANGE BASED OFF RESOLUTION
        self.width = 1600

    def resize(self, *args):
        #Apply to horizontal shift?
        currHeight = self.winfo_height()
        if self.height != currHeight:
            difference = (currHeight - self.height)
            #Change # based on preference for resize
            actual = int (difference / 20)
            size = self.myFont['size']
            self.myFont.configure(size = size + actual)
            self.height = currHeight

    def getListWidgets(self):
        return self.list_widgets

    def getCheckbox(self):
        if not self.checkbox:
            return False
        for i in self.checkbox:
            bool = i.get()
            if not bool:
                return False
        return True

        
    def addText(self, info):
        label = tk.Label(self, text = info)
        self.list_widgets.append(label)
        #label.config(font = self.myFont)
        label['font'] = self.myFont
        label.pack()

    def delText(self):
        if len(self.list_widgets) > 1:
            val = self.list_widgets.pop()
            val.config(state = NORMAL)
            val.delete(1.0, 'end')

    def changeText(self, widget, info):
        widget['text'] = info


    def addImage(self, img):
        label = tk.Label(self, image = img)
        label.pack()

    def addEntry(self, c1):
        entry = tk.Entry(self, bd = 5)
        entry.pack()
        entry.bind("<Return>", c1)

    def addButton(self, info, c1):
        button = tk.Button(self, text = info, command = c1)
        button['font'] = self.buttonFont
        button.pack()

    def addButtonList(self, info, c1):
        tempFrame = tk.Frame(self)
        for i in range(len(info)):
            button = tk.Button(tempFrame, text = info[i], command = c1[i] )
            button['font'] = self.buttonFont
            button.pack(side = "left")
        tempFrame.pack()

    def addCheckbox(self, test_list):
        for i in test_list:
            var = tk.IntVar()
            temp = tk.Checkbutton(self, text = i, variable = var)
            temp['font'] = self.buttonFont
            self.checkbox.append(var)
            temp.pack()


    def addScale(self, c1, min, max, res, tick, label):
        scale = tk.Scale(
            self, 
            from_ = min, 
            to = max, 
            command = c1, 
            orient = HORIZONTAL,
            length = self.width /2,
            resolution = (max - min) / res,
            tickinterval = (max - min) / tick,
            label = label
        )
        scale['font'] = self.buttonFont
        mid = int((min + max) / 2)
        scale.set(mid)
        scale.pack()

    def addCom(self, c1, c2):
        button = tk.Button(self, text = "Previous", command = c1)
        button2 = tk.Button(self, text = "Next", command = c2)
        button['font'] = self.buttonFont
        button2['font'] = self.buttonFont
        button.place(relx = 0.4, rely = 0.9)
        button2.place(relx = 0.6, rely = 0.9)

    def addComNext(self, c1):
        button = tk.Button(self, text = "Next", command = c1)
        button['font'] = self.buttonFont
        button.place(relx = 0.5, rely = 0.9)

    def addComPrevious(self, c1):
        button = tk.Button(self, text = "Previous", command = c1)
        button['font'] = self.buttonFont
        button.place(relx = 0.5, rely = 0.9)

class MainView(tk.Frame):
    
    def __init__(self, *args, **kwargs):
        #initializing the frame
        tk.Frame.__init__(self, *args, **kwargs)
        self.pages = []
        self.stop_thread = Event()
        self.wave = [500, 150, 125, 200]
        color1 = [255, 0, 0, 255]
        color2 = [0, 0, 255, 255]
        self.color_list = [color1, color2]
        #Processing instructions
        provided_num = 6
        #Creating the actual pages inside of the list
        for _ in range(provided_num):
            self.pages.append(PageActual(self))

        #Setup of the actual frames in the window.
        self.container = tk.Frame(self)
        self.buttonframe = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.buttonframe.pack(fill="x", expand=False)
        self.start()
        self.testButton()

    '''
    The start methods uses the init information to setup and create all the pages. 
    This includes the text grouped together from the spreadsheet. 
    '''    
    def start(self):
        pStart = self.pages[0]
        pEnd = self.pages[-1]
        self.image_name_list = []
        #Setting up all the pages inside the pages list
        for x in self.pages:
            x.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        #Connect the pages (besides Start and End) with their previous and next
        for i in range(1, len(self.pages) - 1):
            self.pages[i].addCom(self.pages[i - 1].lift, self.pages[i + 1].lift)
            self.pages[i].addText("Page: " + str(i))
               
        
        #Setup of the start and end pages.
        pStart.addComNext(self.pages[1].lift)
        pStart.addText("Start Page")

        pEnd.addComPrevious(self.pages[-2].lift)
        pEnd.addText("END")
        
        #Closes the window and kills everything
        def close():
            self.container.destroy()
            self.buttonframe.destroy
            self.destroy()
            sys.exit()

        fontStart = Font(size = 15)
        start = tk.Button(self.container, text = "Start", command = pStart.lift)
        start['font'] = fontStart
        start.place(relx=.5, rely=.5, anchor="center")
        
        exitWindow = tk.Button(self.buttonframe, text = "Exit", command = close)
        exitWindow['font'] = fontStart
        exitWindow.pack(side = "bottom")
        
        pStart.show()


    def testButton(self):
        self.pages[1].addButton("TEST Pulse", self.p1thread)
        self.pages[1].addButton("STOP", self.stop_thread_zero)
        self.pages[1].addButtonList(["SLOW", "MEDIUM", "FAST"], [self.slow_preset, self.medium_preset, self.fast_preset])
        self.pages[1].addButtonList(["Set Red", "Set Green", "Set Blue", "Set Random"], [self.setRed, self.setGreen, self.setBlue, self.setRandomColor])
        self.pages[1].addButton("Choose Color: ", self.choose_color)

        self.pages[2].addButton("TEST Shift", self.p2thread)
        self.pages[2].addButton("STOP", self.stop_thread_zero)
        self.pages[2].addButtonList(["SLOW", "MEDIUM", "FAST"], [self.slow_shift, self.medium_shift, self.fast_shift])
        self.pages[2].addButtonList(["Change Color1", "Change Color2"], [self.changeColor1, self.changeColor2])

        self.pages[3].addButton("TEST Rainbow", self.p3thread)
        self.pages[3].addButton("STOP", self.stop_thread_zero)
        self.pages[3].addButtonList(["SLOW", "MEDIUM", "FAST"], [self.slow_rainbow, self.medium_rainbow, self.fast_rainbow])

        self.pages[4].addButton("TEST Wave", self.p4thread)
        self.pages[4].addButton("STOP", self.stop_thread_zero)

    
        
    def stop_thread_zero(self):
        print("Executing")
        self.thread_event.set()
        self.thread.join()
        print(self.thread.is_alive())

    def choose_color(self):
        color_code = colorchooser.askcolor(title = "Choose color")
        for count, val in enumerate(color_code[0]):
            self.wave[count + 1] = val

    def setBlue(self):
        self.wave[1] = 0
        self.wave[2] = 125
        self.wave[3] = 255

    def setRed(self):
        self.wave[1] = 226
        self.wave[2] = 40
        self.wave[3] = 40

    def setGreen(self):
        self.wave[1] = 46
        self.wave[2] = 226
        self.wave[3] = 40

    def setRandomColor(self):
        self.wave[1] = random.randint(0, 255)
        self.wave[2] = random.randint(0, 255)
        self.wave[3] = random.randint(0, 255)

    def slow_preset(self):
        self.wave[0] = 1000
        self.update()

    def medium_preset(self):
        self.test_reset()
        self.update()

    def fast_preset(self):
        self.wave[0] = 300
        self.update()

    def changeColor1(self):
        self.color_list[0] = random.sample(range(0, 255), 4)

    def changeColor2(self):
        self.color_list[1] = random.sample(range(0, 255), 4)

    def check_thread(self):
        return self.thread.is_alive()

    def shift_reset(self):
        self.wave[0] = 4000

    def slow_shift(self):
        self.wave[0] = 7000

    def medium_shift(self):
        self.shift_reset()

    def fast_shift(self):
        self.wave[0] = 1500

    def slow_rainbow(self):
        self.wave[0] = 33600

    def medium_rainbow(self):
        self.rainbow_reset()

    def fast_rainbow(self):
        self.wave[0] = 8400

    def rainbow_reset(self):
        self.wave[0] = 16800

    def slow_wave(self):
        self.wave[0] = 5500

    def medium_wave(self):
        self.wave_reset()

    def fast_wave(self):
        self.wave[0] = 2000

    def wave_reset(self):
        self.wave[0] = 3000

    def Pass(self):
        bool = self.pages[2].getCheckbox()
        label_list = self.pages[2].getListWidgets()

        if bool:
            message = "PASS\nProceed to next page"
        else:
            message = "All tests did not pass.\nAt least one test failed."
        self.pages[2].changeText(label_list[-1], message)


    def p4thread(self):
        self.wave_reset()
        self.thread_event = threading.Event()

    
    def p3thread(self):
        self.rainbow_reset()
        self.thread_event = threading.Event()
        self.thread = threading.Thread(target = self.rainbow_test, args = [self.wave, self.thread_event])
        self.thread.daemon = True
        self.thread.start()

    def p2thread(self):
        self.shift_reset()
        self.thread_event = threading.Event()
        self.thread = threading.Thread(target = self.shift_test, args = [self.wave, self.thread_event, self.color_list])
        self.thread.daemon = True
        self.thread.start()
        self.pages[2].addCheckbox(["Slow", "Medium", "Fast"])
        self.pages[2].addButton("Pass", self.Pass)
        self.pages[2].addText("Run the test then indicate on the checkbox.")
        self.pages[2].addText("Test has not been run.")

    def rainbow_test(self, val, thread_event):
        color_Rainbow.thread_test(val, thread_event)

    def shift_test(self, val, thread_event, color_list):
        color_ShiftMath.thread_test(val, thread_event, color_list)

    def run_test(self, val, thread_event):
        color_pulseModified.thread_test(val, thread_event)

    def test_reset(self):
        self.wave[0] = 500
 
    def p1thread(self):
        self.test_reset()
        self.thread_event = threading.Event()
        self.thread = threading.Thread(target = self.run_test, args = [self.wave, self.thread_event])
        self.thread.daemon = True
        self.thread.start()
        
    def process_queue(self):
        try:
            msg = self.queue.get(0)
            #Show result of the task
            print("bruh")
        except queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        time.sleep(5)
        self.queue.put("task done")

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)

    main.pack(fill="both", expand=True)
    root.wm_geometry("1600x900")
    root.mainloop()