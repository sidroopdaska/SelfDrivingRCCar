import serial
import pygame
from pygame.locals import *

class RCControlTest:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((400, 300))
        self.send_inst = True
        self.steer()

    def steer(self):
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    if key_input[pygame.K_UP]:
                        print("Forward")

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")

                    elif key_input[pygame.K_LEFT]:
                        print("Left")

                    elif key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print('Exit')
                        self.send_inst = False
                        break

                elif event.type == pygame.KEYUP:
                    pass

if __name__ == "__main__":
    RCControlTest()