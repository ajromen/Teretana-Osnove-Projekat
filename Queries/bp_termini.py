from bp_import import *
from bp_rezervacije import obrisi_rezervaciju

'''Termin
id_termina          CHAR(6) PRIMARY KEY NOT NULL,
datum_odrzavanja    DATE,
id_treninga         CHAR(4),
obrisan             BOOLEAN,

FOREIGN KEY (id_treninga) REFERENCES Trening(id_treninga)
'''

def dodaj_termin(id_termina,datum_odrzavanja,id_treninga,obrisan):
    pass

def izmeni_termin(id_termina,datum_odrzavanja=None,id_treninga=None,obrisan=None):
    pass

def obrisi_termin(id_termina):
    cursor=BazaPodataka.get_cursor()
    danas = datetime.date.today().strftime("%Y-%m-%d")
    #oznaci termin kao obrisan
    cursor.execute("UPDATE Termin SET obrisan=TRUE WHERE id_termina = ?",(id_termina,))
    
    #logicko brisanje svih rezervacija za termin
    cursor.execute("SELECT id_rezervacije,datum FROM Rezervacija WHERE id_termina=?",(id_termina,))
    id_rezervacije=cursor.fetchall()
    for rezervacija in id_rezervacije:
        datum_odrzavanja = datetime.datetime.strptime(rezervacija[1], "%Y-%m-%d").date()
        if(datum_odrzavanja>datetime.date.today()):
            cursor.execute("DELETE FROM Rezervacija WHERE id_rezervacije=?",(rezervacija[0],))
        obrisi_rezervaciju(rezervacija[0])
        
    cursor.execute("SELECT datum_odrzavanja FROM Termin WHERE id_termina=?", (id_termina,))
    termin = cursor.fetchone()
    if termin:
        datum_odrzavanja = datetime.datetime.strptime(termin[0], "%Y-%m-%d").date()
        if(datetime.date.today()<datum_odrzavanja):
            cursor.execute("DELETE FROM Termin WHERE id_termina=?", (id_termina,))
    
    BazaPodataka.commit()

