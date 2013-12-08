import socket
import random
from threading import Thread

class Graph_sender:
   TCP_IP = '127.0.0.1'
   TCP_PORT = 5005

   def __init__(self):
        value = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)
        print("nasluchuje")
        conn,addr = self.s.accept()
        while 1:
            try:
                data = conn.recv(128)
                print("odebrano:" + str(data))
                print("wyslano:" + str(value))
                message = "%f" % value
                conn.send(message.encode('ascii') )
                value = value + (random.randrange(-300,300,1) / 100)
            except socket.error:
                conn.close()
                conn,addr = self.s.accept()
        print("koniec")

Graph_sender()
