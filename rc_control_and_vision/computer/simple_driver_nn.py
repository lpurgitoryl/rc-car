
import cv2
import numpy as np
import socket
from model import NeuralNetwork

import sys
sys.path.append('.')
import config

class RCDriverNNOnly(object):

    def __init__(self, host, port1, port2, serial_port, model_path):

        # connection for data to be sent to arduino (manual_control_client.py)
        
        self.server_socket1 = socket.socket()
        self.server_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket1.bind((host, port2))
        self.server_socket1.listen(0)

        self.connection1 = self.server_socket1.accept()[0]

        # camera streaming
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port1))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # load trained neural network
        self.nn = NeuralNetwork()
        self.nn.load_model(model_path)
        
    def steer(self, prediction):
        if prediction == 2:
            self.connection1.send(str(1).encode('utf-8'))
            print("Forward")
        elif prediction == 0:
            self.connection1.send(str(7).encode('utf-8'))
            print("Forward Left")
        elif prediction == 1:
            self.connection1.send(str(6).encode('utf-8'))
            print("Forward Right")
        else:
            self.connection1.send(str(0).encode('utf-8'))
            print("stop")
        
        
    def drive(self):
        stream_bytes = b' '
        try:
            # stream video frames one by one
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]

                    cv2.imshow('image', image)
                    # cv2.imshow('mlp_image', roi)

                    # reshape image
                    image_array = roi.reshape(1, int(height/2) * width).astype(np.float32)

                    # neural network makes prediction
                    prediction = self.nn.predict(image_array)
                    self.steer(prediction)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("car stopped")
                        self.steer(0)
                        break
        finally:
            cv2.destroyAllWindows()
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p1 = config.server_addr, 8000
    
    # host port for control
    h, p2 = config.server_addr, 8004
    
    # serial port
    sp = config.serial_port

    # model path
    path = "saved_model/nn_model.xml"

    rc = RCDriverNNOnly(h, p1, p2, sp, path)
    rc.drive()
