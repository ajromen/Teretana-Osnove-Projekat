import bp_rezervacije
from imports import *

class winRezervacije(winTemplate):
    def __init__(self, window, main_window,uloga,username):
        super().__init__(window,main_window,uloga)
        self.username=username
        
    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        
        kriterijumi=["Šifra termina","Datum održavanja","Broj mesta","Datum rezervacije"]
        if self.uloga=="instruktor" or self.uloga=="admin":
            kriterijumi.append("Korisnik")#username ime i prezime
            self.create_button("./src/img/Widget/btnIzmeni.png",300,541,252,40,self.rezervacija_izmeni)
        else:
            kriterijumi.append("Instruktor")#ime i prezime
            self.create_button("./src/img/Widget/btnPregled.png",300,541,252,40,self.rezervacija_pregledaj)
        
        self.create_table(kriterijumi) 
        
        self.create_button("./src/img/Widget/btnObrisi.png", 576, 541, 252, 40, self.rezervacija_obrisi)
        self.create_button("./src/img/Widget/btnDodaj.png", 23, 541, 252, 40, self.rezervacija_dodaj)  
         
        self.kriterijumiMap={
            "Šifra termina" : "Rezervacija.id_termina",
            "Datum održavanja" : "Termin.datum_odrzavanja",
            "Broj mesta" : "Rezervacija.oznaka_reda_kolone",
            "Datum rezervacije" : "Rezervacija.datum",
            "Korisnik" : "korisnik",
            "Instruktor" : "instruktor"
        }
        
        self.create_entry_search(self.pretrazi)
        self.create_cmbbxSearch(kriterijumi)
        
    def rezervacija_dodaj(self):
        self.top_level=True
        self.create_top_level("Dodaj rezervaciju", 400, 300)
        self.top_level=False
    
    def rezervacija_izmeni(self):
        pass
    
    def rezervacija_obrisi(self):
        pass
    
    def rezervacija_pregledaj(self):
        pass
    
    def popuni_tabelu(self,tabela,kriterijum='username',pretraga=""):
        for red in tabela.get_children(): tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum=kriterijum,pretraga=pretraga)
        
        i=0
        for podatak in podaci:
            tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())

        for red in self.table.get_children():
            self.table.delete(red)
            
        if pretraga =="" or pretraga=="pretraži": pretraga=""
        
        self.popuni_tabelu(self.table,kriterijum=kriterijum,pretraga=pretraga)

    def izlistaj(self,kriterijum='id_rezervacije',pretraga=""):
        if self.uloga=="instruktor" or self.uloga=="admin":     
            return bp_rezervacije.izlistaj_po_instruktoru(kriterijum,pretraga,self.username)
        return bp_rezervacije.izlistaj_po_korisniku(kriterijum,pretraga,self.username)
       