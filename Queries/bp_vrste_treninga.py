from bp_import import *

'''Vrste_treninga 
id_vrste_treninga   INTEGER PRIMARY KEY NOT NULL,
naziv               BLOB,
obrisan             BOOLEAN
'''

def izlistaj_vrste_treninga(pretraga,kriterijum):
    pretraga=str(pretraga)
    kriterijum = kriterijum.strip()
    pretraga = pretraga.strip()

    komanda=''' SELECT * FROM Vrste_treninga WHERE '''
       
    komanda += f'''{kriterijum} LIKE ?;'''
    cursor.execute(komanda, ('%' + str(pretraga) + '%',))
    
    return cursor.fetchall()

def dodaj_vrstu_treninga(sifra,naziv):
    cursor.execute("SELECT * FROM Vrste_treninga WHERE id_vrste_treninga=?",(sifra,))
    if(len(cursor.fetchall())>0):
        helperFunctions.obavestenje("Vrsta treninga sa izabranom šifrom već postoji.")
        return 0
    komanda='''INSERT INTO Vrste_treninga(id_vrste_treninga, naziv)
	        VALUES	(?,?);'''
    cursor.execute(komanda, (sifra,naziv,))
    
def obrisi_vrste_treninga(id_vrste_treninga):
    komanda = "DELETE FROM Vrste_treninga WHERE id_vrste_treninga = ?"
    cursor.execute(komanda,(id_vrste_treninga,))
    connection.commit()