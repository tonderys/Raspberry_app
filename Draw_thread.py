from threading import Thread
import socket
import time
from DrawGraph import *

class Draw_thread(Thread):
    def __init__(self, controller, top_window, graph, measurements):
        self.controller = controller
        self.top_window = top_window
        self.graph = graph
        self.measurements = measurements
        Thread.__init__(self)
        self.setDaemon(True)
        
    def run(self):
        while 1:
            if self.controller.measurements_started == True and len(self.measurements.values) > 0:
                self.graph = DrawGraph(self.top_window, self.measurements.values, self.measurements.times, 500, 500, 1, 3, 10, 1)
                time.sleep(1/self.measurements.freq)
            else:
                time.sleep(1)
