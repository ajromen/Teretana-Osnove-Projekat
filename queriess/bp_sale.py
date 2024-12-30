from bp_import import *

'''Sala
id_sale         INTEGER PRIMARY KEY NOT NULL,
naziv           CHAR(15),
broj_redova     SMALLINT,
oznaka_mesta    CHAR(15),
obrisana        BOOLEAN
'''

def dodaj_salu(id_sale,naziv,broj_redova,oznaka_mesta,obrisana):
    pass

def izmeni_salu(id_sale,naziv=None,broj_redova=None,oznaka_mesta=None,obrisana=None):
    pass

def obrisi_salu(id_sale):
    pass

def get_sala(id_sale):
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT
                    naziv,
                    broj_redova,
                    oznaka_mesta
                FROM Sala
                WHERE id_sale=?'''
    cursor.execute(komanda,(id_sale,))
    return cursor.fetchone()

def get_mesta(id_sale,id_termina,id_rezervacije=None):
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT 
                    Rezervacija.oznaka_reda_kolone 
                FROM Rezervacija
                JOIN Termin ON Rezervacija.id_termina=Termin.id_termina
                JOIN Trening ON Termin.id_treninga=Trening.id_treninga
                WHERE Trening.id_sale=? AND 
                      Termin.id_termina=?'''
    argumenti=(id_sale,id_termina,)
    if id_rezervacije is not None:
        komanda+='AND Rezervacija.id_rezervacije!=?'
        argumenti+=(id_rezervacije,)
    cursor.execute(komanda,argumenti)
    return cursor.fetchall()