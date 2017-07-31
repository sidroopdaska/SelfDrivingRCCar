"""client.py: Client side code for chat app using TCP/IP Sockets"""

import socket
from utils.utils import *

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
print("Connected to server")

try:
	while True:
		data = input("Client: ")
		sock.sendall(bytes(data, 'utf-8'))
		recvData = sock.recv(256)
		print(f'Server: {str(recvData)}')
		if recvData == b'#':
			break;
finally:
	print('Closing socket')
	sock.close()
