import cv2
from pyzbar import pyzbar
import os
from datetime import date

import db_data_management
import cam


groups =    [["A", "B", "C"], ["D","E","F"],["G","H","I"], 
            ["J","K","L"], ["M", "N", "Ñ"], ["O", "P", "Q"], 
            ["R", "S", "T"],["U", "V", "W"],["X", "Y", "Z"] ]

orders=[]

medicamentsPerDemanar = []

#replenishmentListfilepath = "C:\Users\calde\Desktop\UNI\TFG\code\replenishmentFiles\1"
#replenishmentList = open(replenishmentListfilepath, "a")

orders = db_data_management.comandesAPreparar()
        
print(f"\norders:{orders}")        

numComanda = 0
#1
for order in orders:
    #2
    numComanda+=1
    print(f"\nComanda {numComanda} en proces...")
    for group in groups:


        #3
        ST = [ELEMENT for ELEMENT in order if ELEMENT.startswith(tuple(group))]
        if len(ST) != 0:
            for element in ST:
                order.remove(element)
            print("Group "+str(group)+" "+str(ST))

            cam.ferCalaix(ST)

print("Totes les comandes ja han estat preparades! :)")

'''
1. FOR TASK IN TASKS:
    2. FOR GROUP IN GROUPS:
        3. ST = SUBLIST OF TASK IN GROUP
        4. WHILE THERE'S IMG AND LEN(ST) != 0:
            5. IF LECTURE IS IN ST:
                CATCH MEDICINE (- REMOVE OF ST
                                - TAKE PHYSICAL MEDICINE
                                - BRING TO THE DROP-OFF SITE)
            NEXT POSITION
'''
