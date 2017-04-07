import io
import socket
import struct
from PIL import Image

# Create a TCP/IP socket and listen for connections on COMP_IP_ADDRESS:8000
sock = socket.socket()
sock.bind('10.166.38.64', 8000)
sock.listen(1)

print 'Listening for connection...'

# accept a connection and make a file like object out of it
connection = sock.accept()[0].makefile('rb')
print 'Connection established!'
try:
	while True:
		# Read the length of the image as a 32-bit unsigned int. If the
		# length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break
		
		# construct a stream to hold the image data and read image data from the
		# connection
		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))

		# rewind the stream and open it as an image with PIL
		image_stream.seek(0)
		image = Image.open(image_stream)
finally:
	print 'Closing the connection.'
	connection.close()
	sock.close()
