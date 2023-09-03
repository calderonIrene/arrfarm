import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
import client


def is_in_orderList(productName, orderList):
    '''
    This function searches for the product name (passed in the first parameter) 
    in the list passed in the second parameter.

    Args:
        productName (str): The name to search.
        orderList ([str]): The list where search for the name of the medicine.

    Note:
        The `productName` argument must be a non-null string.

    Returns:
        If the product productName is found, the index of the item in the list orderList,
        otherwise -1
    '''

    for i, productinOL in enumerate(orderList):
        if productName.upper() == productinOL.upper():
            return i
    return -1

def ferCalaix(ST):

    '''
    Given a list of medicines, this function reads barcodes and updates the list as it sees the medicines appearing on the list.    
    Ends when the list gets empty.

    In addition, whenever it detects a medicine that is in the list, it uses the client to send feedback to the server.

    Args:
        ST ([str]): The list of medicines to search for.

    Returns:
        None
    '''

    # Initialize an empty set to keep track of the scanned codes
    scanned_codes = set()

    # The camera starts (0 indicates that we will use the computer's main camera)
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    while len(ST):
        # A new image is read and processed with the read_barcodes function
        success, frame = camera.read()
        
        for barcode in decode(frame):
            barcode_info = barcode.data.decode('utf-8')
            if barcode_info in scanned_codes:
                continue

            # If it's a new code, add the name to the scanned codes
            scanned_codes.add(barcode_info)

            pos = is_in_orderList(barcode_info, ST)

            # If the medication is one of the medications to be processed, update the orderList
            if pos != -1:
                ST.pop(pos)
                print(f"The product {barcode_info} has been removed from the list")
                
                print("Feedback message is sent to the robot to pick up the medicine")
                client.send_message("F;Y;")
            
            # Otherwise, it ignores it and asks the robot to go see the next medicine
            else:
                print(f"The product {barcode_info} is not found in the list")
                
                print("Feedback message is sent to the robot to go and see the next medicine")
                client.send_message("F;N;")
        
    # Release the camera resources
    camera.release()
    # Close all OpenCV windows
    cv2.destroyAllWindows()


