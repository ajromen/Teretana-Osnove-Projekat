import sqlite3
import os


connection = sqlite3.connect("Teretana.db")
cursor = connection.cursor()

def izvrsi_skripte_iz_fajla(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        sqlFile = file.read()

    sqlCommands = sqlFile.split(';')

    for i in range(0,len(sqlCommands)):
        try:
            cursor.execute(sqlCommands[i])
        except sqlite3.OperationalError as msg:
            print("Command skipped: ", msg," OVA KOMANDA:"+str(i))

def restartuj_bazu():
    global connection, cursor
    try:
        connection.close()
    except Exception:
        pass

    if os.path.exists("Teretana.db"):
        os.remove("Teretana.db")

    connection = sqlite3.connect("Teretana.db")
    cursor = connection.cursor()

    izvrsi_skripte_iz_fajla("src/sql/Teretana.sql")
    izvrsi_skripte_iz_fajla("src/sql/TeretanaUnosPodataka.sql")
    connection.commit()
    print("Baza uspesno resetovana")
