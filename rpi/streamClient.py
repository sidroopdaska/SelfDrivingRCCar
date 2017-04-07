import io
import time
import picamera
import struct
import socket

client_socket = socket.socket()
print 'Starting connection'
client_socket.connect(('10.166.38.64', 8000))
print 'Connected to server'

connection = client_socket.makefile('wb')

try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)

    start = time.time()
    stream = io.BytesIO()

    for foo in camera.capture_continuous(stream, 'jpeg'):
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        if time.time() - start > 30:
            break
        stream.seek(0)
        stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    print 'Closing the connection'
    connection.close()
    client_socket.close()
