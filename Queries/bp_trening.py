from bp_import import *

'''Trening
id_treninga   CHAR(4) PRIMARY KEY NOT NULL,
id_sale       INTEGER, 
vreme_pocetka TIME,
vreme_kraja   TIME,
dani_nedelje  CHAR(28),
id_programa   INTEGER,
obrisan       BOOLEAN,

FOREIGN KEY (id_sale) REFERENCES Sala(id_sale)
FOREIGN KEY (id_programa) REFERENCES Program(id_programa)
'''

def izlistaj_trening(pretraga,kriterijum):
    pretraga=str(pretraga)
    kriterijum = kriterijum.strip()
    pretraga = pretraga.strip()

    komanda=''' SELECT 
                    Trening.id_treninga AS id_treninga,
                    Sala.naziv AS naziv_sale,
                    Trening.vreme_pocetka AS vreme_pocetka,
                    Trening.vreme_kraja AS vreme_kraja,
                    Trening.dani_nedelje AS dani,
                    Program.naziv AS naziv_programa,
                    Sala.id_sale AS sifra_sale,
                    Program.id_programa AS sifra_programa
                FROM 
                    Trening
                JOIN 
                    Program ON Trening.id_programa = Program.id_programa
                JOIN 
                    Sala ON Trening.id_sale = Sala.id_sale'''
       
    komanda += f''' WHERE {kriterijum} LIKE ?'''
    cursor.execute(komanda, ('%' + str(pretraga) + '%',))
    
    return cursor.fetchall()

def dodaj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa):
    cursor.execute("SELECT * FROM Trening WHERE id_treninga=?",(id,))
    if(len(cursor.fetchall())>0): 
        helperFunctions.obavestenje("Već postoji trening sa datom šifrom.")
        return True
    
    cursor.execute('''INSERT INTO Trening(id_treninga, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa)
	                  VALUES(?,?,?,?,?,?)''',(id,id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa,))
    connection.commit()
    return False

def azuriraj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa):
    cursor.execute('''UPDATE trening 
                        SET 
                            id_sale=?,
                            vreme_pocetka=?,
                            vreme_kraja=?,
                            dani_nedelje==?,
                            id_programa=?
                        WHERE id_treninga=?''',(id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa,id,))
    connection.commit()
    return False

def obrisi_trening(id_treninga):
    komanda = "DELETE FROM Trening WHERE id_treninga = ?"
    cursor.execute(komanda,(id_treninga,))
    connection.commit()