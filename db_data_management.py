import mysql.connector
import config as c

# Configurem la info per conectarnos a la bd
config = {
    'user': c.db_user,
    'password': c.db_password,
    'host': 'localhost',
    'database': 'arrfarm',
    'raise_on_warnings': True
}


# Connecting to the database
config = c.config
cnx = mysql.connector.connect(**config)


# SQL queries to access the database
queryPrescription = "SELECT * FROM prescription WHERE state = 'demanat'" # Les comandes que s'han de preparar
queryMedicines = "SELECT * FROM medicine" # Tots els medicaments
queryMedicineOfPrescriptionX = "SELECT idMedicine, amount FROM medicine_prescription WHERE idPrescription = %s" # Medicament + quantitat demanada en la comanda X
queryMedicineX = "SELECT name, stock FROM medicine WHERE idMedicine = %s" # Nom i stock de la medicina seleccionada

# SQL queries to modify database
queryToModifyStock =  "UPDATE medicine SET stock = %s WHERE idMedicine = %s"


# Cursor will execute the SQL queries
cursor = cnx.cursor()


def fesConsulta(query, aux):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    if query == "allPrescription":
        cursor.execute(queryPrescription)
    
    elif query == "queryMedicineOfPrescriptionX":
        cursor.execute(queryMedicineOfPrescriptionX, aux)
    
    elif query == "medicineALaBD":
        cursor.execute(queryMedicineX, aux)

    results = cursor.fetchall()

    #Tanquem les conexions
    cursor.close()
    cnx.close()

    return results

def actualitzaStock(param):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(queryToModifyStock, param)
    cnx.commit()  # Add this line to commit the changes to the database
    
    #Tanquem les conexions
    cursor.close()
    cnx.close()

def comandesAPreparar ():
    orders=[]
    allPrescriptions = fesConsulta("allPrescription",0)

    for prescription in allPrescriptions:
        thisRecipieList = [prescription[0]]

        # Creem l'albaran corresponent a la comanda 
        #nameOfDeliveryNote = (str(prescription[0])+"_"+str(prescription[1])+".txt")
        #deliveryNotefilepath = os.path.join("C:\\Users\\calde\\Desktop\\UNI\\TFG\\code\\albarans", str(nameOfDeliveryNote))
        #deliveryNote = open(deliveryNotefilepath, "a")
        #deliveryNote.write("COMANDA FETA PER: \n")
        # deliveryNote.write("PREPARADA EL DIA: " + str(date.today()) +"\n")

        #idsMedicinesOfPrescription guarda totes les id dels medicaments de la recepta
        idsMedicinesOfPrescription = fesConsulta("queryMedicineOfPrescriptionX", (prescription[0],))

        # idsMedicinesOfPrescription[0] -> code of medicine
        # idsMedicinesOfPrescription[1] -> amount of medicine
        
        if idsMedicinesOfPrescription: # Si hi ha medicaments demanats
            for medDemanada in idsMedicinesOfPrescription: # Per cada un dels medicaments demanats

                # 1. medicineALaBD guardarà el medicament actual
                medicineALaBD =  fesConsulta("medicineALaBD", (medDemanada[0],))

                print(medicineALaBD[0][1])
                #print("Medicina demanada "+str(medDemanada))
                #print("Medicina en la bd "+str(medicineALaBD))
                
                # Si hi ha stock de la medicina:         
                if medicineALaBD[0][1] != 0:
                    if medDemanada[1] <= medicineALaBD[0][1]: # Si podem servir el 100% de la quantitat de medicament demanada
                        # Servirem indicarà la quantitat de medicament que servirem
                        servirem = medDemanada[1] 
                        # stockActual indicarà l'stock d'aquell medicament
                        # amb el que ens quedarem despres de servir la comanda
                        stockActual = medicineALaBD[0][1] - medDemanada[1]

                    else: # Si no tenim prou stock per servir al 100% la quantitat demanada
                        servirem = medicineALaBD[0][1]
                        stockActual = 0

                    if stockActual == 0:
                        # Si ens hem quedat sense stock al servir la comanda, 
                        # posarem el medicament a la llista de medicaments que s'han de demanar
                        #replenishmentList.write("- " + str(medicineALaBD[0][0])+ "\n")
                            
                    #  Actualizem albaran
                    #deliveryNote.write("\nPRODUCT: " + str(medicineALaBD[0][0])+"")
                    #deliveryNote.write("\nQUANTITAT DEMANADA: " + str(medDemanada[1]) + " --- QUANTITAT SERVIDA: " + str(servirem)+ "\n")
                    #deliveryNote.write("\n Ara tenim un stock total de: " + str(stockActual)+ "\n")
                        print("0")

                    #  Actualizem stock
                    actualitzaStock((stockActual, medDemanada[0]))

                    #  Posem la medicina a la llista de la comanda
                    if servirem >= 0:
                        thisRecipieList.append(medicineALaBD[0][0])
                        #thisRecipieList.append(medicineALaBD[0][1])

                
                #else: # Si no hi ha stock del medicament demanat
                    #Ho indiquem a l'albaran
                    #deliveryNote.write("\nPRODUCT: " + str(medicineALaBD[0][0])+"")
                    #deliveryNote.write("\nQUANTITAT DEMANADA: " + str(medDemanada[1]) + " --- QUANTITAT SERVIDA: 0\n")
                                    
        else: # No hi han medicaments demanats
            print("EMPTY")
        
        print(thisRecipieList)

        orders.append(thisRecipieList[1:])

    return orders
        