# baseWindow.py
from imports import *

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

    