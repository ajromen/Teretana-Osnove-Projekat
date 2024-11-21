from tkinter import *
import customtkinter as ctk
import queries
import helperFunctions
import widgets as wid


class AdminWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None
        

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        wid.create_button(self.current_canvas,"./src/img/Widget/btnExit.png",812,9,33,33,lambda: self.main_window.unisti_trenutni_win())# EXit dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnSearch.png",358,53,33,33,self.pretrazi) # Search dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnDodaj.png",300,541,252,40,self.winAdmin_Dodaj) # delete
        
        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/searchPozadina.png",23,53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/tabelaPozadina.png",23,102)
        
        self.kriterijumiMap={
            "Korisničko ime" : "username",
            "Ime" : "ime",
            "Uloga" : "uloga",
            "Prezime" : "prezime",
            "Članstvo" : "status_clanstva",
        }
        self.kriterijumi=["Korisničko ime", "Ime", "Prezime","Uloga","Datum registracije"]
        self.entrySearch=wid.create_entry_search(self.current_canvas,self.pretrazi)
        
        self.current_canvas.create_text(610,65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch=wid.create_comboBox(self.current_canvas,self.kriterijumi,x=681,y=53)
        
        self.table=wid.create_table(self.current_canvas,self.popuni_tabelu,tuple(self.kriterijumi))
        self.table.column("Korisničko ime", width=90)
        self.table.column("Ime", width=100)
        self.table.column("Prezime", width=100) 
        

    def popuni_tabelu(self,tabela):
        for red in tabela.get_children():
            tabela.delete(red)
                
        podaci=self.izlistaj()
        i=0
        for podatak in podaci:
            podatak=list(podatak)
            admin=podatak[3]
            if(admin=="Administrator"):
                tabela.insert("", "end", values=podatak,tags="admin")
            else: tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

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
        
        i=0
        for podatak in podaci:
            podatak=list(podatak)
            admin=podatak[3]
            if(admin=="Administrator"):
                self.table.insert("", "end", values=podatak,tags="admin")
            else: self.table.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

    def izlistaj(self,kriterijum='username',pretraga=""):              
        return queries.izlistaj_instruktore_admine(pretraga,kriterijum)
    
    
    def winAdmin_Dodaj(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednog korisnika.")
            return
        
        self.trenutni_window=helperFunctions.napravi_toplevel(height=193,title="Izmeni trening")
        
        slctd_data = self.table.item(slctd_item)
        slctd_username = slctd_data["values"][0]
        slctd_ime=slctd_data["values"][1]
        slctd_prezime=slctd_data["values"][2]
        
        self.entryBrDana=wid.create_entry(self.trenutni_window,151,96,width=41,height=23,placeholder=slctd_ime,justify="center",belo=True,state="disabled")
        za_aktivaciju=slctd_data.get("tags")
        if(za_aktivaciju):
            fg_color="#3DA928"
            btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27,text_color="#FFFFFF", text="Nagradi lojalnost",font=("Inter", 15),fg_color=fg_color,hover_color="#87E175", command=self.nagradi_lojalnost)
            btnSacuvaj.place(x=89,y=132)
           
        wid.create_label(self.trenutni_window,"Premium paket:",22,93)
        self.entryStatus=wid.create_entry(self.trenutni_window,197,52,width=124,height=23,placeholder=slctd_ime,justify="center",belo=True,state="disabled")
        self.switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
        self.switchPaket.place(x=272,y=90)
        if (slctd_ime=="Premium"): self.switchPaket.select() 
        else: self.switchPaket.deselect()
            
        