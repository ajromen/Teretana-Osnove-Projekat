from datetime import timedelta
from imports import *
import bp_termini


class TerminiWindow(winTemplate):
    def __init__(self, window, main_window=None, uloga=None, top_level=False,escfunk=None):
        if top_level:
            self.window=window
        else:
            super().__init__(window, main_window, uloga)

    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        self.create_entry_search(self.pretrazi)
        
        self.kriterijumi=["Šifra","Naziv programa","Vrsta treninga","Sala","Dan","Datum održavanja","Vreme početka","Vreme kraja","Potreban paket"]
        self.kriterijumiMap = {
            "Šifra": "Termin.id_termina",
            "Naziv programa": "Program.naziv",
            "Vrsta treninga": "Vrste_treninga.naziv",
            "Sala": "Sala.naziv",
            "Dan": "Termin.datum_odrzavanja",
            "Datum održavanja": "Termin.datum_odrzavanja",
            "Vreme početka": "Trening.vreme_pocetka",
            "Vreme kraja": "Trening.vreme_kraja",
            "Potreban paket": "Program.potreban_paket"
        }
        
        self.create_entry_search(self.pretrazi)

        opcije=[kriterijum for kriterijum in self.kriterijumi if kriterijum != "Dan"]
        self.create_cmbbxSearch(opcije,)
        self.cmbbxSedmica = self.create_comboBox(["Ova nedelja", "Sledeća nedelja","SVE"], 423, 53)
        
        self.create_table(self.kriterijumi, velika=True)
        self.table.column("Vrsta treninga", width=100)
        self.table.column("Naziv programa", width=100)
        self.table.column("Dan", width=70)
        self.table.column("Sala", width=70)
        self.table.column("Vreme kraja", width=70)
        self.table.column("Vreme početka", width=90)
        

    def popuni_tabelu(self, tabela, kriterijum='id_termina', pretraga=""):
        for red in tabela.get_children(): tabela.delete(red)

        podaci = self.izlistaj(kriterijum, pretraga)
        i = 0
        for podatak in podaci:
            podatak=list(podatak)
            dan = datetime.datetime.strptime(podatak[4], "%Y-%m-%d")
            dan = helperFunctions.eng_dani_u_srp(dan.strftime("%A"))
            if(podatak[7]):
                podatak[7]="Premium"
            else:
                podatak[7]="Standard"
                
            podatak.insert(4, dan)
            if podatak[9] == 1:
                if self.uloga == "admin":
                    tabela.insert("", "end", values=podatak, tags="obrisano" + str(i % 2))
            else:
                tabela.insert("", "end", values=podatak, tags=str(i % 2))
            i += 1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        if not kriterijum:
            helperFunctions.obavestenje("Prvo izaberite kriterijum pretrage.")
            return

        for red in self.table.get_children():
            self.table.delete(red)

        if pretraga =="" or pretraga=="pretraži":
            pretraga=""
        else:
            if pretraga in "premium":
                pretraga = 1
            elif pretraga in "standard":
                pretraga = 0  
            else:
                pass

        self.popuni_tabelu(self.table, pretraga=pretraga, kriterijum=kriterijum)

    def izlistaj(self, kriterijum='id_termina', pretraga=""):
        sedmica = self.cmbbxSedmica.get()
        danas = datetime.date.today()
        pocetni_datum = None
        krajnji_datum = None

        if sedmica == "Ova nedelja":
            pocetni_datum = danas
            krajnji_datum = pocetni_datum + timedelta(days=6)
        elif sedmica == "Sledeća nedelja":
            pocetni_datum = danas + timedelta(days=7)
            krajnji_datum = pocetni_datum + timedelta(days=6)

        return bp_termini.izlistaj_termini(pretraga, kriterijum, pocetni_datum, krajnji_datum)
    
    

