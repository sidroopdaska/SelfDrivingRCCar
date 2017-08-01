""" streamClient.py: Script to stream jpeg format video over TCP/IP socket.
"""

import io
import time
import picamera
import struct
import socket
from rpi.utils import (server_address
                       )
# Create a TCP/IP socket and establish connection with
# the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Starting connection')


client_socket.connect(server_address)

print('Connected to server')

# Make a file-like object out of the client socket
connection = client_socket.makefile('wb')

# Since we are intending to process the frames after capture,
# rather than dealing with individual JPEG captures,
# its better to capture a video and decode the frames from the
# resulting file.
try:
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)      # pi camera resolution
    camera.framerate = 10               # 10 frames/sec
    time.sleep(2)                       # give 2 secs for the camera to initialise

    start = time.time()
    stream = io.BytesIO()

    # use video-port for captures
    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
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
    print('Closing the connection...')
    connection.close()
    client_socket.close()
    print('Connection closed')
