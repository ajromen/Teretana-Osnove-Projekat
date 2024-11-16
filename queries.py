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
        helperFunctions.obavestenje("Nalog sa korisničkim imenom već postoji")
        return 0
    password=helperFunctions.hashPassword(password)
    komanda='''INSERT INTO Korisnici(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(komanda, (username, password, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije))
    
    cursor.execute("SELECT username, uloga FROM Korisnici WHERE username=?",(username,))
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
    connection.commit()

def obrisi_rezervaciju(id_rezervacije):
    if(id_rezervacije==None): return
    cursor.execute("DELETE FROM Rezervacija WHERE id_rezervacije=?", (id_rezervacije,))
    connection.commit()

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
    
def izlistaj_programe(pretraga,kriterijum,potrebanPaket,id_programa,naziv,naziv_vrste_treninga,trajanjeOd,trajanjeDo,instruktor):
    kriterijum = kriterijum.strip()
    pretraga = pretraga.strip()
    id_programa = id_programa.strip()
    naziv = naziv.strip()
    naziv_vrste_treninga = naziv_vrste_treninga.strip()
    instruktor = instruktor.strip()

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
       
    komanda += f''' WHERE {kriterijum} LIKE ? 
                        AND id_programa LIKE ? 
                        AND naziv_programa LIKE ? 
                        AND naziv_vrste_treninga LIKE ?
                        AND trajanje >= ?
                        AND trajanje <= ?
                        AND instruktor_ime LIKE ?'''
    if(potrebanPaket==0):
        komanda += "AND potreban_paket = 0"
    cursor.execute(komanda, ('%' + str(pretraga) + '%','%' + str(id_programa) + '%','%' + str(naziv) + '%','%' + str(naziv_vrste_treninga) + '%', trajanjeOd,trajanjeDo,'%' + str(instruktor) + '%',))

    return cursor.fetchall()

def obrisi_goste():
    danas = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute('''SELECT 
                            Rezervacija.id_rezervacije,
                            Korisnici.username
                        FROM 
                            Rezervacija
                        JOIN 
                            Korisnici ON Rezervacija.id_korisnika = Korisnici.username
                        WHERE 
                            Korisnici.uloga = -1 AND Rezervacija.datum < ?
                    ''',(danas,))
    usernames=cursor.fetchall()
    
    for gost in usernames:
        obrisi_rezervaciju(gost[0])
        obrisiKorisnika(gost[1])
    
    cursor.execute('''SELECT 
                            Korisnici.username
                        FROM
                            Korisnici
                        LEFT JOIN 
                            Rezervacija ON Korisnici.username = Rezervacija.id_korisnika
                        WHERE 
                            Korisnici.uloga = -1 AND Rezervacija.id_korisnika IS NULL
    ''')
    gosti_bez_rezervacije = cursor.fetchall()

    for gost in gosti_bez_rezervacije:
        obrisiKorisnika(gost[0])
        
def azuriraj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis):
    cursor.execute("SELECT * FROM Vrste_treninga WHERE id_vrste_treninga=?",(vrsta_treninga,))
    if(len(cursor.fetchall())==0): 
        helperFunctions.obavestenje("Ne postoji odabrana vrsta treninga.")
        return True
    cursor.execute("SELECT * FROM Korisnici WHERE username=?",(instruktor,))
    if(len(cursor.fetchall())==0): 
        helperFunctions.obavestenje("Ne postoji odabrani instruktor.")
        return True
    
    cursor.execute('''UPDATE Program 
                        SET 
                            naziv=?,
                            id_vrste_treninga=?,
                            trajanje=?,
                            id_instruktora=?,
                            potreban_paket=?,
                            opis=?
                        WHERE id_programa=?''',(naziv,vrsta_treninga,trajanje,instruktor,paket,opis,id))
    return False
    
def dodaj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis):
    cursor.execute("SELECT * FROM Vrste_treninga WHERE id_vrste_treninga=?",(vrsta_treninga,))
    if(len(cursor.fetchall())==0): 
        helperFunctions.obavestenje("Ne postoji odabrana vrsta treninga.")
        return True
    cursor.execute("SELECT * FROM Korisnici WHERE username=?",(instruktor,))
    if(len(cursor.fetchall())==0): 
        helperFunctions.obavestenje("Ne postoji odabrani instruktor.")
        return True
    cursor.execute("SELECT * FROM Program WHERE id_programa=?",(id,))
    if(len(cursor.fetchall())>0): 
        helperFunctions.obavestenje("Već postoji korisnik sa datom šifrom.")
        return True
    
    cursor.execute('''INSERT INTO Program(id_programa, naziv, id_vrste_treninga, trajanje, id_instruktora, potreban_paket, opis)
	                  VALUES(?,?,?,?,?,?,?)''',(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis,))
    return False

def izlistaj_trening(pretraga,kriterijum):
    pretraga=str(pretraga)
    kriterijum = kriterijum.strip()
    pretraga = pretraga.strip()

    komanda=''' SELECT 
                    Trening.id_treninga AS id_treninga,
                    Sala.naziv AS naziv_sale,
                    Trening.vreme_pocetka AS vreme_pocetka,
                    Trening.vreme_kraja AS vreme_kraja,
                    Trening.dani_nedelje AS dani,
                    Program.naziv AS naziv_programa,
                    Sala.id_sale AS sifra_sale,
                    Program.id_programa AS sifra_programa
                FROM 
                    Trening
                JOIN 
                    Program ON Trening.id_programa = Program.id_programa
                JOIN 
                    Sala ON Trening.id_sale = Sala.id_sale'''
       
    komanda += f''' WHERE {kriterijum} LIKE ?'''
    cursor.execute(komanda, ('%' + str(pretraga) + '%',))
    
    return cursor.fetchall()

def dodaj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa):
    cursor.execute("SELECT * FROM Trening WHERE id_treninga=?",(id,))
    if(len(cursor.fetchall())>0): 
        helperFunctions.obavestenje("Već postoji trening sa datom šifrom.")
        return True
    
    cursor.execute('''INSERT INTO Trening(id_treninga, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa)
	                  VALUES(?,?,?,?,?,?)''',(id,id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa,))
    return False

def azuriraj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa):    
    cursor.execute('''UPDATE trening 
                        SET 
                            id_sale=?,
                            vreme_pocetka=?,
                            vreme_kraja=?,
                            dani_nedelje==?,
                            id_programa=?
                        WHERE id_treninga=?''',(id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa,id,))
    return False