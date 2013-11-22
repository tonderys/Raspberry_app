from tkinter import *
from DrawGraph import *

class Application:
    def __init__(self):
        self.top_window = Tk()
        self.device_label = Label(self.top_window, text = "device:")
        self.device_label.grid(row = 0, column = 0)
        self.frequency_label = Label(self.top_window, text = "frequency:")
        self.frequency_label.grid(row = 1,column = 1)
        self.frequency_entry = Entry(self.top_window)
        self.frequency_entry.grid(row = 1, column = 2)
        self.frequency_help = Label(self.top_window, text = "(how many seconds between samples)")
        self.frequency_help.grid(row = 2, column = 1, columnspan = 2)
        self.graph = DrawGraph(self.top_window, (0,), (0,), 500, 500, 1,2, 10, 1)

if __name__ == "__main__":
    app = Application()
    app.top_window.mainloop()
