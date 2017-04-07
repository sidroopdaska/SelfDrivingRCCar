import socket
import sys

def handleConnection(connection, client_address):
	try:
		print 'connected to %s on port:%s' % (client_address[0], client_address[1])
		while True:
			data = connection.recv(256)
			print "Received: %s" % data
			if data == '#':
				break
			else:
				print 'Sending data back to the client'
				connection.sendall(data)
	finally:
		# clean up the connection
		connection.close()

		
# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to the port
server_address = ('10.166.38.64', 8000)
print 'start up on  %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# wait for a connection
	print 'Waiting for a connection...'
	connection, client_address = sock.accept()
	handleConnection(connection, client_address)
