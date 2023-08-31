import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
import zxing
import client
import time

def is_in_orderList(productName, orderList):
    # The product (productName) is searched in the order list (orderList)
    # PRE: productName and orderList are not null
    # POST: If the product productName is found, returns the index of the item in the list orderList
    for i, productinOL in enumerate(orderList):
        if productName.upper() == productinOL.upper():
            return i
    return -1


def update_orderList(product, pos, orderList):
    # Remove the product from the order list
    # PRE: The order list is not null and the product is present in it
    # POST: The product has been removed from the list
    orderList.pop(pos)
    print(f"The product {product} has been removed from the list")


'''
def read_barcodes(frame, orderList):
    # PRE: frame is the barcode information, orderList is the list of medications to be found
    # POST: The updated orderList is returned considering the newly scanned code


    barcodes = pyzbar.decode(frame)
    i = 0
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        
        # Check if the code has been scanned before
        barcode_info = barcode.data.decode('utf-8')

        # Write the name of the medication on the image
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

        if barcode_info in codis_llegits:
            continue

        # If it's a new code, add the name to the scanned codes
        codis_llegits.add(barcode_info)

        pos = is_in_orderList(barcode_info, orderList)
        
        # If the medication is one of the medications to be processed, update the orderList
        if pos != -1:
            update_orderList(barcode_info, pos, orderList)
            time.sleep(15)
            client.send_message("F;Y;")
            time.sleep(15)

        # Otherwise, print that it's not one of the products to be processed
        else:
            print(f"The product {barcode_info} is not found in the list")
            #client.send_message("feedback", "no")


    return frame
'''

def ferCalaix(ST):
    # Initialize an empty set to keep track of the scanned codes
    codis_llegits = set()
    # The camera starts (0 indicates that we will use the computer's main camera)
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    while len(ST):
        # A new image is read and processed with the read_barcodes function
        sucess, frame = camera.read()
        #frame = read_barcodes(frame, ST)
        for barcode in decode(frame):
            barcode_info = barcode.data.decode('utf-8')
            if barcode_info in codis_llegits:
                continue
            # If it's a new code, add the name to the scanned codes
            codis_llegits.add(barcode_info)

            pos = is_in_orderList(barcode_info, ST)

            # The image is shown
            #cv2.imshow('Barcode/QR code reader', frame)
            #if cv2.waitKey(1) & 0xFF == 27:
            #    break
        
            # If the medication is one of the medications to be processed, update the orderList
            if pos != -1:
                update_orderList(barcode_info, pos, ST)
                print("Feedback message is sent to the robot to pick up the medicine")
                client.send_message("F;Y;")
            
            # Otherwise, print that it's not one of the products to be processed
            else:
                print(f"The product {barcode_info} is not found in the list")
                print("Feedback message is sent to the robot to go and see the next medicine")
                client.send_message("F;N;")
         


    camera.release()
    cv2.destroyAllWindows()

