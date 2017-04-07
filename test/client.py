import socket
import sys

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to the port
server_address = ('localhost', 8000)
print 'start up on  %s port %s' % server_address
sock.connect(server_address)

try:
	while True:
		data = raw_input("Client: ")
		sock.sendall(data)
		recvData = sock.recv(256)
		print 'Server: %s' %recvData
		if (data == '#'):
			break;
finally:
	print 'Closing socket'
	sock.close()
