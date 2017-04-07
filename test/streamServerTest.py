import io
import socket
import struct
from PIL import Image

# Create a TCP/IP socket and listen for connections on COMP_IP_ADDRESS:8000
# Don't forget to allow the port on the windows firewall settings
sock = socket.socket()
sock.bind(('10.166.38.64', 8000))
sock.listen(1)

print 'Listening for connection...'

# Accept a single connection and make a file like object out of it
# TODO: allow multiple client connections using threading.
connection = sock.accept()[0].makefile('rb')
print 'Connection established!'

try:
	while True:
		# Read the length of the image as a 32-bit unsigned int. If the
		# length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break
		
		# Construct a stream to hold the image data and read image data from the
		# connection
		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))

		# Rewind the stream and open it as an image with PIL
		image_stream.seek(0)
		image = Image.open(image_stream)
		image.show()
finally:
	print 'Closing the connection.'
	connection.close()
	sock.close()
