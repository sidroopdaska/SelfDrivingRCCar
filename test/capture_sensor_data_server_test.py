"""capture_sensor_data_server_test.py: Capture ultrasonic sensor data on server side"""

import socket
import time
from utils.utils import *


class CaptureSensorDataTest(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(server_address)
        self.sock.listen(1)
        self.connection, self.client_address = self.sock.accept()
        self.capture_data()

    def capture_data(self):
        try:
            print("Connection from: {0}".format(self.client_address))
            start = time.time()

            while True:
                sensor_data = float(self.connection.recv(1024))
                print("Distance: {0:.1f} cm".format(sensor_data))

                # Test for 1 min
                if time.time() - start > 300:
                    break
        finally:
            self.connection.close()
            self.sock.close()


if __name__ == '__main__':
    CaptureSensorDataTest()