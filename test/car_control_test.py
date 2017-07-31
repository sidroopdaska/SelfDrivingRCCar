"""car_control_test.py: Script to manually control the RC Car"""

import pygame
from pygame.locals import *
from utils.utils import *
import sys

class CarControlTest:
    def __init__(self):
        # Find the Arduino
        try:
            self.ser = find_arduino(serial_number=arduino_serial_number)
        except IOError as e:
            print(e)
            sys.exit()

        self.ser.flush()

        # Setup and begin pygame
        pygame.init()

        pygame.display.set_mode((400, 300))
        self.send_inst = True
        self.steer()

    def steer(self):
        complex_cmd = False

        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN or complex_cmd:
                    key_input = pygame.key.get_pressed()
                    complex_cmd = False

                    # complex car controls
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        complex_cmd = True
                        self.ser.write(b'5')

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        complex_cmd = True
                        self.ser.write(b'6')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        complex_cmd = True
                        self.ser.write(b'7')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        complex_cmd = True
                        self.ser.write(b'8')

                    # simple car controls
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        self.ser.write(b'1')

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.ser.write(b'2')

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.ser.write(b'3')

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.ser.write(b'4')

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        self.close_serial_connection()
                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(b'0')

                elif event.type == pygame.QUIT:
                    self.close_serial_connection()
                    break

    def close_serial_connection(self):
        print('Exit')
        self.ser.write(b'0')
        self.ser.close()
        self.send_inst = False


if __name__ == "__main__":
    CarControlTest()