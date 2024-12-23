import bp_izvestaji
from imports import *
from logikaIzvestaji import IzvestajiLogika

class IzvestajiWindow(IzvestajiLogika):
    def __init__(self, window, main_window, uloga):
        super().__init__(window, main_window, uloga)

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
            "G": "Top 3 najpopularnija treninga",
            "H": "Najpopularniji dan u nedelji (1 godina)"
        }
        self.varIzvestaj = StringVar()
        self.cmbbxIzvestaj = self.create_comboBox([slovo + ". " + self.izvestajiMap[slovo] for slovo in "ABCDEFGH"], 23, 54, width=184, variable=self.varIzvestaj)
        self.varIzvestaj.trace_add("write", self.on_combo_change)

        self.ret = None  # promenljiva koja oznacava return vrednost filtera
        self.btnFilteri = self.create_text_button("Filteri", 214, 54, width=150, height=33, command=self.filteri)
        self.entryInfo = self.create_entry(374, 54, width=296, height=33, placeholder="", state="disabled")
        self.btnFajl = self.create_text_button("Sačuvaj u datoteku", 679, 54, width=150, height=33)
        self.btnFajl_onemogucen()
        self.a_izvestaj()

    def on_combo_change(self, *args):
        if self.varIzvestaj.get() == "":
            return
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
            case "H": self.h_izvestaj()
            case _: self.a_izvestaj()

    def filteri(self):
        izvestaj = self.cmbbxIzvestaj.get().split(". ")
        helperFunctions.napravi_toplevel(title=izvestaj[1], height=182)
        match izvestaj[0]:
            case "A": self.fltr_a_izvestaj(),
            case "B": self.fltr_b_izvestaj(),
            case "C": self.fltr_c_izvestaj(),
            case "D": self.fltr_d_izvestaj(),
            case "E": self.fltr_e_izvestaj(),
            case "F": self.fltr_f_izvestaj(),
            case "G": self.fltr_g_izvestaj(),
            case "H": self.fltr_h_izvestaj()