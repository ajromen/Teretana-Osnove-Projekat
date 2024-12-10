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


def dodaj_rezervaciju(id_rezervacije,id_korisnika,id_termina,oznaka_reda_kolone,datum):
    pass

def azuriraj_rezervaciju(id_rezervacije,id_korisnika=None,id_termina=None,oznaka_reda_kolone=None,datum=None):
    pass

def obrisi_rezervaciju(id_rezervacije):
    cursor=BazaPodataka.get_cursor()
    #rezeracije se ne brisu sem ako su u buducnosti
    danas = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute("DELETE FROM Rezervacija WHERE datum>? AND id_rezervacije=?",(danas,id_rezervacije,))
    BazaPodataka.commit()
    
