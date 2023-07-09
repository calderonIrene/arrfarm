import datetime
import db_data_management
import cam
import client

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
#1
for order in orders:
    #2
    numComanda+=1
    print(f"\nComanda {numComanda} en proces...")
    for n, group in enumerate(groups):
        print(n)
        #3
        ST = [ELEMENT for ELEMENT in order if ELEMENT.startswith(tuple(group))]
        if len(ST) != 0:
            for element in ST:
                order.remove(element)
            print("Group "+str(group)+" "+str(ST))
            client.send_message(n)

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
