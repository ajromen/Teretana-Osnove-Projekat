from bp_import import BazaPodataka,datetime

# a) Lista rezervacija po datumu rezervacije
# b) Lista rezervacija po datumu termina
# c) Lista rezervacija po datumu rezervacije i instruktoru
# d) Broj rezervacija za dan u nedelji
# e) Broj rezervacija po instruktoru (30 dana)
# f) Broj realizovanih rezervacija po paketu
# g) Top 3 najpopularnija treninga
# h) Najpopularniji dan u nedelji (1 godina)


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
def d_izvestaj(dan_broj:int):#0..6->1..7
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
    
    cursor.execute(komanda, (str(dan_broj+1),))
    
    return cursor.fetchall()

# e) Broj rezervacija po instruktoru (30 dana)
# e. Ukupan broj rezervacije po instruktorima (za svakog instruktora) u
# poslednjih 30 dana. Sortirati prikazane instruktore po ukupnom broju
# ostvarenih rezervacija u njihovim terminima treninga.

def e_izvestaj():
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT 
                    Korisnici.username,
                    Korisnici.ime,
                    Korisnici.prezime
                FROM Korisnici
                WHERE Korisnici.uloga = 1
            '''
    cursor.execute(komanda)
    instruktori=cursor.fetchall()
    podaci=[]
    for instruktor in instruktori:
        instruktor=list(instruktor)
        komanda='''SELECT 
                        COUNT(*)
                    FROM Rezervacija
                    JOIN Termin ON Rezervacija.id_termina = Termin.id_termina
                    JOIN Trening ON Termin.id_treninga = Trening.id_treninga
                    JOIN Program ON Trening.id_programa = Program.id_programa
                    WHERE Program.id_instruktora = ? AND
                          Termin.datum_odrzavanja < date('now')
                '''
        cursor.execute(komanda,(instruktor[0],))
        instruktor.append(cursor.fetchone()[0])
        podaci.append(instruktor)
        
    return sorted(podaci,key=lambda x:x[3],reverse=True)

# f) Broj realizovanih rezervacija po paketu
# g) Top 3 najpopularnija treninga
# h) Najpopularniji dan u nedelji (1 godina)