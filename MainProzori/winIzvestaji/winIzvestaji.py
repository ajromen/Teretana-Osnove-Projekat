import bp_izvestaji
from imports import *
from logikaIzvestaji import IzvestajiLogika

class IzvestajiWindow(IzvestajiLogika):
    def __init__(self, window, escfunk=None, uloga=None,username=None, u_prozoru=False):
        super().__init__(window, escfunk, uloga, u_prozoru, username)

    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_table_bg(True)

        self.izvestajiMap = {
            "A": "Lista rezervacija po datumu rezervacije",
            "B": "Lista rezervacija po datumu termina",
            "C": "Lista rezervacija po datumu rezervacije i instruktoru",
            "D": "Broj rezervacija za dan u nedelji",
            "E": "Broj rezervacija po instruktoru (30 dana)",
            "F": "Broj realizovanih rezervacija po paketu",
            "G": "Top 3 najpopularnija programa treninga",
            "H": "Najpopularniji dan u nedelji (1 godina)"
        }
        self.varIzvestaj = StringVar()
        self.cmbbxIzvestaj = self.create_comboBox([slovo + ". " + self.izvestajiMap[slovo] for slovo in "ABCDEFGH"], 23, 54, width=184, variable=self.varIzvestaj)
        self.varIzvestaj.trace_add("write", self.on_combo_change)

        self.btnFilteri = self.create_text_button("Filteri", 214, 54, width=150, height=33, command=self.filteri)
        self.entryInfo = self.create_entry(374, 54, width=296, height=33, placeholder="", state="normal")
        self.btnFajl = self.create_text_button("Sačuvaj u datoteku", 679, 54, width=150, height=33)
        self.btnFajl_onemogucen()
        self.a_izvestaj()

    def on_combo_change(self, *args):
        if self.varIzvestaj.get() == "":
            return
        self.ret = None
        self.btnFajl_onemogucen()
        self.btnFilteri_omogucen()
        izvestaj = self.varIzvestaj.get().split(". ")[0]
        self.table.destroy()

        match izvestaj:
            case "A": self.a_izvestaj(),
            case "B": self.b_izvestaj(),
            case "C": self.c_izvestaj(),
            case "D": self.d_izvestaj(),
            case "E": self.e_izvestaj(),
            case "F": self.f_izvestaj(),
            case "G": self.g_izvestaj(),
            case "H": self.h_izvestaj(),
            case _: self.a_izvestaj()

    def filteri(self):
        self.top_level = True
        izvestaj = self.cmbbxIzvestaj.get().split(". ")
        self.trenutni_window=helperFunctions.napravi_toplevel(title=izvestaj[1],height=200)
        self.btnOtkazi=self.create_button("src/img/Widget/btnOtkazi.png",136,139,command=self.trenutni_window.destroy)
        self.btnSacuvaj=self.create_text_button("Sačuvaj", 102, 102)
        match izvestaj[0]:
            case "A": self.fltr_a_izvestaj(),
            case "B": self.fltr_b_izvestaj(),
            case "C": self.fltr_c_izvestaj(),
            case "D": self.fltr_d_izvestaj(),
            case "F": self.fltr_f_izvestaj(),
            case _: self.fltr_a_izvestaj()
            
        self.top_level = False
            
    def sacuvaj_u_fajl(self):
        podaci = [list(self.table.item(item)["values"]) for item in self.table.get_children()]
        if not helperFunctions.pitaj("Da li  ste sigurni da želite da sačuvate izveštaj u fajl?"):
            return
        if len(podaci) == 0:
            if not helperFunctions.pitaj("Nema podataka za čuvanje u fajl. \nDa li želite da sačuvate praznu tabelu?"):
                return

        imena_kolona = [kolona for kolona in self.table["columns"]]
        putanja = "Izvestaji/izvestaj_" + self.trenutni_izvestaj + ".txt"
        helperFunctions.sacuvaj_tabelu(podaci, imena_kolona, putanja)
        
        match self.trenutni_izvestaj:
            case "A": self.a_txt()
            case "B": self.b_txt()
            case "C": self.c_txt()
            case "D": self.d_txt()
            case "E": self.e_txt()
            case "F": self.f_txt()
            case "G": self.g_txt()
            case "H": self.h_txt()
            
        helperFunctions.dopisi_u_fajl(putanja, "Datum izrade izveštaja: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    def popuni_tabelu(self, tabela, podaci: list = None, kolonaZaBrisanje=None):
        for red in tabela.get_children(): tabela.delete(red)
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
        self.entryInfo.configure(state="normal")
        self.entryInfo.configure(text_color=boje.text_siva)
        self.entryInfo.delete(0, END)
        self.entryInfo.insert(0, tekst)
        self.entryInfo.configure(state="disabled")

    def info_upozorenje(self, tekst):
        self.entryInfo.configure(state="normal")
        self.entryInfo.configure(text_color=boje.text_error)
        self.entryInfo.delete(0, END)
        self.entryInfo.insert(0, tekst)
        self.entryInfo.configure(state="disabled")

    def btnFajl_onemogucen(self):
        self.btnFajl.configure(command=None)
        self.btnFajl.configure(fg_color=boje.dugme_disabled)

    def btnFajl_omogucen(self):
        self.btnFajl.configure(command=self.sacuvaj_u_fajl)
        self.btnFajl.configure(fg_color=boje.dugme)
        
    def btnFilteri_onemogucen(self):
        self.btnFilteri.configure(command=None)
        self.btnFilteri.configure(fg_color=boje.dugme_disabled)
        
    def btnFilteri_omogucen(self):
        self.btnFilteri.configure(command=self.filteri)
        self.btnFilteri.configure(fg_color=boje.dugme)