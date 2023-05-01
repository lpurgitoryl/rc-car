
import numpy as np
import cv2
import math

import socket
import time
import os


import sys
sys.path.append('.')
import config

# HSV (Hue, Saturation, Value)
def convert_to_HSV(frame):
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  cv2.imshow("HSV image",hsv)
  
  return hsv

# takes in hsv frame
# https://www.geeksforgeeks.org/implement-canny-edge-detector-in-python-using-opencv/?ref=rp
# https://www.geeksforgeeks.org/real-time-edge-detection-using-opencv-python/?ref=rp
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

def detect_edges(frame):
    lower_blue = np.array([96, 80, 118], dtype = "uint8")
    upper_blue = np.array([179, 255, 162], dtype="uint8")
    
    mask = cv2.inRange(frame,lower_blue,upper_blue) # this mask will filter out everything but blue
    cv2.imshow("mask", mask)
    # detect edges
    # res = cv2.bitwise_and(frame,frame, mask= mask)
    
    edges = cv2.Canny(mask, 50, 100) 
    cv2.imshow("edges",edges)
    return edges

# takes edge frame
# the point (0,0) starts from the upper left corner. y-axis being the height and x-axis being the width
def region_of_interest(edges):
    height, width = edges.shape # extract the height and width of the edges frame
    mask = np.zeros_like(edges) # make an empty matrix with same dimensions of the edges frame

    # only focus lower half of the screen
    # specify the coordinates of 4 points (lower left, upper left, upper right, lower right)
    polygon = np.array([[
        (0, height), 
        (0,  height/2),
        (width , height/2),
        (width , height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255) # fill the polygon with blue color 
    cropped_edges = cv2.bitwise_and(edges, mask) 
    cv2.imshow("roi",cropped_edges)
    return cropped_edges

def detect_line_segments(cropped_edges):
    rho = 1  
    theta = np.pi / 180  
    min_threshold = 10 
    line_segments = cv2.HoughLinesP(cropped_edges, rho, theta, min_threshold, 
                                    np.array([]), minLineLength=5, maxLineGap=150)
    return line_segments

def average_slope_intercept(frame, line_segments):
    lane_lines = []

    if line_segments is None:
        print("no line segment detected")
        return lane_lines

    height, width,_ = frame.shape
    left_fit = []
    right_fit = []
    boundary = 1/3

    left_region_boundary = width * (1 - boundary) 
    right_region_boundary = width * boundary 

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                print("skipping vertical lines (slope = infinity)")
                continue

            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)

            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    # lane_lines is a 2-D array consisting the coordinates of the right and left lane lines
    # for example: lane_lines = [[x1,y1,x2,y2],[x1,y1,x2,y2]]
    # where the left array is for left lane and the right array is for right lane 
    # all coordinate points are in pixels
    return lane_lines

# helper function for avg slope
def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 / 2)  # make points from middle of the frame down

    if slope == 0: 
        slope = 0.1    

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return [[x1, y1, x2, y2]]

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=6): # line color (B,G,R)
    line_image = np.zeros_like(frame)

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)

    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)  
    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=6 ):

    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape

    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)

    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    return heading_image

def get_steering_angle(frame, lane_lines):
    height, width, _ = frame.shape

    if len(lane_lines) == 2: # if two lane lines are detected
        _, _, left_x2, _ = lane_lines[0][0] # extract left x2 from lane_lines array
        _, _, right_x2, _ = lane_lines[1][0] # extract right x2 from lane_lines array
        mid = int(width / 2)
        x_offset = (left_x2 + right_x2) / 2 - mid
        y_offset = int(height / 2)  

    elif len(lane_lines) == 1: # if only one line is detected
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
        y_offset = int(height / 2)

    elif len(lane_lines) == 0: # if no line is detected
        x_offset = 0
        y_offset = int(height / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  
    steering_angle = angle_to_mid_deg + 90 

    return steering_angle




class computer_processing(object):
# https://github.com/aseempurohit/udp-server-multiple-ports/blob/master/udp-server.py
    def __init__(self, host, port1, port2):
        
        # commands
        
        self.server_socket1 = socket.socket()
        self.server_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket1.bind((host, port2))
        self.server_socket1.listen(0)

        self.connection1 = self.server_socket1.accept()[0]
        
        # camera streaming
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port1))
        self.server_socket.listen(0)

        self.connection = self.server_socket.accept()[0].makefile('rb')


        self.send_inst = True
        self.speed = 8
        self.lastTime = 0
        self.lastError = 0

        self.kp = 0.4
        self.kd = self.kp * 0.65


    def init(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()


        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #Calling the functions
                    
                    hsv = convert_to_HSV(image)
                    edges = detect_edges(hsv)
                    roi = region_of_interest(edges)
                    line_segments = detect_line_segments(roi)
                    lane_lines = average_slope_intercept(image,line_segments)
                    lane_lines_image = display_lines(image,lane_lines)
                    steering_angle = get_steering_angle(image, lane_lines)
                    heading_image = display_heading_line(lane_lines_image,steering_angle)
                    
                    cv2.imshow("heading line",heading_image)
                    
                    cv2.imshow('original image', image)

                    
                    frame += 1
                    total_frame += 1

                    # self.connection1.send(str(1).encode('utf-8'))
                    
                    
                    now = time.time()
                    
                    #  pid controller 
                    dt = now - self.lastTime

                    deviation = steering_angle - 90
                    error = abs(deviation)
                    
                    if deviation < 5 and deviation > -5: # do not steer if there is a 10-degree error range
                        deviation = 0
                        error = 0
                        self.connection1.send(str(0).encode('utf-8'))

                    elif deviation > 5: # steer right if the deviation is positive
                        self.connection1.send(str(6).encode('utf-8'))
                        

                    elif deviation < -5: # steer left if deviation is negative
                        self.connection1.send(str(7).encode('utf-8'))

                    derivative = self.kd * (error - self.lastError) / dt
                    proportional = self.kp * error
                    PD = int(self.speed + derivative + proportional)
                    spd = abs(PD)

                    if spd > 25:
                        spd = 25
                        
                    # throttle.start(spd)
                    self.connection1.send(str(1).encode('utf-8'))

                    self.lastError = error
                    self.lastTime = time.time()
                    time.sleep(.2)
                    # # complex orders
                    # if :
                    #     print("Forward Right")
                    #     saved_frame += 1
                    #     self.connection1.send(str(6).encode('utf-8'))

                    # elif :
                    #     print("Forward Left")
                    #     saved_frame += 1
                    #     self.connection1.send(str(7).encode('utf-8'))



                    # # simple orders
                    # elif :
                    #     print("Forward")
                    #     saved_frame += 1
                    #     self.connection1.send(str(1).encode('utf-8'))


                    # elif :
                    #     print("stop")
                    #     self.send_inst = False
                    #     self.connection1.send(str(0).encode('utf-8'))
                    #     break


                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print('exit key pressed')
                        self.connection1.send(str(0).encode('utf-8'))
                        break


            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            self.connection.close()
            self.connection1.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port for camera
    h, p1 = config.server_addr, 8000

    # host port for control
    h, p2 = config.server_addr, 8004

    # vector size, half of the image
    s = 120 * 320

    ctd = computer_processing(h, p1, p2)
    ctd.init()
