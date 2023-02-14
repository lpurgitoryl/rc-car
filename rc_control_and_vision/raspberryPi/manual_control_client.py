
from socket import *
import time
import serial


import sys
sys.path.append('.')
import config

# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((config.server_addr, 8004))
ser = serial.Serial(config.serial_port, 115200, timeout=1)

try:
    while True:
        # msg = input('Enter Msg\n')
        # if msg:
        #     client_socket.send(str(msg).encode('utf-8'))
        #     if msg == 'exit':
        #         break
        #     print('sent message\n')
        
        ard = client_socket.recv(1024)
        recv_msg = str(ard.decode('utf8', 'strict'))
        if recv_msg == 'q':
            break
        
        print(f'\nmessage recv\'d from server =>{recv_msg}<=\n')
        serial.write(ard)
        
        
    
finally:
    ser.close()
    client_socket.close()
    

