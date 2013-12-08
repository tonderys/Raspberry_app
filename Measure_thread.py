from threading import Thread
import socket
import time

class Measure_thread(Thread):
    values = ()
    times = ()
    clock = 0
    def __init__(self, controller, ip, port):
        print ("utworzono watek mierzacy")
        self.controller = controller
        self.ip = ip
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        Thread.__init__(self)
        self.setDaemon(True)
    
    def run(self):
        while 1:
            self.freq = float(self.controller.frequency_entry.get())
            if self.controller.measurements_started == True:
                #print("wyslano:" + str(self.clock))
                message = "%f" % self.clock
                self.socket.send(message.encode('ascii'))
                data = self.socket.recv(128).decode('ascii')
                #print("odebrano:" + str(data))
                self.times += (self.clock, )
                #print("data:"+data)
                self.values += (float(data), )
                time.sleep(1/self.freq)
                self.clock += 1/self.freq

                #print(self.times)
                #print(self.values)
        self.socket.close()
        

