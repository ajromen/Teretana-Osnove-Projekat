import bp_izvestaji
from imports import *

class IzvestajiLogika(winTemplate):
    def __init__(self, window, main_window, uloga):
        super().__init__(window, main_window, uloga)
        self.trenutni_izvestaj = None 
        self.ret = None
        
    def postavi_izvestaj(self, kriterijumi, izvestaj_funk,text_fail='',text_succ=''):
        self.btnFajl_onemogucen()
        self.create_table(kriterijumi, True)
        if self.ret is None or self.ret == [] or self.ret == "" or len(self.ret) == 0:
            self.info_upozorenje(text_fail)
            return
        self.info_uspesan(text_succ)
        self.btnFajl_omogucen()
        podaci = izvestaj_funk(self.ret)
        self.popuni_tabelu(self.table, podaci) 

    # Izvestaj A
    def a_izvestaj(self):
        self.trenutni_izvestaj = "A"
        kriterijumi = ["Ime", "Prezime", "Datum rezervacije", "Broj mesta", "Program"]
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.a_izvestaj,"Molimo Vas prvo izaberite datum u filterima.","Datum: " + str(self.ret))
        
    def fltr_a_izvestaj(self):
        self.top_level = True
        self.trenutni_window.geometry("343x167")
        self.create_label("Odaberite datum:", 38, 41)
        self.btnSacuvaj.configure(command=self.ret_a)
        self.entryDatum = self.create_date_picker(197, 42)
        self.top_level = False
    
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
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.b_izvestaj,"Molimo Vas prvo izaberite datum termina u filterima.","Datum termina: " + str(self.ret))
    
    def fltr_b_izvestaj(self):
        self.top_level = True
        self.trenutni_window.geometry("343x167")
        self.create_label("Odaberite datum termina:", 38, 41)
        self.btnSacuvaj.configure(command=self.ret_b)
        self.entryDatum = self.create_date_picker(197, 42)
        self.top_level = False
    
    def ret_b(self):
        self.ret = self.entryDatum.get()
        self.trenutni_window.destroy()
        self.b_izvestaj()
    
    def b_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_B.txt", "Rezervacije po datumu termina za datum: " + self.ret)


    # Izvestaj C
    def c_izvestaj(self):
        self.trenutni_izvestaj = "C"
        kriterijumi = ["Ime", "Prezime", "Datum rezervacije","Broj mesta", "Program"]
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.c_izvestaj,"Molimo Vas prvo izaberite datum i instruktora u filterima.","Datum, Instruktor: " + str(self.ret))

    def fltr_c_izvestaj(self):
        self.top_level = True
        self.trenutni_window.geometry("343x189")
        self.create_label("Odaberite datum termina:", 15, 29)
        self.cmbbxInstruktor=self.napravi_sql_cmbbx("Odaberite instruktora:", 25, 80,177,69,"SELECT username,ime,prezime FROM Korisnici WHERE uloga = 1",2,True,12)
        self.btnSacuvaj.configure(command=self.ret_c)
        self.btnSacuvaj.place(x=102, y=126)
        self.btnOtkazi.place(x=136, y=163)
        self.entryDatum = self.create_date_picker(197, 29)
        self.top_level = False


    def ret_c(self):
        instruktor=self.cmbbxInstruktor.get().strip().split(" ")[0]
        datum=self.entryDatum.get()
        self.ret = f'{datum}, {instruktor}'
        self.trenutni_window.destroy()
        self.c_izvestaj()
    
    def c_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_C.txt", "Rezervacije po datumu i instruktoru: " + self.ret)
    
    
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
    