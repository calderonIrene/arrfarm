import datetime
import db_data_management
import cam
import client
#import subprocess

#subprocess.run(["python", "python_server.py"])

groups =    [["A", "B", "C"], ["D","E","F"],["G","H","I"], 
            ["J","K","L"], ["M", "N", "Ñ"], ["O", "P", "Q"], 
            ["R", "S", "T"],["U", "V", "W"],["X", "Y", "Z"] ]




# The file where the company's medicines to be refilled will be written is created
# The name of the file will be in the format day-month-year_HourMinute in which the order is being prepared
fecha_hora_actual_str = datetime.datetime.now().strftime("%d-%m-%Y_%H%M")  
replenishmentListfilepath = r"C:\Users\calde\Desktop\UNI\TFG\src\replenishmentFiles\{}.txt".format(fecha_hora_actual_str)
replenishmentList = open(replenishmentListfilepath, "a")

# The list of commands to be prepared and the list of medicines that are no longer in stock are obtained
orders, replenishment = db_data_management.comandesAPreparar()

# The file of the list of medicines that are no longer in stock is updated
for med in replenishment:
    replenishmentList.write("- " + med + "\n")

print(f"\replenishment:{replenishment}")           
print(f"\norders:{orders}")        

numComanda = 0
#1. FOR TASK IN TASKS:
for order in orders:
    
    numComanda+=1
    print(f"\nComanda {numComanda} en proces...")
    # 2. FOR GROUP IN GROUPS:
    for n, group in enumerate(groups):
        print(n)
        #3. ST = SUBLIST OF TASK IN GROUP
        ST = [ELEMENT for ELEMENT in order if ELEMENT.startswith(tuple(group))]
        # 4. WHILE LEN(ST) != 0:
        if len(ST) != 0:
            for element in ST:
                order.remove(element)
            print("Group "+str(group)+" "+str(ST))
            client.send_message("box_position",n) # The position of the present group container is sent to the robot

            cam.ferCalaix(ST) # Medicines from the current group are collected

print("Totes les comandes ja han estat preparades! :)")

'''

        
        
            5. IF LECTURE IS IN ST:
                CATCH MEDICINE (- REMOVE OF ST
                                - TAKE PHYSICAL MEDICINE
                                - BRING TO THE DROP-OFF SITE)
            NEXT POSITION
'''
