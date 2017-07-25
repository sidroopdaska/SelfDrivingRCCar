import socket
import sys

def handleConnection(connection, client_address):
	try:
		print('connected to {0} on port:{1}'.format(client_address[0], client_address[1]))
		while True:
			data = connection.recv(256)
			print("Received: {0}".format(str(data)))
			if data == b'#':
				break
			else:
				print('Sending data back to the client')
				connection.sendall(data)
	finally:
		# clean up the connection
		connection.close()


# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to the port
server_address = ('10.104.64.231', 45713)
print('start up on {0} port {1}'.format(server_address[0], server_address[1]))

sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
	# wait for a connection
	print('Waiting for a connection...')
	connection, client_address = sock.accept()
	handleConnection(connection, client_address)
