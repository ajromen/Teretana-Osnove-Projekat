from bp_import import * 
from bp_trening import obrisi_trening

'''Program
id_programa         INTEGER PRIMARY KEY NOT NULL,
naziv               CHAR(30),
id_vrste_treninga   INTEGER,--
trajanje            SMALLINT,
id_instruktora      CHAR(25),--
potreban_paket      BOOLEAN,
opis                BLOB,
obrisan             BOOLEAN,

FOREIGN KEY (id_vrste_treninga) REFERENCES Vrste_treninga(id_vrste_treninga),
FOREIGN KEY (id_instruktora) REFERENCES Korisnici(username)
'''

def izlistaj_programe(pretraga,kriterijum,potrebanPaket,id_programa,naziv,naziv_vrste_treninga,trajanjeOd,trajanjeDo,instruktor,uloga,username):
    pretraga, kriterijum, id_programa, naziv, naziv_vrste_treninga, instruktor = helperFunctions.ocisti_string(
        pretraga, kriterijum, id_programa, naziv, naziv_vrste_treninga, instruktor
    )
    cursor=BazaPodataka.get_cursor()
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
                        Program.opis,
                        Program.obrisan AS Obrisan
                    FROM 
                        Program
                    JOIN Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga
                    JOIN Korisnici ON Program.id_instruktora = Korisnici.username'''
       
    komanda += f''' WHERE {kriterijum} LIKE ? 
                        AND id_programa LIKE ? 
                        AND naziv_programa LIKE ? 
                        AND naziv_vrste_treninga LIKE ?
                        AND trajanje >= ?
                        AND trajanje <= ?
                        AND instruktor_ime LIKE ?'''
    argumenti=(f'%{pretraga}%',f'%{id_programa}%',f'%{naziv}%',f'%{naziv_vrste_treninga}%',trajanjeOd,trajanjeDo,f'%{instruktor}%',)
    if(uloga=="instruktor"):
        komanda += "AND id_instruktora = ?"
        argumenti+=(username,)
    if(potrebanPaket==0):
        komanda += "AND potreban_paket = 0"
    cursor.execute(komanda, argumenti)

    return cursor.fetchall()

def azuriraj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT id_vrste_treninga FROM Vrste_treninga WHERE id_vrste_treninga=?",(vrsta_treninga,))
    if(cursor.fetchone() is None): 
        helperFunctions.obavestenje("Ne postoji odabrana vrsta treninga.",crveno=True)
        return True
    cursor.execute("SELECT username FROM Korisnici WHERE username=?",(instruktor,))
    if(cursor.fetchone() is None): 
        helperFunctions.obavestenje("Ne postoji odabrani instruktor.",crveno=True)
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
    BazaPodataka.commit()
    return False
    
def dodaj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT id_vrste_treninga FROM Vrste_treninga WHERE id_vrste_treninga=?",(vrsta_treninga,))
    if(cursor.fetchone() is None): 
        helperFunctions.obavestenje("Ne postoji odabrana vrsta treninga.",crveno=True)
        return True
    cursor.execute("SELECT username FROM Korisnici WHERE username=?",(instruktor,))
    if(cursor.fetchone() is None): 
        helperFunctions.obavestenje("Ne postoji odabrani instruktor.",crveno=True)
        return True
    cursor.execute("SELECT id_programa FROM Program WHERE id_programa=?",(id,))
    if(cursor.fetchone()): 
        helperFunctions.obavestenje("Već postoji korisnik sa datom šifrom.",crveno=True)
        return True
    
    cursor.execute('''INSERT INTO Program(id_programa, naziv, id_vrste_treninga, trajanje, id_instruktora, potreban_paket, opis)
	                  VALUES(?,?,?,?,?,?,?)''',(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis,))
    BazaPodataka.commit()
    return False

def get_trajanje_range():
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT MIN(trajanje), MAX(trajanje) FROM Program")
    rez=cursor.fetchall()
    if(len(rez)!=0):rez=rez[0]
    if(len(rez)==2):
        return rez[0], rez[1]
    return 0, 0

def obrisi_program(id_programa,totalno=False):
    cursor=BazaPodataka.get_cursor()
    #oznaci trening kao obrisan
    cursor.execute("UPDATE Program SET obrisan=TRUE WHERE id_programa = ?",(id_programa,))
    
    #logicko brisanje svih treninga
    cursor.execute("SELECT id_treninga FROM Trening WHERE id_programa=?",(id_programa,))
    id_treninga=cursor.fetchall()
    for trening in id_treninga:
        obrisi_trening(trening[0],totalno)
        
    if totalno:
        cursor.execute("DELETE FROM Program WHERE id_programa=?",(id_programa,))
    
    BazaPodataka.commit()
    
    
def get_trajanje(id_programa: str)->int:
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT trajanje FROM Program WHERE id_programa=?",(id_programa,))
    vrati=cursor.fetchone()
    return vrati[0]

def query_koriscene_vrste_treninga():
    return  '''SELECT DISTINCT Vrste_treninga.naziv FROM Program JOIN Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga WHERE Vrste_treninga.obrisan IS NOT TRUE'''
    
def query_nazivi_neobrisanih():
    return  '''SELECT DISTINCT Program.naziv FROM Program WHERE Program.obrisan IS NOT TRUE'''
                    
def query_razliciti_instruktori():
    return """SELECT DISTINCT Korisnici.ime 
                FROM Program 
                JOIN Korisnici ON Program.id_instruktora = Korisnici.username 
                WHERE Korisnici.username IS NOT 'obrisan_korisnik'"""
                
def query_neobrisani_korisnici():
    return "SELECT id_programa FROM Program WHERE obrisan IS NOT TRUE"