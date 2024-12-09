from bp_import import *

'''Rezervacija
id_rezervacije      INTEGER PRIMARY KEY NOT NULL,
id_korisnika        CHAR(25),
id_termina          CHAR(6),
oznaka_reda_kolone  INTEGER,
datum               DATE,

FOREIGN KEY (id_korisnika) REFERENCES Korisnici(username)
FOREIGN KEY (id_termina) REFERENCES Termin(id_termina)
'''

def izbrisi_rezervaciju(id_rezervacije):
    pass

def dodaj_rezervaciju(id_rezervacije,id_korisnika,id_termina,oznaka_reda_kolone,datum):
    pass

def azuriraj_rezervaciju(id_rezervacije,id_korisnika=None,id_termina=None,oznaka_reda_kolone=None,datum=None):
    pass