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
                    SET username='{username}', 
                        password='{password}', 
                        ime='{ime}', 
                        prezime='{prezime}', 
                        uloga={uloga},
                        status_clanstva={status_clanstva},
                        uplacen_paket={uplacen_paket},
                        datum_registracije='{datum_registracije}'
                   WHERE username='{stariUsername}';
                   '''
        cursor.execute(komanda)
        
        cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+username+"'")
        return cursor.fetchall()
    else:
        return napraviNalog(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)
    
def izlistaj_programe(kriterijum='id_programa',pretraga="*",id='',naziv='',naziv_vrste_treninga='',trajanje_od=-100,trajanje_do=1000,instruktor='',potreban_paket=1):
    komanda=''' SELECT 
                    Program.id_programa,
                    Program.naziv AS naziv_programa,
                    Vrste_treninga.naziv AS naziv_vrste_treninga,
                    Program.trajanje || ' min' AS trajanje,
                    Korisnici.ime AS instruktor_ime,
                    CASE 
                        WHEN Program.potreban_paket = 0 THEN 'Standard'
                        WHEN Program.potreban_paket = 1 THEN 'Premium'
                    END AS potreban_paket,
                    Program.opis
                FROM 
                    Program
                JOIN 
                    Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga
                JOIN 
                    Korisnici ON Program.id_instruktora = Korisnici.username'''
    
    if (pretraga != "*"):
        komanda += f''' WHERE {kriterijum} LIKE ? 
                        AND id_programa LIKE ? 
                        AND naziv_programa LIKE ? 
                        AND naziv_vrste_treninga LIKE ?
                        AND trajanje >= ?
                        AND trajanje <= ?
                        AND instruktor_ime LIKE ?'''
        if(potreban_paket==0):
            komanda += "AND potreban_paket = 0"
        cursor.execute(komanda, ('%' + str(pretraga) + '%','%' + str(id) + '%','%' + str(naziv) + '%','%' + str(naziv_vrste_treninga) + '%', trajanje_od,trajanje_do,'%' + str(instruktor) + '%',))
    else:
        cursor.execute(komanda)
                            
    return cursor.fetchall()