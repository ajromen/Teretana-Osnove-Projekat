import bp_izvestaji
from imports import *
from templateIzvestaji import PocetniWindow

class IzvestajiLogika(PocetniWindow):
    def __init__(self, window, main_window, uloga):
        super().__init__(window, main_window, uloga)
        self.ret = None  # promenljiva koja oznacava return vrednost filtera
        

    # Izvestaj A
    def a_izvestaj(self):
        self.trenutni_izvestaj = "A"
        kriterijumi = ["Ime", "Prezime", "Datum rezervacije", "Broj mesta", "Program"]

        self.btnFajl_onemogucen()
        self.info_upozorenje("Molimo Vas prvo izaberite datum u filterima.")
        self.btnFilteri.configure(command=self.fltr_a_izvestaj)

        self.create_table(kriterijumi, True)
        if self.ret is None or self.ret == [] or self.ret == "" or len(self.ret) == 0:
            return
        self.info_uspesan("")
        self.btnFajl_omogucen()
        podaci = bp_izvestaji.a_izvestaj(self.ret)
        self.popuni_tabelu(self.table, podaci)
        
    def fltr_a_izvestaj(self):
        self.trenutni_window = helperFunctions.napravi_toplevel(height=182, title=self.izvestajiMap["A"])
        self.entryDatum = self.create_date_picker(10, 10, top_level=True)
        self.create_text_button("AJDE", 110, 100, command=self.ret_a, top_level=True)
    
    def ret_a(self):
        self.ret = self.entryDatum.get()
        self.trenutni_window.destroy()
        self.a_izvestaj()
        
    def a_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_A.txt", "Rezervacije za datum: " + self.ret)

    # Izvestaj B
    def b_izvestaj(self):
        self.trenutni_izvestaj = "B"
        kriterijumi = ["Ime", "Prezime", "Datum termina", "Broj mesta", "Program"]
        self.create_table(kriterijumi, True)
        pass
    
    def fltr_b_izvestaj(self):
        pass
    
    def ret_b(self):
        pass
    
    def b_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_B.txt", "Rezervacije po datumu termina za datum: " + self.ret)


    # Izvestaj C
    def c_izvestaj(self):
        self.trenutni_izvestaj = "C"
        kriterijumi = ["Ime", "Prezime", "Datum rezervacije", "Program", "Instruktor"]
        self.create_table(kriterijumi, True)
        pass

    def fltr_c_izvestaj(self):
        pass

    def ret_c(self):
        pass
    
    def c_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_C.txt", "Rezervacije po datumu rezervacije i instruktoru za datum: " + self.ret)
    
    
    # Izvestaj D
    def d_izvestaj(self):
        kriterijumi=["Dan","Ime","Prezime","Datum rezervacije","Program"]
        self.trenutni_izvestaj = "D"
        self.create_table(kriterijumi, True)
        pass
    
    def fltr_d_izvestaj(self):
        pass
    
    def ret_d(self):
        pass


    # Izvestaj E
    def e_izvestaj(self):
        self.trenutni_izvestaj = "E"
        pass
    
    def fltr_e_izvestaj(self):
        pass
    
    def ret_e(self):    
        pass
    
    
    # Izvestaj F
    def f_izvestaj(self):
        self.trenutni_izvestaj = "F"
        pass
    
    def fltr_f_izvestaj(self):
        pass
    
    def ret_f(self):
        pass
    
    
    # Izvestaj G
    def g_izvestaj(self):
        self.trenutni_izvestaj = "G"
        pass
    
    def fltr_g_izvestaj(self):
        pass
    
    def ret_g(self):
        pass
    
    
    # Izvestaj H
    def h_izvestaj(self):
        self.trenutni_izvestaj = "H"
        pass
    
    def fltr_h_izvestaj(self):
        pass
    
    def ret_h(self):
        pass
    