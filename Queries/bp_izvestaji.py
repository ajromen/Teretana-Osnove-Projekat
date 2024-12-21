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


def a_izvestaj(datum:datetime):
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
    datum=datum.strftime("%Y-%m-%d")
    cursor.execute(komanda,(datum,))
    
    return cursor.fetchall()

def b_izvestaj(datum:datetime):
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT 
                    Korisnici.ime,
                    Korisnici.prezime,
                    Termin.datum,
                    Rezervacija.oznaka_reda_kolone,
                    Program.naziv
                FROM Rezervacija
                JOIN Korisnici ON Rezervacija.id_korisnika = Korisnici.username
                JOIN Termin ON Rezervacija.id_termina = Termin.id_termina
                JOIN Trening ON Termin.id_treninga = Trening.id_treninga
                JOIN Program ON Trening.id_programa = Program.id_programa
                WHERE Termin.datum = ?
                '''
    datum=datum.strftime("%Y-%m-%d")
    cursor.execute(komanda,(datum,))
    
    return cursor.fetchall()