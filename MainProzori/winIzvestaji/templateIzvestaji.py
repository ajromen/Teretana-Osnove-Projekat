# baseWindow.py
from imports import *
import helperFunctions

class PocetniWindow(winTemplate):
    def __init__(self, window, main_window, uloga):
        super().__init__(window, main_window, uloga)
        self.trenutni_izvestaj = None

    def popuni_tabelu(self, tabela, podaci: list = None, kolonaZaBrisanje=None):
        for red in tabela.get_children():
            tabela.delete(red)
        if podaci is None:
            return
        i = 0
        for podatak in podaci:
            if kolonaZaBrisanje is not None and podatak[kolonaZaBrisanje] == 1:  # obrisan
                tabela.insert("", "end", values=podatak, tags="obrisano" + str(i % 2))
            else:
                tabela.insert("", "end", values=podatak, tags=str(i % 2))
            i += 1

    def info_uspesan(self, tekst):
        self.entryInfo.configure(text_color="#FFFFFF")
        self.entryInfo.delete(0, END)
        self.entryInfo.insert(0, tekst)

    def info_upozorenje(self, tekst):
        self.entryInfo.configure(text_color="#FF1C1C")
        self.entryInfo.delete(0, END)
        self.entryInfo.insert(0, tekst)

    def btnFajl_onemogucen(self):
        self.btnFajl.configure(command=None)
        self.btnFajl.configure(fg_color="#252525")

    def btnFajl_omogucen(self):
        self.btnFajl.configure(command=self.sacuvaj_u_fajl)
        self.btnFajl.configure(fg_color="#1F6AA5")

    def sacuvaj_u_fajl(self):
        podaci = [list(self.table.item(item)["values"]) for item in self.table.get_children()]
        if len(podaci) == 0:
            if not helperFunctions.pitaj("Nema podataka za čuvanje u fajl. \nDa li želite da sačuvate praznu tabelu?"):
                return

        imena_kolona = [kolona for kolona in self.table["columns"]]
        putanja = "Izvestaji/izvestaj_" + self.trenutni_izvestaj + ".txt"
        helperFunctions.sacuvaj_tabelu(podaci, imena_kolona, putanja)