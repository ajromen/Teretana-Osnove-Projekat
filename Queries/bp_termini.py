from datetime import timedelta
import string
from bp_import import *
from bp_rezervacije import obrisi_rezervaciju

'''Termin
id_termina          CHAR(6) PRIMARY KEY NOT NULL,
datum_odrzavanja    DATE,
id_treninga         CHAR(4),
obrisan             BOOLEAN,

FOREIGN KEY (id_treninga) REFERENCES Trening(id_treninga)
'''

def izlistaj_termini(pretraga="", kriterijum="Termin.id_termina",pocetni_datum=None, krajnji_datum=None):
    cursor=BazaPodataka.get_cursor()

    pretraga,kriterijum = helperFunctions.ocisti_string(pretraga, kriterijum)

    komanda = f"""SELECT 
        Termin.id_termina, 
        Program.naziv, 
        Vrste_treninga.naziv, 
        Sala.naziv, 
        Termin.datum_odrzavanja, 
        Trening.vreme_pocetka, 
        Trening.vreme_kraja, 
        program.potreban_paket, 
        Termin.obrisan
    FROM 
        Termin
    JOIN 
        Trening ON Termin.id_treninga = Trening.id_treninga
    JOIN 
        Program ON Trening.id_programa = Program.id_programa
    JOIN 
        Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga
    JOIN 
        Sala ON Trening.id_sale = Sala.id_sale
    WHERE 
        {kriterijum} LIKE ?
    """
    
    parametri=[f'%{pretraga}%']
    
    if pocetni_datum and krajnji_datum:
        komanda += " AND Termin.datum_odrzavanja BETWEEN ? AND ?"
        parametri.extend([pocetni_datum.strftime('%Y-%m-%d'), krajnji_datum.strftime('%Y-%m-%d')])

    cursor.execute(komanda, tuple(parametri))
    return cursor.fetchall()
    

def dodaj_termin(id_termina,datum_odrzavanja,id_treninga,obrisan):
    pass

def izmeni_termin(id_termina,datum_odrzavanja=None,id_treninga=None,obrisan=None):
    pass

def obrisi_termin(id_termina,totalno=True):
    """ako se obrise termin u buducnosti onda treba da se obrise i rezervacija za taj termin
    ako je termin iz proslosti on ne treba da se obrise ali ne treba ni rezervacija"""
    cursor=BazaPodataka.get_cursor()
    #oznaci termin kao obrisan
    cursor.execute("UPDATE Termin SET obrisan=TRUE WHERE id_termina = ?",(id_termina,))
    
    cursor.execute("SELECT datum_odrzavanja FROM Termin WHERE id_termina=?", (id_termina,))
    datum_termina = cursor.fetchone()
    datum_odrzavanja = datetime.datetime.strptime(datum_termina[0], "%Y-%m-%d").date()
    
    if(datum_odrzavanja>datetime.date.today()):
        cursor.execute("SELECT id_rezervacije FROM Rezervacija WHERE id_termina=?",(id_termina,))
        rezervacije=cursor.fetchall()
        for rezervacija in rezervacije:
            obrisi_rezervaciju(rezervacija[0])
        cursor.execute("DELETE FROM Termin WHERE id_termina=?", (id_termina,))
        
    if totalno:
        cursor.execute("DELETE FROM Rezervacija WHERE id_termina=?", (id_termina,))
        cursor.execute("DELETE FROM Termin WHERE id_termina=?",(id_termina,))
    
    BazaPodataka.commit()

    
def generisi_termine(za_naredne_sedmice=2):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT id_treninga FROM Trening")
    
    treninzi=cursor.fetchall()
    dani_map = {
        "Pon": 0,
        "Uto": 1,
        "Sre": 2,
        "Čet": 3,
        "Pet": 4,
        "Sub": 5,
        "Ned": 6
    }
    
    danas = datetime.date.today()
    pocetni_datum = danas - timedelta(days=danas.weekday())
    krajnji_datum = danas + timedelta(days=za_naredne_sedmice*7-1)
    
    for trening in treninzi:
        trening=trening[0]
        cursor.execute("SELECT dani_nedelje FROM Trening WHERE id_treninga=? AND obrisan IS NOT TRUE",(trening,))
        dani=cursor.fetchone()
        if dani:
            dani=dani[0].strip().split(",")
            for dan in dani:
                if dan in dani_map:
                    pomeri_za = dani_map[dan]
                    trenutni_datum = pocetni_datum + timedelta(days=pomeri_za)
                    while trenutni_datum <= krajnji_datum:
                        if postoji_termin_za_datum(trenutni_datum,trening):
                            trenutni_datum += timedelta(days=7)
                            continue
                        id_termina = generisi_random_id(trening)
                        cursor.execute("INSERT INTO Termin (id_termina, id_treninga, datum_odrzavanja) VALUES (?, ?, ?)", (id_termina, trening, trenutni_datum.strftime('%Y-%m-%d')))
                        trenutni_datum += timedelta(days=7)
                        
    BazaPodataka.commit()

def generisi_random_id(trening):# nece raditi zbog postavke zadatka...
    cursor=BazaPodataka.get_cursor()
    while True:
        rand_slova = ''.join(random.choices(string.ascii_uppercase, k=2))
        id_termina = f"{trening}{rand_slova}"
        cursor.execute("SELECT 1 FROM Termin WHERE id_termina=?", (id_termina,))
        if not cursor.fetchone():
            break
    return id_termina

def postoji_termin_za_datum(datum: datetime,trening: str):
    datum=datum.strftime('%Y-%m-%d')
    cursor=BazaPodataka.get_cursor()
    cursor.execute("SELECT 1 FROM Termin WHERE datum_odrzavanja=? AND id_treninga=?",(datum,trening))
    if cursor.fetchone():
        return True
    return False

def get_sala(id_termina):
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT Trening.id_sale 
            FROM Termin 
            JOIN Trening ON Termin.id_treninga = Trening.id_treninga
            WHERE id_termina=?'''
    cursor.execute(komanda,(id_termina,))
    return cursor.fetchone()[0]