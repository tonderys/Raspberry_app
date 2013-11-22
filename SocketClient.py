import socket
from threading import Thread
import time

class Socket_client:
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    def __init__(self):
        self.alphabet_thread = self.Alphabet_thread(self)
        self.number_thread = self.Number_Thread(self)
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))
        self.alphabet_thread.start()
        self.number_thread.start()
        self.alphabet_thread.join()
        self.number_thread.join()
        self.s.close()
    
    class Alphabet_thread(Thread):
        alpha=('a','b','c','d','e','f','g','h','i','j','k','l')
        counter = 0
        def __init__(self, controller):
            Thread.__init__(self)
            self.controller = controller
            self.setDaemon(True)
    
        def run(self):
            while self.counter < 11:
                time.sleep(3)
                self.controller.s.send("%s.%s"%(str(self.counter),self.alpha[self.counter]))
                self.counter = self.counter+1
                
    
    class Number_Thread(Thread):
        counter = 0
        def __init__(self, controller):
            Thread.__init__(self)
            self.controller = controller
            self.setDaemon(True)
    
        def run(self):
            while self.counter < 7:
                time.sleep(5)
                self.controller.s.send("%sseconds"%str(self.counter))
                self.counter = self.counter+1
Socket_client()
