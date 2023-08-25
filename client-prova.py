import socket
import time
import struct


# Create a TCP/IP socket
setUpPos = [0.98, -1.78, 139.78, 167.65, 50.25, 129.58]
groupsPositions = [
    (56.27, 82.88, 81.57, -125.27, 78.27, 78.29, 123.68),
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

joint_1 = 0.98
joint_2 = -1.78
joint_3 = 139.78
joint_4 = 167.65
joint_5 = 50.25
joint_6 = 129.58

def send_message(type,n=None):

    joint_1 = 0.98
    joint_2 = -1.78
    joint_3 = 139.78
    joint_4 = 167.65
    joint_5 = 50.25
    joint_6 = 129.58


    message = b''  # Default empty bytes message
    if type == "set-up" :
        pos = setUpPos 
        joint_1 = pos[0]
        joint_2 = pos[1]
        joint_3 = pos[2]
        joint_4 = pos[3]
        joint_5 = pos[4]
        joint_6 = pos[5]

        print("Joint 1:", pos[0])
        print("Joint 2:", pos[1])
        print("Joint 3:", pos[2])
        print("Joint 4:", pos[3])
        print("Joint 5:", pos[4])
        print("Joint 6:", pos[5])

        message = struct.pack(">ffffff", pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
    
    elif type == "box-position" :
        #message = json.dumps(groupsPositions[n]).encode()
        pos = groupsPositions[n]
        joint_1 = pos[0]
        joint_2 = pos[1]
        joint_3 = pos[2]
        joint_4 = pos[3]
        joint_5 = pos[4]
        joint_6 = pos[5]

        print("Joint 1:", pos[0])
        print("Joint 2:", pos[1])
        print("Joint 3:", pos[2])
        print("Joint 4:", pos[3])
        print("Joint 5:", pos[4])
        print("Joint 6:", pos[5])

        message = struct.pack(">ffffff", pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

    elif type == "feedback" :
        message = n.encode()

    else:
        message = struct.pack(">ffffff", joint_1, joint_2, joint_3, joint_4, joint_5, joint_6)

    # Create a TCP client to ROBOT_IP:2001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('84.88.129.201', 2005)) 

    #Send data 
    print("I'm sennding: ", message)
    n = sock.send(message)
    print("send: {} bytes".format(n))
    time.sleep(0.1)

    sock.close()




def send_message_exmp():
    # Create a TCP client to ROBOT_IP:2001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('84.88.129.201', 2007)) 

    while True:
        message = struct.pack(">ffffff", joint_1, joint_2, joint_3, joint_4, joint_5, joint_6)
        #Send data 
        print("I'm sennding: ", message)
        n = sock.send(message)
        print("send: {} bytes".format(n))
        time.sleep(0.1)
    sock.close()
#send_message("set-up")
#send_message("box-position", 0)
#send_message("other", 0)

send_message_exmp()
