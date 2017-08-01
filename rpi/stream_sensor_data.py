"""stream_sensor_data.py: Transmit ultrasonic sensor data over TCP/IP socket"""

import socket
import time
from rpi.utils import (server_address)
import RPi.GPIO as GPIO


def measure():
    # Send a 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()

    while GPIO.output(GPIO_ECHO) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300) / 2

    return distance


def measure_average():
    # returns the average.
    distance1 = measure()
    time.sleep(0.1)

    distance2 = measure()
    time.sleep(0.1)

    distance3 = measure()
    distance = (distance1 + distance2 + distance3) / 3
    return distance


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(server_address)
    print("Connected to the server! Starting to measure the distance...")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Define the GPIO pins for trigger and echo
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24

    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Set trigger to false and allow module to settle
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)

    try:
        while True:
            # Send distance to server every 0.5sec
            distance = measure_average()
            print("Distance: {0:.1f}".format(distance))
            sock.send(distance)
            time.sleep(0.5)
    finally:
        sock.close()
        GPIO.cleanup()