import datetime
import db_data_management
import alternative_cam as cam
import client
import time

# Grups will store the various groups into which the medicines are divided
groups =    [["A", "B", "C","D","E","F","G","H","I"], 
            ["J","K","L","M", "N", "Ñ","O", "P", "Q"], 
            ["R", "S", "T","U", "V", "W","X", "Y", "Z"] ]


# The file where the drugs to be replenished will be written is created.
# The name of the file will be in the format day-month-year_HourMinute in which the order is being prepared
date_and_time = datetime.datetime.now().strftime("%d-%m-%Y_%H%M")  
replenishment_list_filepath = r"C:\Users\calde\Desktop\UNI\TFG\src\replenishmentFiles\{}.txt".format(date_and_time)
replenishment_list = open(replenishment_list_filepath, "a")

# The list of commands to be prepared and the list of medicines that are no longer in stock are obtained
orders, replenishment = db_data_management.orders_to_be_prepared()

# The file of the list of medicines that are no longer in stock is updated
for med in replenishment:
    replenishment_list.write("- " + med + "\n")

print(f"\replenishment:{replenishment}")           
print(f"\norders:{orders}")        

# The robot is notified that the commands preparation is starting
client.send_message("I;")

numComanda = 0
#1. FOR TASK IN TASKS:
for order in orders:
    
    numComanda+=1
    print(f"\nComanda {numComanda} en proces...")

    #FOR GROUP IN GROUPS:
    for n, group in enumerate(groups):
        #print(n)

        # The medicines to be collected that belong to the group being processed are selected
        ST = [ELEMENT for ELEMENT in order if ELEMENT.startswith(tuple(group))]
        
        # If there are medicines of the group
        if len(ST) != 0:
            # The group to be processed is sent to the robot
            client.send_message("C;%s;" % n)   

            for element in ST:
                order.remove(element)
            print("Group "+str(group)+" "+str(ST))
            
            #client.send_message("box_position",n) # The position of the present group container is sent to the robot
            #client.send_message()

            time.sleep(30)
            #print("Dormo 30s")

            cam.ferCalaix(ST) # Medicines from the current group are collected

            #client.send_message("A;")
print("All orders have been prepared! :)")