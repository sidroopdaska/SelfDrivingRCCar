"""auto_driver.py: Multi-threaded server program that receives jpeg video frames, ultrasonic
sensor data and allows the RC car to drive itself with front collision avoidance."""

import cv2
import numpy as np
import threading
import socketserver
from utils.utils import *
import struct

# Ultrasonic sensor distance value
sensor_data = None


class NeuralNetwork():
    def __init__(self):
        self.model = cv2.ml.ANN_MLP_load('mlp_xml/mlp_1501357468.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)


class RCControl(object):
    def __init__(self):
        self.ser = find_arduino(serial_number=arduino_serial_number)

    def steer(self, prediction):
        if prediction == 0:
            self.ser.write(b'6')
            print("Left")

        elif prediction == 1:
            self.ser.write(b'5')
            print("Right")

        elif prediction == 2:
            self.ser.write(b'1')
            print("Forward")

        else:
            self.stop()

    def stop(self):
        self.ser.write(b'0')


class VideoStreamHandler(socketserver.StreamRequestHandler):
    # Create a neural network
    model = NeuralNetwork()

    car = RCControl()
    global sensor_data

    def handle(self):
        # read the video frames one by one
        try:
            while True:
                image_len = struct.unpack('<L', self.rfile.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break

                recv_bytes = b''
                recv_bytes += self.rfile.read(image_len)

                gray = cv2.imdecode(np.fromstring(recv_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                image = cv2.imdecode(np.fromstring(recv_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

                # Get ROI
                roi = gray[120:240, :]

                # Reshape ROI
                image_array = roi.reshape(1, 38400).astype(np.float32)

                cv2.imshow('Video', image)

                # Neural Network makes the prediction
                prediction = self.model.predict(image_array)

                # Check for stop conditions
                if sensor_data is not None and sensor_data < 15:
                    # Front collision avoidance
                    self.car.stop()
                else:
                    self.car.steer(prediction)

                if (cv2.waitKey(5) & 0xFF) == ord('q'):
                    break

            cv2.destroyAllWindows()

        finally:
            self.car.stop()
            print("Connection closed on the server video thread!")


class SensorStreamHandler(socketserver.BaseRequestHandler):
    global sensor_data
    data = " "

    def handle(self):
        try:
            while self.data:
                self.data = self.request.recv(1024)
                sensor_data = round(float(self.data), 1)
                print(f"Dist: {sensor_data}")
        finally:
            print("Connection closed on sensor server thread!")


class ThreadServer():
    def server_video_thread(host, port):
        server = socketserver.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    def ultrasonic_server_thread(host, port):
        server = socketserver.TCPServer((host, port), SensorStreamHandler)
        server.serve_forever()

    video_thread = threading.Thread(target=server_video_thread, args=(server_address[0], server_address[1]))
    video_thread.start()

    ultrasonic_sensor_thread = threading.Thread(target=ultrasonic_server_thread, args=(server_address[0], server_address[1] + 1))
    ultrasonic_sensor_thread.start()

if __name__ == '__main__':
    ThreadServer()