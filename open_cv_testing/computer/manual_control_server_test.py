import socket
import pygame
from pygame.locals import *
import time

import sys
sys.path.append('.')
import config

class SensorStreamingTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        
        self.send_inst = True
        
        self.streaming()
        

    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Enter 'q' to to terminate connection")
            
            while self.send_inst:
                recv_msg = str(self.connection.recv(1024).decode('utf8', 'strict'))
                if recv_msg == 'exit':
                    print('exit command recv from client')
                    break
                print(f'\nThis is the msg from the client  => {recv_msg} <= \n')
                self.connection.send(str('here').encode('utf-8'))
                

               
            print('q key has been pressed, closing connection')
        
        
                
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    h, p = config.server_addr , 8004
    print('Waiting for client')
    SensorStreamingTest(h, p)