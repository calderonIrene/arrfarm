import datetime
import db_data_management
import cam
import client

# Grups will store the various groups into which the medicines are divided
groups =    [["A", "B", "C","D","E","F","G","H","I"], 
            ["J","K","L","M", "N", "Ñ","O", "P", "Q"], 
            ["R", "S", "T","U", "V", "W","X", "Y", "Z"] ]


### The file where the drugs to be replenished will be written is created

# The name of the file will be in the format day-month-year_HourMinute in which the order is being prepared
date_and_time = datetime.datetime.now().strftime("%d-%m-%Y_%H%M")  
replenishment_list_filepath = r"C:\Users\calde\Desktop\UNI\TFG\src\replenishmentFiles\{}.txt".format(date_and_time)
replenishment_list = open(replenishment_list_filepath, "a")

### The list of commands to be prepared and the list of medicines that are no longer in stock are obtained
orders, replenishment = db_data_management.orders_to_be_prepared()



# The file of the list of medicines that are no longer in stock is updated
for med in replenishment:
    replenishment_list.write("- " + med + "\n")


# The robot is notified that the commands preparation is starting
client.send_message("I;")


### The order preparation process begins

# Iterate over each order in the list of orders
for orderNum, order in enumerate(orders):
    print(f"\nProcessing Order {orderNum}...")

    # Iterate over each group in the list of groups
    for groupNum, group in enumerate(groups):

        # Select medicines to be collected from the order that belong to the current group
        medicines_to_collect = [element for element in order if element.startswith(tuple(group))]

        # Check if there are medicines from the current group to collect
        if len(medicines_to_collect) != 0:
            # Send the current group information to the robot for processing
            client.send_message("C;%s;" % groupNum)   

            # Remove collected medicines from the order
            for element in medicines_to_collect:
                order.remove(element)
            print(f"Collected Medicines in Group {groupNum}: {medicines_to_collect}")

            # Collect medicines from the current group using the 'cam' object
            cam.collect_medicines(medicines_to_collect)

# Notify that all orders have been prepared
client.send_message("A;")
print("All orders have been prepared! :)")
