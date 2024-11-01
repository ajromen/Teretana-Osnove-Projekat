import sqlite3
connection=sqlite3.connect("Teretana.db")
cursor=connection.cursor()


def executeScriptsFromFile(filename):
    file = open(filename, 'r')
    sqlFile = file.read()
    file.close()

    sqlCommands = sqlFile.split(';')

    for i in range(0,len(sqlCommands)):
        try:
            cursor.execute(sqlCommands[i])
        except sqlite3.OperationalError as msg:
            print("Command skipped: ", msg," OVA KOMANDA:"+str(i))