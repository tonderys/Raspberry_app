from Tkinter import *
from time import *
import socket
from threading import Thread

class SocketServer:
    ip = "localhost"
    port = 5005
    buffer_size = 50
    listen_flag = False 

    def __init__(self):
        self.top_window = Tk()
        self.text = StringVar()
        message = Message(self.top_window, textvariable = self.text)
        message.grid(column = 1, row = 1)
        button = Button(self.top_window, text = "listen", command = self.listen)
        button.grid(column = 1, row = 2)
        self.writer = self.Writer_thread(self)

    class Writer_thread(Thread):
        def __init__(self, controller):
            Thread.__init__(self)
            self.controller = controller
            self.setDaemon(True)
        def run(self):
            while self.controller.listen_flag:
                data = self.controller.conn.recv(self.controller.buffer_size)
                if not data: continue 
                self.controller.text.set (self.controller.text.get() + data + "\n")

    def listen(self):
        if not self.listen_flag:
            self.listen_flag = True
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.ip, self.port))
            sock.listen(1)
     
            self.conn, addr = sock.accept()
            print 'Connection Address:', addr
            self.writer.start()
        else:
            self.listen_flag = False
            #self.writer.join()
            self.conn.close()
        
sock = SocketServer()
sock.top_window.mainloop()
