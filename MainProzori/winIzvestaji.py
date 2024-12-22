import bp_izvestaji
from imports import *

class IzvestajiWindow(winTemplate):
    def __init__(self, window, main_window,uloga):
        super().__init__(window,main_window,uloga)
        
    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_table_bg(True)
        
        self.izvestajiMap={
            "A": "Lista rezervacija po datumu rezervacije",
            "B": "Lista rezervacija po datumu termina",
            "C": "Lista rezervacija po datumu rezervacije i instruktoru",
            "D": "Broj rezervacija za dan u nedelji",
            "E": "Broj rezervacija po instruktoru (30 dana)",
            "F": "Broj realizovanih rezervacija po paketu",
            "G": "Top 3 najpopularnija treninga",
            "H": "Najpopularniji dan u nedelji (1 godina)"
        }
        self.varIzvestaj=StringVar()
        self.cmbbxIzvestaj=self.create_comboBox([slovo+". "+self.izvestajiMap[slovo] for slovo in "ABCDEFGH"], 23, 54,width=184,variable=self.varIzvestaj)
        self.varIzvestaj.trace_add("write", self.on_combo_change)
        
        self.ret=None#promenljiva koja oznacava return vrednost filtera 
        self.btnFilteri=self.create_text_button("Filteri",214, 54,width=150,height=33,command=self.filteri)
        self.entryInfo=self.create_entry(374,54,width=296,height=33,placeholder="Molim Vas izaberite filtere.",state="disabled")
        self.entryInfo.configure(text_color="#FF1C1C")
        self.create_text_button("Sačuvaj u datoteku",679, 54,width=150,height=33)
        self.a_izvestaj()
        
    def on_combo_change(self, *args):
        if(self.varIzvestaj.get()==""): return
        izvestaj=self.varIzvestaj.get().split(". ")[0]
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
            
    def popuni_tabelu(self,tabela,podaci:list =None,kolonaZaBrisanje=None):
        for red in tabela.get_children():
            tabela.delete(red)
        if(podaci==None): return
        i=0
        for podatak in podaci:
            if(kolonaZaBrisanje!=None and podatak[kolonaZaBrisanje]==1): #obrisan
                tabela.insert("", "end", values=podatak,tags="obrisano"+str(i%2))
            else: tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1
            
    def info_uspesan(self,tekst):
        self.entryInfo.configure(text_color="#FFFFFF")
        self.entryInfo.delete(0,END)
        self.entryInfo.insert(0,tekst)
        
    def info_upozorenje(self,tekst):
        self.entryInfo.configure(text_color="#FF1C1C")
        self.entryInfo.delete(0,END)
        self.entryInfo.insert(0,tekst)
            
    def filteri(self):
        izvestaj=self.cmbbxIzvestaj.get().split(". ")
        helperFunctions.napravi_toplevel(title=izvestaj[1],height=182)
        match izvestaj[0]:
            case "A": self.fltr_a_izvestaj(),
            case "B": self.fltr_b_izvestaj(),
            case "C": self.fltr_c_izvestaj()
    
    def a_izvestaj(self):
        kriterijumi=["Ime","Prezime","Datum rezervacije","Red","Program"]
        self.btnFilteri.configure(command=self.fltr_a_izvestaj)
        
        self.create_table(kriterijumi,True)
        if(self.ret==None):
            return
        podaci=bp_izvestaji.a_izvestaj(self.ret)
        self.popuni_tabelu(self.table,podaci)
    
    def b_izvestaj(self):
        kriterijumi=["Ime","Prezime","Datum termina","Red","Program"]
        self.create_table(kriterijumi,True)
        pass
    
    def c_izvestaj(self):
        kriterijumi=["Ime","Prezime","Datum rezervacije","Red","Program"]
        pass
    
    def d_izvestaj(self):
        pass
    
    def e_izvestaj(self):
        pass
    
    def f_izvestaj(self):
        pass
    
    def g_izvestaj(self):
        pass
    
    def h_izvestaj(self):
        pass
    
    def fltr_a_izvestaj(self):
        self.trenutni_window=helperFunctions.napravi_toplevel(height=182,title=self.izvestajiMap["A"])
        self.entryDate=self.create_entry(33,28,top_level=True)
        self.create_text_button("AJDE",110,100,command=lambda:print("usp"),top_level=True)
    
    def fltr_b_izvestaj(self):
        pass
    
    def fltr_c_izvestaj(self):
        pass
    
    def fltr_d_izvestaj(self):
        pass
    
    def fltr_e_izvestaj(self):
        pass
    
    def fltr_f_izvestaj(self):
        pass
    
    def fltr_g_izvestaj(self):
        pass
    
    def fltr_h_izvestaj(self):
        pass