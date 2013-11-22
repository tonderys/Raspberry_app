from Tkinter import *
from threading import Thread
import time

class Frame:
    top = None
    button = None
    threadRunner = False
    clicked = 0

    def __init__(self):
    	self.top = Tk()
    	self.button = Button(self.top, text = "START", command = self.click, width = 30)
    	self.button.pack()
    	self.top.mainloop()

    def click(self):
        if self.threadRunner == False:
            self.threadRunner = True
            self.timer = self.TimerThread(self)
            self.timer.start()
        else:
            self.threadRunner = False

    class TimerThread(Thread):
        def __init__(self, controller):
            Thread.__init__(self)
            self.controller = controller
            self.setDaemon(True)
         
        def run(self):
            while self.controller.threadRunner == True:
                time.sleep(1)
                print "WIELKI BIALY NAPIS"
                self.controller.clicked += 1
                self.controller.button.config(text = "minelo %d sekund" % self.controller.clicked)
frame = Frame()
