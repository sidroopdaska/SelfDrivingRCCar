"""streamStreamTest.py: Server code for video streaming from rpi """
__author__ = 'Siddharth Sharma'

import cv2
import numpy as np
import socket
import struct

class VideoStreamingTest:
	def __init__(self):
		# Create a TCP/IP socket and listen for connections on COMP_IP_ADDRESS:8000
		# Don't forget to allow the port on the windows firewall settings
		self.server_socket = socket.socket()
		self.server_socket.bind(('10.166.38.64', 8000))
		self.server_socket.listen(0)
		print 'Listening for connection...'
		
		# Accept a single connection and make a file like object out of it
		# TODO: allow multiple client connections using threading.
		self.connection, self.client_address = self.server_socket.accept()
		self.connection = self.connection.makefile('rb')
		self.streamVideo()

	def streamVideo(self):
		try:
			print 'Connection from:', self.client_address
			print 'Streaming...'
			print "Press 'q' to exit"

			while True:
				# Obtain the length of the frame streamed over the connection. If image_len = 0, close the
				# connection
				image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
				if not image_len:
					break

				# Store bytes in a string
				stream_bytes = ''
				stream_bytes += self.connection.read(image_len)

				# Read an image from buffer in memory
				image = cv2.imdecode(np.fromstring(stream_bytes, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)

				# Show the frame
				cv2.imshow('Video', image)
				if (cv2.waitKey(5) & 0xFF) == ord('q'):
					break
		finally:
			print 'Closing the connection.'
			self.connection.close()
			self.server_socket.close()

if __name__ == '__main__':
	VideoStreamingTest()
