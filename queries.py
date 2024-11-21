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
            
def napraviNalog(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine):
    cursor.execute("SELECT * FROM Korisnici WHERE username=?",(username,))
    if(len(cursor.fetchall())>0):
        helperFunctions.obavestenje("Nalog sa korisničkim imenom već postoji")
        return 0
    password=helperFunctions.hashPassword(password)
    komanda='''INSERT INTO Korisnici(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine)
	 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cursor.execute(komanda, (username, password, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije, obnova_clanarine))
    
    cursor.execute("SELECT username, uloga FROM Korisnici WHERE username=?",(username,))
    return cursor.fetchall()

def napraviGosta():
    random_id = random.randint(10000000, 99999999)
    username = f"guest_{random_id}"
    cursor.execute("SELECT username FROM Korisnici where username=?", (username,))
    if(cursor.fetchone() is None):
        datum=datetime.datetime.now().strftime("%Y-%m-%d")
        napraviNalog(username,"","","",-1,0,0,datum,None)
    return username

def restartuj_bazu():
    global connection, cursor
    try:
        connection.close()
    except e:
        pass

    if os.path.exists("Teretana.db"):
        os.remove("Teretana.db")

    connection = sqlite3.connect("Teretana.db")
    cursor = connection.cursor()

    executeScriptsFromFile("src/sql/Teretana.sql")
    executeScriptsFromFile("src/sql/TeretanaUnosPodataka.sql")
    connection.commit()
    print("Baza uspesno resetovana")
    

def obrisiKorisnika(username):
    if(username==""): return
    cursor.execute("DELETE FROM Korisnici WHERE username=?", (username,))
    connection.commit()

def obrisi_rezervaciju(id_rezervacije):
    if(id_rezervacije==None): return
    cursor.execute("DELETE FROM Rezervacija WHERE id_rezervacije=?", (id_rezervacije,))
    connection.commit()

def azurirajNalog(stariUsername,username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine):
    cursor.execute("SELECT * FROM Korisnici WHERE username=?",(stariUsername,))
    if(len(cursor.fetchall())>0):
        password=helperFunctions.hashPassword(password)
        komanda='''UPDATE Korisnici 
                    SET username=?, 
                        password=?, 
                        ime=?, 
                        prezime=?, 
                        uloga=?,
                        status_clanstva=?,
                        uplacen_paket=?,
                        datum_registracije=?,
                        obnova_clanarine=?
                   WHERE username=?;
                   '''
        cursor.execute(komanda,(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine,stariUsername,))
        
        cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+username+"'")
        return cursor.fetchall()
    else:
        return napraviNalog(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)
    
def izlistaj_programe(pretraga,kriterijum,potrebanPaket,id_programa,naziv,naziv_vrste_treninga,trajanjeOd,trajanjeDo,instruktor):
    kriterijum=str(kriterijum)
    pretraga=str(pretraga)
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
def izlistaj_korisnike(pretraga,kriterijum):
    pretraga=str(pretraga)
    kriterijum = kriterijum.strip()
    pretraga = pretraga.strip()

    komanda=''' SELECT 
                    username,
                    ime,
                    prezime,
                    CASE 
                        WHEN status_clanstva = 0 THEN 'Neaktiviran'
                        WHEN status_clanstva = 1 THEN 'Aktiviran'
                    END AS status_clanstva,
                    CASE 
                        WHEN uplacen_paket = 0 THEN 'Standard'
                        WHEN uplacen_paket = 1 THEN 'Premium'
                    END AS uplacen_paket,
                    datum_registracije,
                    obnova_clanarine
                FROM 
                    Korisnici
                WHERE uloga=0 AND '''
       
    komanda += f'''{kriterijum} LIKE ?;'''
    cursor.execute(komanda, ('%' + str(pretraga) + '%',))
    
    return cursor.fetchall()

def izlistaj_instruktore_admine(pretraga,kriterijum):
    pretraga=str(pretraga)
    kriterijum = kriterijum.strip()
    pretraga = pretraga.strip()

    komanda=''' SELECT 
                    username,
                    ime,
                    prezime,
                    CASE 
                        WHEN uloga = 1 THEN 'Instruktor' 
                        ELSE 'Administrator' 
                    END AS uloga,
                    datum_registracije
                FROM 
                    Korisnici
                WHERE uloga>0 AND '''
       
    komanda += f'''{kriterijum} LIKE ?;'''
    cursor.execute(komanda, ('%' + str(pretraga) + '%',))
    
    return cursor.fetchall()

def broj_rezervacija_za_mesec(username):
    username=str(username)
    username.strip()
    komanda = """
        SELECT COUNT(*) FROM 
            Rezervacija
        JOIN 
            Korisnici ON Rezervacija.id_korisnika = Korisnici.username
        WHERE 
            Rezervacija.id_korisnika = ? AND
            
            Rezervacija.datum > Korisnici.obnova_clanarine AND
            Rezervacija.datum <= DATE('now') AND
            Rezervacija.datum <= DATE(Korisnici.obnova_clanarine, '+1 month');
        """
    
    cursor.execute(komanda, (username,))
    vrati = cursor.fetchone()
    return vrati[0]

def proveri_status_korisnika():
    komanda="SELECT * FROM Korisnici WHERE uloga=0 AND obnova_clanarine<DATE('now', '-1 month')"
    cursor.execute(komanda)
    korisnici=cursor.fetchall()
    if(len(korisnici)==0): return
    for korisnik in korisnici:
        komanda="UPDATE Korisnici SET status_clanstva=0,uplacen_paket=0,obnova_clanarine='1970-01-01' WHERE username=?"
        cursor.execute(komanda,(korisnik[0],))
        
def nagradi_lojalnost(username):
    komanda='''UPDATE Korisnici
                SET 
                    status_clanstva = 1,
                    uplacen_paket = 1,
                    obnova_clanarine = CASE
                        WHEN obnova_clanarine IS NOT NULL AND obnova_clanarine > DATE('now', '-1 month')
                            THEN DATE(obnova_clanarine, '+1 month')
                        ELSE DATE('now')
                    END
                WHERE username = ?;'''
    cursor.execute(komanda,(username,))
    connection.commit()

def aktiviraj_paket(username,paket):
    komanda='''UPDATE Korisnici
                SET 
                    status_clanstva = 1,
                    uplacen_paket = ?,
                    obnova_clanarine = DATE('now')
                WHERE username = ?;'''
    
    cursor.execute(komanda, (paket,username,))
    connection.commit()
