import serial
import serial.tools.list_ports
import pygame
from pygame.locals import *

def find_arduino(serial_number):
    for p in serial.tools.list_ports.comports():
        if p.serial_number == serial_number:
            return serial.Serial(p.device)

    raise IOError("Could not find the Arduino - is it plugged in!")

class RCControlTest:
    def __init__(self):
        # Find the Arduino
        self.ser = find_arduino(serial_number='75237333536351F0F0C1')
        self.ser.flush()

        # Setup and begin pygame
        pygame.init()
        pygame.display.set_mode((400, 300))
        self.send_inst = True
        self.steer()

    def steer(self):
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # simple car controls
                    if key_input[pygame.K_UP]:
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

                    # complex car controls
                    elif key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        self.ser.write(b'5')

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        self.ser.write(b'6')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        self.ser.write(b'7')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        self.ser.write(b'8')

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
    RCControlTest()