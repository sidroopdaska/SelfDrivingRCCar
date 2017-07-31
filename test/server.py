"""server.py: Server side code for chat app using TCP/IP Sockets"""

import socket
from utils.utils import *

def handle_connection(connection, client_address):
	try:
		print('connected to {0} on port:{1}'.format(client_address[0], client_address[1]))
		while True:
			data = connection.recv(256)
			if data:
				print("Received: {0}".format(str(data)))
				connection.sendall(data)

				if data == b'#':
					print('Ending the current connection')
					break
				else:
					print('Sending data back to the client')
	finally:
		# clean up the connection
		connection.close()

if __name__ == '__main__':
	# create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind socket to the port
	print('start up on {0} port {1}'.format(server_address[0], server_address[1]))
	sock.bind(server_address)

	# Listen for incoming connections
	sock.listen(1)

	while True:
		# wait for a connection
		print('Waiting for a connection...')
		connection, client_address = sock.accept()
		handle_connection(connection, client_address)
