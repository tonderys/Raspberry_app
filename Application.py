from Tkinter import *
from DrawGraph import *
import os
from time import gmtime, strftime
from Measure_thread import *
from Draw_thread import *

class Application:
    row = 0
    column = 0
    measurements_started = False
    folder = strftime("%Y-%m-%d---%H:%M:%S", gmtime())
    def __init__(self):
        self.top_window = Tk()
        self.ip_entry_var = StringVar()
        self.port_entry_var = StringVar()
        self.frequency_entry_val = StringVar()

        self.frequency_label = Label(self.top_window, text = "frequency:")
        self.frequency_label.grid(row = 1,column = 0)
        self.frequency_entry = Entry(self.top_window, text = "1", textvariable = self.frequency_entry_val)
        self.frequency_entry.grid(row = 1, column = 1)
        self.frequency_unit_label = Label(self.top_window, text = "measures/second")
        self.frequency_unit_label.grid(row = 1, column = 2)

        self.ip_label = Label(self.top_window, text = "ip")
        self.ip_label.grid(row = 3, column = 0)
        self.ip_entry = Entry(self.top_window, textvariable = self.ip_entry_var)
        self.ip_entry.grid(row = 3, column = 1)
        self.port_label = Label(self.top_window, text = "port")
        self.port_label.grid(row = 4, column = 0)
        self.port_entry = Entry(self.top_window, textvariable = self.port_entry_var) 
        self.port_entry.grid(row = 4, column = 1)

        self.ip_entry_var.set("127.0.0.1")
        self.port_entry_var.set("5005")

        self.start_button = Button(self.top_window, text = "Start!", command = self.start_or_stop_getting_measurements)
        self.start_button.grid(row = 10, column = 0, columnspan = 2)
        self.send_button = Button(self.top_window, text = "Send!", command = self.send_files_to_ftp)        
        self.send_button.grid(row = 11, column = 0, columnspan = 2)

        self.graph = DrawGraph(self.top_window, (0,), (0,), 500, 500, 1,3, 10, 1)

    def start_or_stop_getting_measurements(self):
        if self.measurements_started == False:
            self.measurements_started = True
            self.start_button.config(text = "Stop!")
            self.frequency_entry.config(state = "disabled")
            try:
                if not float(self.frequency_entry.get()) > 0 :
                    self.frequency_entry_val.set('1')
            except ValueError:
                self.frequency_entry_val.set('1')
                
            if not hasattr(self, 'measure'):
                self.measure = Measure_thread(self, self.ip_entry.get(), self.port_entry.get())
                self.measure.change_freq(float(self.frequency_entry.get()))
                self.measure.start()
            else:   
                self.measure.change_freq(float(self.frequency_entry.get()))
            if not hasattr(self, 'drawer'):
                self.drawer = Draw_thread(self,self.top_window, self.graph, self.measure)
                self.drawer.start()
        else:
            self.measurements_started = False
            self.start_button.config(text = "Start!")
            self.frequency_entry.config(state = "normal")

    def send_files_to_ftp(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        self.make_graph_index()

    def make_graph_image(self):
        self.drawer.graph.make_image_to_file(self.folder + "/img.png")

    def make_graph_table(self):
        table = "\t\t<table border=1>\n"
        table += "\t\t\t<tr>\n"
        table += "\t\t\t\t<td><b>value</b></td>\n"
        for v in self.measure.values:
            table += "\t\t\t\t<td>"+str(v)+"</td>\n"
        table += "\t\t\t</tr><tr>\n"
        table += "\t\t\t\t<td><b>time</b></td>\n"
        for v in self.measure.times:
            table += "\t\t\t\t<td>"+str(v)+"</td>\n"
        table += "\t\t\t</tr>\n"
        table += "\t\t</table>\n"
        return table

    def make_graph_index(self):
        index = "<html>\n"
        index += "\t<body>\n"
        self.make_graph_image()
        index += '\t\t<img src="img.png">'
        index += self.make_graph_table()
        index += "\t</body>\n"
        index += "</html>"
        file = open(self.folder + "/index.html", "w")
        file.write(index)
        file.close()
        
 
if __name__ == "__main__":
    app = Application()
    app.top_window.mainloop()
