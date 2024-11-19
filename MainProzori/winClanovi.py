from tkinter import *
import customtkinter as ctk
import queries
import helperFunctions
import widgets as wid


class ClanoviWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        wid.create_button(self.current_canvas,"./src/img/Widget/btnExit.png",812,9,33,33,lambda: self.main_window.unisti_trenutni_win())# EXit dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnSearch.png",358,53,33,33,self.pretrazi) # Search dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnNagradi.png",653,53,176,33,self.winClan_Izmeni) # Search dugme
        
        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/searchPozadina.png",23,53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/tabelaPozadina_duza.png",23,102)
        
        self.kriterijumiMap={
            "Korisničko ime" : "username",
            "Ime" : "ime",
            "Prezime" : "prezime",
            "Članstvo" : "status_clanstva",
            "Paket" : "uplacen_paket",
            "Datum registracije" : "datum_registracije",
            "Članarina obnovljena" : "obnova_clanarine"
        }
        self.kriterijumi=["Korisničko ime", "Ime", "Prezime", "Članstvo", "Paket","Datum registracije","Članarina obnovljena","Broj rezervacija"]
        self.entrySearch=wid.create_entry_search(self.current_canvas,self.pretrazi)
        
        self.current_canvas.create_text(420,65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch=wid.create_comboBox(self.current_canvas,self.kriterijumi,x=497,y=53)
        self.cmbbxSearch.configure(values=self.kriterijumi[:-1])
        
        self.table=wid.create_table(self.current_canvas,self.popuni_tabelu,tuple(self.kriterijumi),height=462)
        self.table.column("Korisničko ime", width=90)
        self.table.column("Ime", width=100)
        self.table.column("Prezime", width=100)
        self.table.column("Datum registracije", width=100)
        self.table.column("Članarina obnovljena", width=120)    
    

    def popuni_tabelu(self,tabela):
        for red in tabela.get_children():
            tabela.delete(red)
                
        podaci=self.izlistaj()
        
        for podatak in podaci:
            podatak=list(podatak)
            username=podatak[0]
            broj_rezervacija=queries.broj_rezervacija_za_mesec(username)
            podatak.append(broj_rezervacija)
            if(broj_rezervacija>1):
                tabela.insert("", "end", values=podatak,tags="za_aktivaciju")
            else: tabela.insert("", "end", values=podatak)

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        if(not kriterijum):
            helperFunctions.obavestenje("Prvo izaberite kriterijum pretrage.")
            return

        for red in self.table.get_children():
            self.table.delete(red)
            
        if pretraga =="" or pretraga=="pretraži":
            pretraga=""
        else:
            if pretraga in "premium":
                pretraga = 1
            elif pretraga in "standard":
                pretraga = 0  
            elif pretraga in "aktiviran":
                pretraga = 1
            elif pretraga in "neaktiviran":
                pretraga = 0  
            else:
                pass
        
        podaci=self.izlistaj(pretraga=pretraga,kriterijum=kriterijum)
        
        for podatak in podaci:
            podatak=list(podatak)
            username=podatak[0]
            broj_rezervacija=queries.broj_rezervacija_za_mesec(username)
            podatak.append(broj_rezervacija)
            if(broj_rezervacija>1):
                self.table.insert("", "end", values=podatak,tags="za_aktivaciju")
            else: self.table.insert("", "end", values=podatak)

    def izlistaj(self,kriterijum='username',pretraga=""):              
        return queries.izlistaj_korisnike(pretraga,kriterijum)
    
    def winClan_Izmeni(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednog korisnika.")
            return
        
        self.trenutni_window=helperFunctions.napravi_toplevel(height=193,title="Izmeni trening")
        
        slctd_data = self.table.item(slctd_item)
        slctd_username = slctd_data["values"][0]
        slctd_ime=slctd_data["values"][1]
        slctd_prezime=slctd_data["values"][2]
        slctd_br_rez=slctd_data["values"][7]
        za_aktivaciju=slctd_data.get("tags")
        
        wid.create_label(self.trenutni_window,"Broj realizovanih rezervacija u proteklih",34,52)
        wid.create_label(self.trenutni_window,"mesec dana:",126,70)
        
        self.entryID=wid.create_entry(self.trenutni_window,70,11,width=203,height=23,placeholder=slctd_username+", "+slctd_ime+" "+slctd_prezime,justify="center",belo=True,state="disabled")
        self.entryID=wid.create_entry(self.trenutni_window,151,96,width=41,height=23,placeholder=slctd_br_rez,justify="center",belo=True,state="disabled")
        
        
        if(za_aktivaciju):
            fg_color="#4FD035"
            btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27, text="Nagradi lojalnost",font=("Inter", 15),fg_color=fg_color,hover_color="#87E175", command=lambda: self.aktiviraj_paket(slctd_username))
            btnSacuvaj.place(x=89,y=132)
        else:
            fg_color="#2B2B2B"
            btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27, text="Nagradi lojalnost",font=("Inter", 15),fg_color=fg_color,hover_color="#6B6969", command=lambda: None)
            btnSacuvaj.place(x=89,y=132)
    
        
        wid.create_button(self.trenutni_window,"./src/img/Widget/btnOtkazi.png",x=136,y=166,width=72,height=17,command=self.trenutni_window.destroy)

    
    def aktiviraj_paket(self,username):
        '''kada se pritisne treba korisniku da stavi na datum obnove clanarine
           na dan jedan mesec posle proslog dana obnove i da mu dodeli premium paket'''
        pass