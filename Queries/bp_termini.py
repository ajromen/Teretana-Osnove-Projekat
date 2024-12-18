from bp_import import *
from bp_rezervacije import obrisi_rezervaciju

'''Termin
id_termina          CHAR(6) PRIMARY KEY NOT NULL,
datum_odrzavanja    DATE,
id_treninga         CHAR(4),
obrisan             BOOLEAN,

FOREIGN KEY (id_treninga) REFERENCES Trening(id_treninga)
'''

def izlistaj_termini(pretraga="", kriterijum="Termin.id_termina",start_date=None, end_date=None):
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
    
    if start_date and end_date:
        komanda += " AND Termin.datum_odrzavanja BETWEEN ? AND ?"
        parametri.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])

    cursor.execute(komanda, tuple(parametri))
    return cursor.fetchall()
    

def dodaj_termin(id_termina,datum_odrzavanja,id_treninga,obrisan):
    pass

def izmeni_termin(id_termina,datum_odrzavanja=None,id_treninga=None,obrisan=None):
    pass

def obrisi_termin(id_termina):
    cursor=BazaPodataka.get_cursor()
    danas = datetime.date.today().strftime("%Y-%m-%d")
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
        
    
    #ako se obrise termin u buducnosti onda treba da se obrise i rezervacija za taj termin
    #ako je termin iz proslosti on ne treba da se obrise ali ne treba ni rezervacija
    
    
    BazaPodataka.commit()

