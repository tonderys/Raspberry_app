from tkinter import *
from tkinter.ttk import *
from DrawGraph import *
import os
from Measure_thread import *

docs_folder = "documentations"

class Application:
    row = 0
    column = 0
    device_name = StringVar 
    def __init__(self):
        self.top_window = Tk()

        self.frequency_label = Label(self.top_window, text = "frequency:")
        self.frequency_label.grid(row = 1,column = 0)
        self.frequency_entry = Entry(self.top_window, text = "1")
        self.frequency_entry.grid(row = 1, column = 1)

        self.ip_label = Label(self.top_window, text = "ip")
        self.ip_label.grid(row = 3, column = 0)
        self.ip_entry = Entry(self.top_window, text="127.0.0.1")
        self.ip_entry.grid(row = 3, column = 1)
        self.port_label = Label(self.top_window, text = "port")
        self.port_label.grid(row = 4, column = 0)
        self.port_entry = Entry(self.top_window, text = "5005")
        self.port_entry.grid(row = 4, column = 1)

        self.start_button = Button(self.top_window, text = "Start!", command = self.start_getting_measurements)
        self.start_button.grid(row = 10, column = 0, columnspan = 2)
        self.graph = DrawGraph(self.top_window, (0,), (0,), 500, 500, 1,2, 10, 1)

    def start_getting_measurements(self):
        measure = Measure_thread(self.frequency_entry.get(), self.ip_entry.get(), self.port_entry.get())
        measure.start()

if __name__ == "__main__":
    app = Application()
    app.top_window.mainloop()
