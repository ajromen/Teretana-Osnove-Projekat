import bp_izvestaji
from imports import *

class IzvestajiLogika(winTemplate):
    def __init__(self, window, main_window, uloga):
        super().__init__(window, main_window, uloga)
        self.trenutni_izvestaj = None 
        self.ret = None
        
    def postavi_izvestaj(self, kriterijumi, izvestaj_funk,text_fail='',text_succ='',uslov=False,ima_ret=True):
        self.btnFajl_onemogucen()
        self.create_table(kriterijumi, True)
        if not uslov:
            self.info_upozorenje(text_fail)
            return
        self.info_uspesan(text_succ)
        self.btnFajl_omogucen()
        if ima_ret:
            podaci = izvestaj_funk(self.ret)
        else:
            podaci = izvestaj_funk()
        self.popuni_tabelu(self.table, podaci) 
        
    def namesti_top_level(self,window_y,sacuvaj_y,ret_komanda=None):
        self.trenutni_window.geometry("343x"+str(window_y))
        otkazi_y = sacuvaj_y + 37
        self.btnSacuvaj.place(x=102, y=sacuvaj_y)
        self.btnOtkazi.place(x=136, y=otkazi_y)
        self.btnSacuvaj.configure(command=ret_komanda)

    # Izvestaj A
    def a_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "A"
        kriterijumi = ["Ime", "Prezime", "Datum rezervacije", "Broj mesta", "Program"]
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.a_izvestaj,"Molimo Vas prvo izaberite datum u filterima.","Datum: " + str(self.ret),uslov=izabrano)
        
    def fltr_a_izvestaj(self):
        self.top_level = True
        self.trenutni_window.geometry("343x167")
        self.namesti_top_level(167, 102, self.ret_a)
        
        self.create_label("Odaberite datum:", 38, 41)
        self.entryDatum = self.create_date_picker(197, 42)
        self.top_level = False
    
    def ret_a(self):
        self.ret = self.entryDatum.get()
        self.trenutni_window.destroy()
        self.a_izvestaj(izabrano=True)
        
    def a_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_A.txt", "Rezervacije za datum: " + self.ret)

    # Izvestaj B
    def b_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "B"
        kriterijumi = ["Ime", "Prezime", "Datum termina", "Broj mesta", "Program"]
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.b_izvestaj,"Molimo Vas prvo izaberite datum termina u filterima.","Datum termina: " + str(self.ret),uslov=izabrano)
    
    def fltr_b_izvestaj(self):
        self.top_level = True
        self.namesti_top_level(167, 102, self.ret_b)
        
        self.create_label("Odaberite datum termina:", 38, 41)
        self.entryDatum = self.create_date_picker(197, 42)
        self.top_level = False
    
    def ret_b(self):
        self.ret = self.entryDatum.get()
        self.trenutni_window.destroy()
        self.b_izvestaj(izabrano=True)
    
    def b_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_B.txt", "Rezervacije po datumu termina za datum: " + self.ret)


    # Izvestaj C
    def c_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "C"
        kriterijumi = ["Ime", "Prezime", "Datum rezervacije","Broj mesta", "Program"]
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.c_izvestaj,"Molimo Vas prvo izaberite datum i instruktora u filterima.","Datum, Instruktor: " + str(self.ret),uslov=izabrano)

    def fltr_c_izvestaj(self):
        self.top_level = True
        self.namesti_top_level(189, 126, self.ret_c)
        
        self.create_label("Odaberite datum:", 38, 29)
        self.cmbbxInstruktor=self.napravi_sql_cmbbx("Odaberite instruktora:", 25, 80,177,69,"SELECT username,ime,prezime FROM Korisnici WHERE uloga = 1",2,True,12)
        self.entryDatum = self.create_date_picker(197, 29)
        self.top_level = False


    def ret_c(self):
        instruktor=self.cmbbxInstruktor.get().strip().split(" ")[0]
        datum=self.entryDatum.get()
        self.ret = f'{datum}, {instruktor}'
        self.trenutni_window.destroy()
        self.c_izvestaj(izabrano=True)
    
    def c_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_C.txt", "Rezervacije po datumu i instruktoru: " + self.ret)

    # Izvestaj D
    def d_izvestaj(self,izabrano=False):
        kriterijumi=["Ime","Prezime","Datum rezervacije","Broj mesta","Program"]
        self.trenutni_izvestaj = "D"
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.d_izvestaj,"Molimo Vas prvo izaberite dan u filterima.","Dan: " + helperFunctions.broj_u_dan(self.ret),uslov=izabrano)
    
    def fltr_d_izvestaj(self):
        self.top_level = True
        self.namesti_top_level(150, 90, self.ret_d)
        
        self.create_label("Odaberite dan u nedelji:", 27, 43)
        self.cmbbxDan = self.create_comboBox(["Ponedeljak", "Utorak", "Sreda", "Četvrtak", "Petak", "Subota", "Nedelja"], 179, 32)
        self.top_level = False
    
    def ret_d(self):
        self.ret = helperFunctions.dan_u_broj(self.cmbbxDan.get())
        self.trenutni_window.destroy()
        self.d_izvestaj(izabrano=True)
    
    def d_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_D.txt", "Rezervacije po danu: " + helperFunctions.broj_u_dan(self.ret))


    # Izvestaj E
    def e_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "E"
        kriterijumi=["Korisničko ime","Ime","Prezime","Broj rezervacija"]
        self.btnFilteri_onemogucen()
        self.postavi_izvestaj(kriterijumi,bp_izvestaji.e_izvestaj,"","",True,False)
    
    def fltr_e_izvestaj(self):
        """Nema filtere"""
        pass
    
    def ret_e(self):    
        """Nema return vrednost"""
        pass
    
    def e_txt(self):
        helperFunctions.dopisi_u_fajl("Izvestaji/izvestaj_E.txt", "Broj rezervacija po instruktoru (30 dana)")
    
    
    # Izvestaj F
    def f_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "F"
        pass
    
    def fltr_f_izvestaj(self):
        pass
    
    def ret_f(self):
        pass
    
    
    # Izvestaj G
    def g_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "G"
        pass
    
    def fltr_g_izvestaj(self):
        pass
    
    def ret_g(self):
        pass
    
    
    # Izvestaj H
    def h_izvestaj(self,izabrano=False):
        self.trenutni_izvestaj = "H"
        pass
    
    def fltr_h_izvestaj(self):
        pass
    
    def ret_h(self):
        pass
    