from bp_import import *
from bp_programi import obrisi_program

'''Korisnici
username            CHAR(25) PRIMARY KEY NOT NULL,
password            CHAR(64),
ime                 CHAR(25),
prezime             CHAR(25),
uloga               SMALLINT,
status_clanstva     BOOLEAN,
uplacen_paket       BOOLEAN,
datum_registracije  DATE,
obnova_clanarine    DATE,
obrisan             BOOLEAN
'''


def dodaj_korisnika(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine):
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

def dodaj_gosta():
    random_id = random.randint(10000000, 99999999)
    username = f"guest_{random_id}"
    cursor.execute("SELECT username FROM Korisnici where username=?", (username,))
    if(cursor.fetchone() is None):
        datum=datetime.datetime.now().strftime("%Y-%m-%d")
        dodaj_korisnika(username,"","","",-1,0,0,datum,None)
    return username

def obrisi_korisnika(username,instruktor=False):
    if(username==""): return False
    elif username.strip()=='obrisan_korisnik': 
        helperFunctions.obavestenje("Obrisani korisnik sluzi za evidenciju i nije ga dozvoljeno birsati.")
        return False
    
    #brisanje iz rezervacija ako je nekad u buducnosti
    danas = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute("DELETE FROM Rezervacija WHERE datum > ? AND id_korisnika=?", (danas,username))
    #brisanje instrkuktora iz rezervacija
    cursor.execute("UPDATE Rezervacija SET id_korisnika='obrisan_korisnik' WHERE id_korisnika=?", (username,))
    
    #brisanje programa ako je insktruktor
    if instruktor:
        cursor.execute("SELECT id_programa FROM Program WHERE id_instruktora=?",(username,))
        id_programa=cursor.fetchall()
        cursor.execute("UPDATE Program SET obrisan=TRUE, id_instruktora='obrisan_korisnik' WHERE id_instruktora = ?", (username,))
        for program in id_programa:
            obrisi_program(program[0])

    connection.commit()
    #brisanje iz baze
    cursor.execute("DELETE FROM Korisnici WHERE username=?", (username,))
    connection.commit()
    return True

def azuriraj_korisnika(stariUsername,username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine):
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
        return dodaj_korisnika(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)

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
        obrisi_korisnika(gost[1])
    
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
        obrisi_korisnika(gost[0])
        
    connection.commit()

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
        komanda="UPDATE Korisnici SET status_clanstva=0,uplacen_paket=0 WHERE username=?"
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
