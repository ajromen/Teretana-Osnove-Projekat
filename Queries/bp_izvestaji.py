from bp_import import BazaPodataka,datetime

'''
a) Lista rezervacija po datumu rezervacije
b) Lista rezervacija po datumu termina
c) Lista rezervacija po datumu rezervacije i instruktoru
d) Broj rezervacija za dan u nedelji
e) Broj rezervacija po instruktoru (30 dana)
f) Broj realizovanih rezervacija po paketu
g) Top 3 najpopularnija treninga
h) Najpopularniji dan u nedelji (1 godina)
'''

#a) Lista rezervacija po datumu rezervacije
def a_izvestaj(datum:str):
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT 
                    Korisnici.ime,
                    Korisnici.prezime,
                    Rezervacija.datum,
                    Rezervacija.oznaka_reda_kolone,
                    Program.naziv
                FROM Rezervacija
                JOIN Korisnici ON Rezervacija.id_korisnika = Korisnici.username
                JOIN Termin ON Rezervacija.id_termina = Termin.id_termina
                JOIN Trening ON Termin.id_treninga = Trening.id_treninga
                JOIN Program ON Trening.id_programa = Program.id_programa
                WHERE Rezervacija.datum = ?
                '''
    cursor.execute(komanda,(datum,))
    
    return cursor.fetchall()

def b_izvestaj(datum:str):
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT 
                    Korisnici.ime,
                    Korisnici.prezime,
                    Termin.datum_odrzavanja,
                    Rezervacija.oznaka_reda_kolone,
                    Program.naziv
                FROM Rezervacija
                JOIN Korisnici ON Rezervacija.id_korisnika = Korisnici.username
                JOIN Termin ON Rezervacija.id_termina = Termin.id_termina
                JOIN Trening ON Termin.id_treninga = Trening.id_treninga
                JOIN Program ON Trening.id_programa = Program.id_programa
                WHERE Termin.datum_odrzavanja = ?
                '''
    cursor.execute(komanda,(datum,))
    
    return cursor.fetchall()

# c) Lista rezervacija po datumu rezervacije i instruktoru
def c_izvestaj(podaci:str):
    """Podaci su 'datum, instruktor'"""
    cursor=BazaPodataka.get_cursor()
    datum,instruktor=podaci.split(", ")
    komanda='''SELECT 
                    Korisnici.ime,
                    Korisnici.prezime,
                    Rezervacija.datum,
                    Rezervacija.oznaka_reda_kolone,
                    Program.naziv
                FROM Rezervacija
                JOIN Korisnici ON Rezervacija.id_korisnika = Korisnici.username
                JOIN Termin ON Rezervacija.id_termina = Termin.id_termina
                JOIN Trening ON Termin.id_treninga = Trening.id_treninga
                JOIN Program ON Trening.id_programa = Program.id_programa
                WHERE Rezervacija.datum = ? AND
                      Program.id_instruktora = ?
                '''
    cursor.execute(komanda,(datum,instruktor,))
    
    return cursor.fetchall()

# d) Broj rezervacija za dan u nedelji
def d_izvestaj(dan_broj:int):#0..6
    cursor = BazaPodataka.get_cursor()
    komanda = '''SELECT 
                    Korisnici.ime,
                    Korisnici.prezime,
                    Rezervacija.datum,
                    Rezervacija.oznaka_reda_kolone,
                    Program.naziv
                FROM Rezervacija
                JOIN Korisnici ON Rezervacija.id_korisnika = Korisnici.username
                JOIN Termin ON Rezervacija.id_termina = Termin.id_termina
                JOIN Trening ON Termin.id_treninga = Trening.id_treninga
                JOIN Program ON Trening.id_programa = Program.id_programa
                WHERE strftime('%w', Rezervacija.datum) = ?
                '''
    
    cursor.execute(komanda, (str(dan_broj),))
    
    return cursor.fetchall()

# e) Broj rezervacija po instruktoru (30 dana)
# f) Broj realizovanih rezervacija po paketu
# g) Top 3 najpopularnija treninga
# h) Najpopularniji dan u nedelji (1 godina)