import socket
import time
import struct
import json


# Create a TCP/IP socket

# Connect the socket to the port where the server is listening


groupsPositions = [
    (0,0,0,0,0,0),
    (0,1,0,0,0,0),
    (0,2,0,0,0,0),
    (0,3,0,0,0,0),
    (0,4,0,0,0,0),
    (0,5,0,0,0,0),
    (0,6,0,0,0,0),
    (0,7,0,0,0,0),
    (0,8,0,0,0,0),
    (0,9,0,0,0,0),
]



def send_message(type,n):

    if type == "box_position" :
        message = json.dumps(groupsPositions[n]).encode()
    elif type == "feedback" :
        message = n.encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    sock.sendall(message)

    print('closing socket')
    sock.close()