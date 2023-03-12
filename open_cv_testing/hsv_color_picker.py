
import numpy as np
import cv2
import socket
import math

import sys
sys.path.append('.')
import config

def nothing(x):
    pass

# https://medium.com/programming-fever/how-to-find-hsv-range-of-an-object-for-computer-vision-applications-254a8eb039fc

class VideoStreamingTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
                                # Get the new values of the trackbar in real time as the user changes 
            # them
            cv2.namedWindow("Trackbars")

            # Now create 6 trackbars that will control the lower and upper range of 
            # H,S and V channels. The Arguments are like this: Name of trackbar, 
            # window name, range,callback function. For Hue the range is 0-179 and
            # for S,V its 0-255.
            cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
            cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
            cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
            cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
            cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
            cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
            
            l_h = cv2.getTrackbarPos("L - H", "Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "Trackbars")
            u_h = cv2.getTrackbarPos("U - H", "Trackbars")
            u_s = cv2.getTrackbarPos("U - S", "Trackbars")
            u_v = cv2.getTrackbarPos("U - V", "Trackbars")
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #Calling the functions
                    frame = image
                    
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    # Get the new values of the trackbar in real time as the user changes 
                    # them
                    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
                    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
                    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
                    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
                    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
                    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
                
                    # Set the lower and upper HSV range according to the value selected
                    # by the trackbar
                    lower_range = np.array([l_h, l_s, l_v])
                    upper_range = np.array([u_h, u_s, u_v])
                    
                    # Filter the image and get the binary mask, where white represents 
                    # your target color
                    mask = cv2.inRange(hsv, lower_range, upper_range)
                
                    # You can also visualize the real part of the target color (Optional)
                    res = cv2.bitwise_and(frame, frame, mask=mask)
                    
                    # Converting the binary mask to 3 channel image, this is just so 
                    # we can stack it with the others
                    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                    
                    # stack the mask, orginal frame and the filtered result
                    stacked = np.hstack((mask_3,frame,res))
                    
                    # Show this stacked frame at 40% of the size.
                    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
                    

                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print('exit key pressed')
                        break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = config.server_addr, 8000
    VideoStreamingTest(h, p)
