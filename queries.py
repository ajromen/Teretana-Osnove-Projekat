import datetime
import os
import random
import sqlite3
import helperFunctions
import re

connection=sqlite3.connect("Teretana.db")
cursor=connection.cursor()


def executeScriptsFromFile(filename):
    file = open(filename, 'r', encoding='utf-8')
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
        helperFunctions.pisi_eror("Nalog sa korisničkim imenom već postoji")
        return 0
    password=helperFunctions.hashPassword(password)
    komanda='''INSERT INTO Korisnici(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(komanda, (username, password, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije))
    
    cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+username+"'")
    return cursor.fetchall()

def napraviGosta():
    random_id = random.randint(10000000, 99999999)
    username = f"guest_{random_id}"
    cursor.execute("SELECT username FROM Korisnici where username=?", (username,))
    if(cursor.fetchone() is None):
        datum=datetime.datetime.now().strftime("%Y-%m-%d")
        napraviNalog(username,"","","",-1,0,0,datum)
    return username

def  restartuj_bazu():
    executeScriptsFromFile("src/sql/Teretana.sql")
    executeScriptsFromFile("src/sql/TeretanaUnosPodataka.sql")

def obrisiKorisnika(username):
    if(username==""): return
    cursor.execute("DELETE FROM Korisnici WHERE username=?", (username,))

def azurirajNalog(stariUsername,username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije):
    cursor.execute("SELECT * FROM Korisnici WHERE username=?",(stariUsername,))
    if(len(cursor.fetchall())>0):
        password=helperFunctions.hashPassword(password)
        komanda=f'''UPDATE Korisnici 
                   SET username='{username}', password='{password}', ime='{ime}', prezime='{prezime}', uloga={uloga},status_clanstva={status_clanstva}, uplacen_paket={uplacen_paket}, datum_registracije='{datum_registracije}'
                   WHERE username='{stariUsername}';
                   '''
        cursor.execute(komanda)
        
        cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+username+"'")
        return cursor.fetchall()
    else:
        return napraviNalog(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)