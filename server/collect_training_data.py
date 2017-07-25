"""collect_training_data.py: Collects the training images and classifies them based
on the user car control"""

import cv2
import numpy as np
import socket
import struct
import pygame
from pygame.locals import *
from utils.utils import *
import time
import os

# TODO: save the images within the same .npz file


class CollectTrainingData(object):
    def __init__(self):
        # Open a socket and accept a single connection in read mode
        self.sock = socket.socket()
        self.sock.bind(server_address)
        self.sock.listen(1)

        self.connection = self.sock.accept()[0].makefile('rb')

        # Connect to the serial port
        self.ser = find_arduino(arduino_serial_number)
        self.ser.flush()
        self.send_instr = True

        # Create class labels (L, R, F, B)
        self.k = np.zeros((4,4), 'float')
        for i in range(4):
            self.k[i,i] = 1

        # Initialise pygame for user car steering input
        pygame.init()
        pygame.display.set_mode((400, 300))

        self.collect_images()

    def collect_images(self):
        saved_frames = 0
        total_frames = 0
        start_time = cv2.getTickCount()

        print('Starting to collect training images...')
        img_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # Capture frames from the streamed video
        try:
            frame = 1

            while self.send_instr:
                # Get frame
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break

                recv_bytes = b''
                recv_bytes += self.connection.read(image_len)
                image = cv2.imdecode(np.fromstring(recv_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                # save image
                cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)

                # Show the frame
                cv2.imshow('Video', image)

                # get ROI- lower half of the image (height, width, channel= no channel for greyscale)
                roi = image[120:240, :]

                # Reshape the ROI image into one row array
                temp_array = roi.reshape(1, 38400).astype(np.float32)

                frame += 1
                total_frames += 1

                # Get driver input
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        key = pygame.key.get_pressed()

                        if key[pygame.K_UP] and key[pygame.K_RIGHT]:
                            print("Forward Right")
                            img_array = np.vstack((img_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
                            saved_frames += 1
                            self.ser.write(b'5')

                        elif key[pygame.K_UP] and key[pygame.K_LEFT]:
                            print("Forward Left")
                            img_array = np.vstack((img_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            saved_frames += 1
                            self.ser.write(b'6')

                        elif key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
                            print("Reverse Right")
                            self.ser.write(b'7')

                        elif key[pygame.K_DOWN] and key[pygame.K_LEFT]:
                            print("Reverse Left")
                            self.ser.write(b'8')

                        elif key[pygame.K_UP]:
                            print("Forward")
                            img_array = np.vstack((img_array, temp_array))
                            label_array = np.vstack((label_array, self.k[2]))
                            saved_frames += 1
                            self.ser.write(b'1')

                        elif key[pygame.K_DOWN]:
                            print("Reverse")
                            img_array = np.vstack((img_array, temp_array))
                            label_array = np.vstack((label_array, self.k[3]))
                            saved_frames += 1
                            self.ser.write(b'2')

                        elif key[pygame.K_RIGHT]:
                            print("Right")
                            img_array = np.vstack((img_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
                            saved_frames += 1
                            self.ser.write(b'3')

                        elif key[pygame.K_LEFT]:
                            print("Left")
                            img_array = np.vstack((img_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            saved_frames += 1
                            self.ser.write(b'4')

                        elif key[pygame.K_x] or key[pygame.K_q]:
                            print("Exit")
                            self.ser.write(b'0')
                            self.send_instr = False
                            break

                    elif event.type == KEYUP:
                        self.ser.write(b'0')

            # Save training images and labels
            training_data = img_array[1:, :]
            training_labels = label_array[1:, :]

            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)

            try:
                np.savez(directory + '/' + file_name + '.npz', training_data=training_data,
                         training_labels=training_labels)
            except IOError as e:
                print(e)

            # Print meta data
            end_time = cv2.getTickCount()
            duration = end_time - start_time // cv2.getTickFrequency()
            print("Streaming duration: {0}".format(duration))
            print(training_data.shape)
            print(training_labels.shape)
            print("Total frames: {}".format(total_frames))
            print("Saved frames: {}".format(saved_frames))
            print("Dropped frames: {}".format(total_frames - saved_frames))

        finally:
            self.connection.close()
            self.sock.close()


if __name__ == '__main__':
    CollectTrainingData()
