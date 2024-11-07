import sqlite3
import helperFunctions
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
            
def napraviNalog(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije):
    cursor.execute("SELECT * FROM Korisnici WHERE username=?",(username,))
    if(len(cursor.fetchall())>0):
        return "vecPostoji"
    password=helperFunctions.hashPassword(password)
    komanda='''INSERT INTO Korisnici(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(komanda, (username, password, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije))
    
    cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+username+"'")
    return cursor.fetchall()

def  restartuj_bazu():
    executeScriptsFromFile("src/sql/Teretana.sql")
    executeScriptsFromFile("src/sql/TeretanaUnosPodataka.sql")