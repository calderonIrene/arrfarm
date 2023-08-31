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
    n = sock.send(message_bytes)


    ### Receive data
    while True:
        d = sock.recv(24).decode()
        if d.strip():  # Verifica si la cadena contiene algo más que espacios en blanco
            break

    #print("Received data:", d)
    print("Feedback is received from robot")
    
    # Decodify it as 6 floats in big-endian format with 4 bytes each
    #joints = d.decode('utf-8')
    #print("Received value for each joint is: {}".format(joints))

    # Close the socket
    sock.close()





#########################################
################# TESTS #################
#########################################


#send_message_nou_format("A;")
#send_message("set-up")
#send_message("box-position", 0)
#send_message("other", 0)

#send_message_nou_format("F;Y;")
#time.sleep(30)
#send_message_nou_format("F;N;")
#time.sleep(30)
#send_message_nou_format("C;N;")

#send_message("C;3;")
#time.sleep(5)
#send_message("C;2;")
#time.sleep(5)
#send_message("C;0;")

#send_message("C;O;0;")