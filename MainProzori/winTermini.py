from datetime import timedelta
from imports import *
import bp_termini

class TerminiWindow:
    def __init__(self, window, main_window, uloga):
        self.window = window
        self.main_window = main_window
        self.current_canvas = None
        self.uloga = uloga
        self.dani_map = {
            "Monday": "Ponedeljak",
            "Tuesday": "Utorak",
            "Wednesday": "Sreda",
            "Thursday": "Četvrtak",
            "Friday": "Petak",
            "Saturday": "Subota",
            "Sunday": "Nedelja"
        }

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)

        wid.create_button(self.current_canvas, "./src/img/Widget/btnExit.png", 812, 9, 33, 33, lambda: self.main_window.unisti_trenutni_win())
        wid.create_button(self.current_canvas, "./src/img/Widget/btnSearch.png", 358, 53, 33, 33, self.pretrazi)
        
        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/searchPozadina.png", 23, 53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/tabelaPozadina_duza.png",23,102)
        
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
        
        self.entrySearch = wid.create_entry_search(self.current_canvas, self.pretrazi)

        self.current_canvas.create_text(610, 65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch = wid.create_comboBox(self.current_canvas, self.kriterijumi, x=681, y=53)  
        
        self.cmbbxSedmica = wid.create_comboBox(self.current_canvas, ["Ova nedelja", "Sledeća nedelja","SVE"], x=423, y=53)
        
        tabela_hieight=470
        self.table = wid.create_table(self.current_canvas, self.popuni_tabelu, tuple(self.kriterijumi),height=tabela_hieight)
        self.table.column("Vrsta treninga", width=100)
        self.table.column("Naziv programa", width=100)
        self.table.column("Dan", width=70)
        

    def popuni_tabelu(self, tabela, kriterijum='id_termina', pretraga=""):
        for red in tabela.get_children():
            tabela.delete(red)

        podaci = self.izlistaj(kriterijum, pretraga)
        i = 0
        for podatak in podaci:
            podatak=list(podatak)
            dan = datetime.datetime.strptime(podatak[4], "%Y-%m-%d")
            dan=self.dani_map[dan.strftime("%A")]
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

