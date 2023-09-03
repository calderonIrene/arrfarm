import socket
import struct
import config

def send_message(message):
    """
    This function sends a message to a specified IP address and port using TCP, 
    and then receives the robot's joint configuration as a reply.

    Args:
        message (str): The message to be sent.

    Note:
        The `message` argument must be a non-null string.

    Returns:
        None
    """

    # Create a TCP client socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the specified IP address and port from config
    sock.connect((config.ROBOT_IP, config.ROBOT_PORT)) 

    # Convert the message to bytes
    message_bytes = message.encode()

    ### Send data 
    print("I'm sending:", message_bytes)

    sock.send(message_bytes)

    ### Receive data
    while True:
        d = sock.recv(24).decode()
        if d.strip():  # Checks if the string contains anything other than white spaces
            break

    print("Feedback is received from robot")
    
    # Close the socket
    sock.close()


