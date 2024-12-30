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

# "Šifra" : "id_rezervacije",
#             "Šifra termina" : "id_termina",
#             "Oznaka mesta" : "oznaka_reda_kolone",
#             "Datum" : "datum",
#             "Korisničko ime" : "id_korisnika",
#             "Instruktor" : "instruktor"

def dodaj_rezervaciju(id_korisnika,id_termina,oznaka_reda_kolone,datum):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("INSERT INTO Rezervacija (id_korisnika,id_termina,oznaka_reda_kolone,datum) VALUES (?,?,?,?)",(id_korisnika,id_termina,oznaka_reda_kolone,datum))
    BazaPodataka.commit()

def azuriraj_rezervaciju(id_rezervacije,id_korisnika=None,id_termina=None,oznaka_reda_kolone=None,datum=None):
    cursor=BazaPodataka.get_cursor()
    komanda='''UPDATE Rezervacija 
                SET 
                    id_korisnika=?,
                    id_termina=?,
                    oznaka_reda_kolone=?,
                    datum=?
                WHERE id_rezervacije=?'''
                    
    cursor.execute(komanda,(id_korisnika,id_termina,oznaka_reda_kolone,datum,id_rezervacije))

def obrisi_rezervaciju(id_rezervacije):
    cursor=BazaPodataka.get_cursor()
    cursor.execute("DELETE FROM Rezervacija WHERE id_rezervacije=?",(id_rezervacije,))
    BazaPodataka.commit()

def izlistaj_po_korisniku(kriterijum='id_rezervacije',pretraga="",id_korisnika=None):
    kriterijum,pretraga=helperFunctions.ocisti_string(kriterijum,pretraga)           
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT
                    Rezervacija.id_termina,
                    Termin.datum_odrzavanja,
                    Rezervacija.oznaka_reda_kolone,
                    Rezervacija.datum,
                    Korisnici.ime || ' ' || Korisnici.prezime AS instruktor,
                    Rezervacija.id_rezervacije
                FROM Rezervacija 
                JOIN Termin ON Rezervacija.id_termina=Termin.id_termina
                JOIN Trening ON Termin.id_treninga=Trening.id_treninga
                JOIN Program ON Trening.id_programa=Program.id_programa
                JOIN Korisnici ON Program.id_instruktora=Korisnici.username
            '''
    komanda += f''' WHERE {kriterijum} LIKE ? 
                        AND Rezervacija.id_korisnika = ?'''
    cursor.execute(komanda,('%'+pretraga+'%',id_korisnika,))
    return cursor.fetchall()

def izlistaj_po_instruktoru(kriterijum='id_rezervacije',pretraga="",instruktor=None):
    kriterijum,pretraga=helperFunctions.ocisti_string(kriterijum,pretraga)           
    cursor=BazaPodataka.get_cursor()
    komanda='''SELECT
                    Rezervacija.id_termina,
                    Termin.datum_odrzavanja,
                    Rezervacija.oznaka_reda_kolone,
                    Rezervacija.datum,
                    Korisnici.username || ' ' || Korisnici.ime || ' ' || Korisnici.prezime AS korisnik,
                    Rezervacija.id_rezervacije
                FROM Rezervacija 
                JOIN Termin ON Rezervacija.id_termina=Termin.id_termina
                JOIN Korisnici ON Rezervacija.id_korisnika=Korisnici.username
                JOIN Trening ON Termin.id_treninga=Trening.id_treninga
                JOIN Program ON Trening.id_programa=Program.id_programa
                '''
    komanda += f''' WHERE {kriterijum} LIKE ? 
                       AND Program.id_instruktora=?'''
                
    cursor.execute(komanda,('%'+pretraga+'%',instruktor,))
    return cursor.fetchall()