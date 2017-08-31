"""auto_driver.py: Multi-threaded server program that receives jpeg video frames, ultrasonic
sensor data and allows the RC car to drive itself with front collision avoidance."""

import cv2
import math
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


class ObjectDetection(object):
    def __init__(self):
        self.red_light = False
        self.green_light = False

    def detect(self, image, gray, classifier):
        # Parameter needed for measuring dist using monocular vision
        # Camera coordinates for the y-axis pertaining to point on the target object, P
        v = 0

        # minimum difference between the lowest and highest pixel intesity values to proceed
        # detection of traffic being on
        threshold = 150

        # Detect the objects
        objects = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(image, (x+5, y+5), (x+w-5, y+h-5), (255, 255, 255), 2)
            v = y + h - 5

            print(f"width/height is: {w/h}")
            # Stop sign
            if w / h == 1:
                cv2.putText(image, 'STOP', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Traffic light
            else:
                roi = gray[y+10: y+h-10, x+10: x+w-10]

                # Apply a Gaussian blur through the image and find the brightest spot to determine if the
                # light is on
                mask = cv2.GaussianBlur(roi, (25,25), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

                # Check to see if light is on
                if maxVal - minVal > threshold:
                    cv2.circle(roi, maxLoc, 5, (255, 0, 0), 2)

                    # Red light
                    if 1.0/8*(h - 30) < maxLoc[1] < 4.0/8*(h - 30):
                        cv2.putText(image, 'Red', (x+5, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        self.red_light = True

                    # Green light
                    if 5.5/8*(h-30) < maxLoc[1] < h - 30:
                        cv2.putText(image, 'Red', (x + 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        self.green_light = True

            return v


class DistanceToCamera(object):
    def __init__(self):
        # Params obtained from camera calibration
        self.alpha = 8.0 * math.pi / 180
        self.v0 = 119.865631
        self.ay = 332.262498

    def calculate(self, v, h, x_shift, image):
        """Calculates the distance to an object through a geometry model using monocular vision"""
        d = h / math.tan(self.alpha + math.atan((v - self.v0) / self.ay))

        if d > 0:
            cv2.putText(image, f"{d:.1f}cm", (image.shape[1] - x_shift, image.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return d


class VideoStreamHandler(socketserver.StreamRequestHandler):
    # Cascade Classifiers
    stop_classifier = cv2.CascadeClassifier('./cascade_classifiers/stop_sign.xml')
    light_classifier = cv2.CascadeClassifier('./cascade_classifiers/traffic_light.xml')

    # Object detection instance
    obj_detection = ObjectDetection()

    # Distance to camera instance
    dist_to_camera = DistanceToCamera()
    h_stop = 14.5 - 10 # cm
    h_light = 14.5 - 10 # cm
    d_stop = 30.0
    d_light = 30.0

    # Create a neural network
    model = NeuralNetwork()

    car = RCControl()

    def handle(self):
        global sensor_data
        stop_sign_active = True
        stop_flag = False
        stop_start = 0
        stop_finish = 0
        stop_time = 0
        drive_time_after_stop = 0

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

                # Object detection
                v_stop = self.obj_detection.detect(image, gray, self.stop_classifier)
                v_light = self.obj_detection.detect(image, gray, self.light_classifier)

                # Distance measurement
                if v_stop > 0 or v_light > 0:
                    d_stop = self.dist_to_camera.calculate(v_stop, self.h_stop, 300, image)
                    d_light = self.dist_to_camera.calculate(v_light, self.h_light, 100, image)
                    self.d_stop = d_stop
                    self.d_light = d_light

                # Neural Network makes the prediction
                prediction = self.model.predict(image_array)

                # Check for stop conditions
                if sensor_data is not None and sensor_data < 30:
                    # Front collision avoidance
                    self.car.stop()
                    print("Stopping, obstacle in front!")

                elif 0.0 < self.d_stop < 30.0 and stop_sign_active:
                    print('Stop sign ahead. Stopping...')
                    self.car.stop()

                    # Stop for 5 seconds
                    if stop_flag is False:
                        stop_start = cv2.getTickCount()
                        stop_flag = True

                    stop_finish = cv2.getTickFrequency()
                    stop_time = stop_finish - stop_start
                    print(f"Stop time: {stop_time}")

                    # Waited 5 seconds, continue driving
                    if stop_time > 5:
                        stop_flag = False
                        stop_sign_active = False
                        print("Waited for 5 seconds")

                elif 0.0 < self.d_light < 30.0:
                    if self.obj_detection.red_light:
                        print("Red light")
                        self.car.stop()
                    elif self.obj_detection.green_light:
                        print("Green light")
                        pass
                        
                    self.obj_detection.red_light = False
                    self.obj_detection.green_light = False
                    self.d_light = 30.0

                else:
                    self.car.steer(prediction)
                    self.d_stop = 30.0
                    stop_start = cv2.getTickCount()

                    if stop_sign_active is False:
                        drive_time_after_stop = (stop_start - stop_finish) / cv2.getTickFrequency()
                        if drive_time_after_stop > 5:
                            stop_sign_active = True

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