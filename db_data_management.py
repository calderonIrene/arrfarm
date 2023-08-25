import mysql.connector
from config import config
import os
from datetime import date

# SQL queries to access the database
#query_prescription requests for all the orders to be prepared
query_prescription = "SELECT * FROM prescription WHERE state = 'demanat'" 
#query_medicine_of_prescriptionX requests the id and stock of the medicines that are related to the prescription passed by parameter
query_medicine_of_prescriptionX = "SELECT idMedicine, amount FROM medicine_prescription WHERE idPrescription = %s" 
# query_medicineX requests the name and the stock of the medicine with the id passed by parameter
query_medicineX = "SELECT name, stock FROM medicine WHERE idMedicine = %s" 

# SQL queries to modify database
queryToModifyStock =  "UPDATE medicine SET stock = %s WHERE idMedicine = %s"


def make_query(query, param):
    """
    This function executes the requested query to the database

    Args:
        query (str): Query to be executed
        param (any): Parameters passed to the query

    Note:
        The `query` argument must be a non-null string.

    Returns:
        The result of making the query passed by parameter to the database
    """


    #cnx establishes a connection to the MySQL database using the provided configuration settings
    cnx = mysql.connector.connect(**config)
    # cursor is going to execute queries on the cnx connection
    cursor = cnx.cursor()
    
    if query == "allPrescription":
        cursor.execute(query_prescription)
    
    elif query == "queryMedicineOfPrescriptionX":
        cursor.execute(query_medicine_of_prescriptionX, param)
    
    elif query == "medicineALaBD":
        cursor.execute(query_medicineX, param)

    # results contains all the results of the query
    results = cursor.fetchall()

    # Connection is closed
    cursor.close()
    cnx.close()

    return results

def update_stock(param):
    """
    This function updates the stock of a product in the database.

    Args:
        param: Tuple containing the id of the product and the updated stock

    Note:
        Param must be a non-null tuple

    Returns:
        None
    """

    #cnx establishes a connection to the MySQL database using the provided configuration settings
    cnx = mysql.connector.connect(**config)
    # cursor is going to execute queries on the cnx connection
    cursor = cnx.cursor()

    # The query to modify the stock in the database is executed with the given parameters (param)
    cursor.execute(queryToModifyStock, param)

    # The changes to the database are commited
    cnx.commit()  
    
    # Connection is closed
    cursor.close()
    cnx.close()


def orders_to_be_prepared ():
    """
    Returns a list containing all the orders to be prepared in the following format:

        [[medicine 1, ...,  medicine n1], ..., [medicine 1, ...,  medicine nX]]

        Each sublist represents the list of medicines for each order.

        It also returns the list of medicines that the company needs to replenish.

    Args:
        None
        
    Returns:
        list: A list of lists, where each sublist contains the medicines for each order.
        list: A list of medicines that need to be replenished by the company.
        
    """

    orders=[]
    replenishmentList = []

    allPrescriptions = make_query("allPrescription",None)

    for prescription in allPrescriptions:
        thisRecipieList = [prescription[0]]

        name_of_delivery_note = (str(prescription[0])+"_"+str(prescription[1])+".txt")

        delivery_note_file_path = os.path.join("C:\\Users\\calde\\Desktop\\UNI\\TFG\\src\\deliveryNotes", str(name_of_delivery_note))
        print(delivery_note_file_path)
        
        output_folder = os.path.dirname(delivery_note_file_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        delivery_note = open(delivery_note_file_path, "w")

        delivery_note.write("ORDER PLACED BY: \n")
        delivery_note.write("PREPARED ON THE DAY: " + str(date.today()) +"\n")

        # ids_medicines_of_prescription stores all the ids of the medicines in the prescription
        ids_medicines_of_prescription = make_query("queryMedicineOfPrescriptionX", (prescription[0],))

        # ids_medicines_of_prescription[0] -> code of medicine
        # ids_medicines_of_prescription[1] -> amount of medicine
        
        # # if there are medicines ordered
        if ids_medicines_of_prescription:  
            # for each medicine ordered 
            for med_ordered in ids_medicines_of_prescription:

                # medicine_in_BD will save the current product
                medicine_in_BD =  make_query("medicineALaBD", (med_ordered[0],))
                
                # If the medicine is in stock:    
                if medicine_in_BD[0][1] != 0:
                    # If we can deliver the full amount of the medicine ordered:
                    if med_ordered[1] <= medicine_in_BD[0][1]: 
                        # delivered will store the amount of medication that will be served
                        delivered = med_ordered[1] 
                        # updated_stock will indicate the updated stock of that drug 
                        # after the order has been served.
                        updated_stock = medicine_in_BD[0][1] - med_ordered[1]

                    else: 
                        # If we are unable to deliver the full amount of the medicine
                        # The maximum number of products available will be served
                        delivered = medicine_in_BD[0][1]
                        updated_stock = 0

                    if updated_stock == 0:
                        # If the remaining stock of the drug is 0, 
                        # it will be noted in the list of drugs to be replenished
                        replenishmentList.append(medicine_in_BD[0][0])
                            
                    #  The delivery note of the order is updated with the information collected:
                    delivery_note.write("\nPRODUCT: " + str(medicine_in_BD[0][0])+"")
                    delivery_note.write("\nQUANTITAT DEMANADA: " + str(med_ordered[1]) + " --- QUANTITAT SERVIDA: " + str(delivered)+ "\n")
                    delivery_note.write("\n Ara tenim un stock total de: " + str(updated_stock)+ "\n")

                    #  The stock of the drug in the database is updated
                    update_stock((updated_stock, med_ordered[0]))

                    # The medicine is added to the order list
                    if delivered >= 0:
                        thisRecipieList.append(medicine_in_BD[0][0])
                        #thisRecipieList.append(medicine_in_BD[0][1])

                # If the order could not be served because we do not have the medicine in stock:
                else: 
                    # It is added to the list of products to be replenished
                    replenishmentList.append(medicine_in_BD[0][0])
                    # It is indicated on the delivery note
                    delivery_note.write("\nPRODUCT: " + str(medicine_in_BD[0][0])+"")
                    delivery_note.write("\nQUANTITAT DEMANADA: " + str(med_ordered[1]) + " --- QUANTITAT SERVIDA: 0\n")
                                    
        # If there are no medicines ordered
        else: 
            print("EMPTY")
        
        print(thisRecipieList)

        orders.append(thisRecipieList[1:])

    return orders, replenishmentList