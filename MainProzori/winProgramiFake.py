# MainProzori/winProgrami.py
import helperFunctions
from winTemplate import winTemplate
import bp_programi

class ProgramiWindow(winTemplate):
    def __init__(self, window, main_window, uloga):
        super().__init__(window, main_window, uloga)
        self.promenljive_filteri()

    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        # self.create_button("./src/img/Widget/btnFilteri.png", 687, 53, 142, 33, self.winProgramiFilteri)
        self.create_entry_search(self.pretrazi)
        self.kriterijumi = ["Šifra", "Naziv", "Vrsta treninga", "Trajanje", "Instruktor", "Potreban paket", "Opis"]
        self.kriterijumiMap = {
            "Šifra": "id_programa",
            "Naziv": "naziv_programa",
            "Vrsta treninga": "naziv_vrste_treninga",
            "Trajanje": "trajanje",
            "Instruktor": "instruktor_ime",
            "Potreban paket": "potreban_paket",
            "Opis": "opis"
        }
        self.create_table(self.kriterijumi)
        self.create_cmbbxSearch(self.kriterijumi,x=524,y=53)
        # if self.uloga == "admin":
        #     self.create_button("./src/img/Widget/btnDodaj.png", 23, 543, 252, 40, self.winProgrami_Dodaj)
        #     self.create_button("./src/img/Widget/btnIzmeni.png", 300, 543, 252, 40, self.winProgrami_Izmeni)
        #     self.create_button("./src/img/Widget/btnObrisi.png", 577, 543, 252, 40, self.obrisi_program)


    def popuni_tabelu(self, tabela, kriterijum='id_programa', pretraga=''):
        for red in tabela.get_children():
            tabela.delete(red)
        podaci = self.izlistaj_programe(kriterijum, pretraga)
        i = 0
        for podatak in podaci:
            if podatak[7] == 1:
                if self.uloga == "admin":
                    tabela.insert("", "end", values=podatak[:-1], tags="obrisano" + str(i % 2))
            else:
                tabela.insert("", "end", values=podatak[:-1], tags=str(i % 2))
            i += 1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        if not kriterijum:
            helperFunctions.obavestenje("Prvo izaberite kriterijum pretrage.")
            return
        for red in self.table.get_children():
            self.table.delete(red)
        if pretraga == "" or pretraga == "pretraži":
            pretraga = ""
        else:
            if pretraga in "premium":
                pretraga = 1
            elif pretraga in "standard":
                pretraga = 0
        self.popuni_tabelu(self.table, pretraga=pretraga, kriterijum=kriterijum)

    def izlistaj_programe(self, kriterijum='id_programa', pretraga=""):
        return bp_programi.izlistaj_programe(pretraga, kriterijum, self.potrebanPaket, self.id_programa, self.naziv, self.naziv_vrste_treninga, self.trajanjeOd, self.trajanjeDo, self.instruktor)

    def promenljive_filteri(self):
        self.trajanjeOd, self.trajanjeDo = bp_programi.get_trajanje_range()
        self.potrebanPaket = 1
        self.id_programa = ''
        self.naziv = ''
        self.naziv_vrste_treninga = ''
        self.instruktor = ''