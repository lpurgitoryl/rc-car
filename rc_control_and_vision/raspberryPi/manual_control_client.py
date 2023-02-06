
from socket import *
import time


import sys
sys.path.append('.')
import config



# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((config.server_addr, 8004))

try:
    while True:
        # msg = input('Enter Msg\n')
        # if msg:
        #     client_socket.send(str(msg).encode('utf-8'))
        #     if msg == 'exit':
        #         break
        #     print('sent message\n')
        # recv_msg = str(client_socket.recv(1024).decode('utf8', 'strict'))
        # if recv_msg:
        #     print(f'\nmessage recv\'d from server =>{recv_msg}<=\n')
        
        time.sleep(0.5) 
finally:
    client_socket.close()

