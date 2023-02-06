__author__ = 'zhengwang'

import pygame
from pygame.locals import *

import sys
sys.path.append('.')
import config

class RCTest(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((250, 250))
        self.send_inst = True
        self.steer()

    def steer(self):

        while self.send_inst:
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
                        # self.ser.write(chr(1).encode())

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        # self.ser.write(chr(2).encode())

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        # self.ser.write(chr(3).encode())

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        # self.ser.write(chr(4).encode())

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        # self.ser.write(chr(0).encode())
                        # self.ser.close()
                        break

                elif event.type == pygame.KEYUP:
                    print('text')
                    # self.ser.write(chr(0).encode())


if __name__ == '__main__':
    RCTest()

'''
     // single command
     case 1: forward(time); break;
     case 2: reverse(time); break;
     case 3: right(time); break;
     case 4: left(time); break;

     //combination command
     case 6: forward_right(time); break;
     case 7: forward_left(time); break;
     case 8: reverse_right(time); break;
     case 9: reverse_left(time); break;
'''