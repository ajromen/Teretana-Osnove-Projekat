from bp_import import *

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
                        Program.opis,
                        Program.obrisan AS Obrisan
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
    connection.commit()
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
    connection.commit()
    return False

def get_trajanje_range():
    cursor.execute("SELECT MIN(trajanje), MAX(trajanje) FROM Program")
    rez=cursor.fetchall()
    if(len(rez)!=0):rez=rez[0]
    if(len(rez)==2):
        return rez[0], rez[1]
    return 0, 0

def obrisi_program(id_programa):
    #oznaci program kao obrisan
    cursor.execute("UPDATE Program SET obrisan=TRUE WHERE id_programa = ?",(id_programa,))
        
    #cursor.execute("SELECT ",(id_programa,))
    
    connection.commit()