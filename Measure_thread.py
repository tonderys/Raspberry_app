from threading import Thread
import socket
import time

class Measure_thread(Thread):
    values = ()
    times = ()
    clock = 0
    def __init__(self, controller, ip, port):
        self.controller = controller
        self.ip = ip
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        Thread.__init__(self)
        self.setDaemon(True)

    def change_freq(self, frequency) :
        self.freq = frequency
    
    def run(self):
        while 1:
            if self.controller.measurements_started == True:
                message = "%f" % self.clock
                self.socket.send(message.encode('ascii'))
                data = self.socket.recv(128).decode('ascii')
                self.times += (self.clock, )
                self.values += (float(data), )
                self.clock += 1/self.freq
                time.sleep(1/self.freq)
            else:
                time.sleep(1)
        self.socket.close()
        

