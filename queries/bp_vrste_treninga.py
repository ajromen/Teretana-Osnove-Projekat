from bp_import import *
from bp_programi import obrisi_program

'''Vrste_treninga 
id_vrste_treninga   INTEGER PRIMARY KEY NOT NULL,
naziv               BLOB,
obrisan             BOOLEAN
'''

def izlistaj_vrste_treninga(pretraga,kriterijum):
    cursor=BazaPodataka.get_cursor()
    kriterijum ,pretraga=helperFunctions.ocisti_string(
        kriterijum,pretraga
    )

    komanda=''' SELECT id_vrste_treninga FROM Vrste_treninga WHERE '''
    komanda += f'''{kriterijum} LIKE ?;'''
    cursor.execute(komanda, (f'%{pretraga}%',))
    return cursor.fetchall()

def dodaj_vrstu_treninga(sifra,naziv):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT id_vrste_treninga FROM Vrste_treninga WHERE id_vrste_treninga=?",(sifra,))
    if(cursor.fetchone()):
        helperFunctions.obavestenje("Vrsta treninga sa izabranom šifrom već postoji.")
        return 0
    komanda='''INSERT INTO Vrste_treninga(id_vrste_treninga, naziv)
	        VALUES	(?,?);'''
    cursor.execute(komanda, (sifra,naziv,))
    
def obrisi_vrste_treninga(id_vrste_treninga,totalno=False):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("UPDATE Vrste_treninga SET obrisan=TRUE WHERE id_vrste_treninga = ?",(id_vrste_treninga,))
    
    #logicko brisanje svih termina
    cursor.execute("SELECT id_programa FROM Program WHERE id_vrste_treninga=?",(id_vrste_treninga,))
    id_programa=cursor.fetchall()
    for program in id_programa:
        obrisi_program(program[0],totalno)
        
    if totalno:
        cursor.execute("DELETE FROM Vrste_treninga WHERE id_vrste_treninga = ?",(id_vrste_treninga,))
    
    BazaPodataka.commit()
    
def azuriraj_vrstu_treninga(id_vrste_treninga, naziv):
    cursor = BazaPodataka.get_cursor()
    komanda = '''UPDATE Vrste_treninga
                 SET naziv = ?
                 WHERE id_vrste_treninga = ?;'''
    cursor.execute(komanda, (naziv, id_vrste_treninga))
    BazaPodataka.commit()
    return False