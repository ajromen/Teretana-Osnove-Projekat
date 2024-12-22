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
        
        self.btnFilteri=self.create_text_button("Filteri",214, 54,width=150,height=33,command=self.filteri)
        self.entryInfo=self.create_entry(374,54,width=296,height=33,placeholder="Molim Vas izaberite filtere.")
        self.entryInfo.configure(text_color="#FF1C1C")
        self.create_text_button("Sačuvaj u datoteku",679, 54,width=150,height=33)
        self.a_izvestaj()
        
    def on_combo_change(self, *args):
        if(self.varIzvestaj.get()==""): return
        izvestaj=self.varIzvestaj.get().split(". ")[0]
        self.btnFilteri.destroy()
        self.table.destroy()
        
        match izvestaj:
            case "A": self.a_izvestaj(),
            case "B": self.b_izvestaj(),
            
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
            case "A": pass
            case "B": pass
            case "C": pass
    
    def a_izvestaj(self):
        kriterijumi=["Ime","Prezime","Datum rezervacije","Red","Program"]
        #podaci=bp_izvestaji.a_izvestaj(None)
        self.create_table(kriterijumi,True)
        #self.popuni_tabelu(self.table,podaci)
    
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