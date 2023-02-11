import socket
import pygame
from pygame.locals import *

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
        
        pygame.init()
        pygame.display.set_mode((250, 250))
        self.send_inst = True
        
        self.streaming()
        

    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Enter 'q' to to terminate connection")
            
            while self.send_inst:
                # recv_msg = str(self.connection.recv(1024).decode('utf8', 'strict'))
                # if recv_msg == 'exit':
                #     print('exit command recv from client')
                #     break
                # print(f'\nThis is the msg from the client  => {recv_msg} <= \n')
                # self.connection.send(str('here').encode('utf-8'))
                

                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        key_input = pygame.key.get_pressed()
                        
                        # complex orders
                        if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                            print("Forward Right")
                            # self.ser.write(chr(6).encode())

                        elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                            print("Forward Left")
                            # self.ser.write(chr(7).encode())

                        elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                            print("Reverse Right")
                            # self.ser.write(chr(8).encode())

                        elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                            print("Reverse Left")
                            # self.ser.write(chr(9).encode())

                        # simple orders
                        elif key_input[pygame.K_UP]:
                            print("Forward")
                            self.connection.send(str(1).encode('utf-8'))
                            # self.ser.write(chr(1).encode())

                        elif key_input[pygame.K_DOWN]:
                            print("Reverse")
                            self.connection.send(str(2).encode('utf-8'))
                            # self.ser.write(chr(2).encode())

                        elif key_input[pygame.K_RIGHT]:
                            print("Right")
                            self.connection.send(str(3).encode('utf-8'))
                            # self.ser.write(chr(3).encode())

                        elif key_input[pygame.K_LEFT]:
                            print("Left")
                            self.connection.send(str(4).encode('utf-8'))
                            # self.ser.write(chr(4).encode())

                        # exit
                        elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                            print("Exit")
                            self.send_inst = False
                            self.connection.send(str(0).encode('utf-8'))
                            self.connection.send(str('q').encode('utf-8'))
                            # self.ser.write(chr(0).encode())
                            
                            # self.ser.close()
                            break

                    elif event.type == pygame.KEYUP:
                        self.connection.send(str(0).encode('utf-8'))
                        # self.ser.write(chr(0).encode())
            print('q key has been pressed, closing connection')
        
        
                
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    h, p = config.server_addr , 8004
    print('Waiting for client')
    SensorStreamingTest(h, p)