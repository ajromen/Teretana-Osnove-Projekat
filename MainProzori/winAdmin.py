from datetime import date
import re
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
        wid.create_button(self.current_canvas,"./src/img/Widget/btnDodaj.png",23,543,252,40,lambda: self.winAdmin_Dodaj()) # Dodaj Dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnObrisi.png",577,543,252,40,self.obrisi) # Obrisi Dugme
        
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
            
        pretraga=pretraga.lower()
            
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
        self.trenutni_window=helperFunctions.napravi_toplevel(height=341,title="Dodaj administrarota")
        
        wid.create_label(self.trenutni_window,"Korisničko ime:",23,31)
        wid.create_label(self.trenutni_window,"Ime:",62,76)
        wid.create_label(self.trenutni_window,"Prezime:",46,120)
        wid.create_label(self.trenutni_window,"Lozinka:",47,164)
        wid.create_label(self.trenutni_window,"Administrator:",27,218)
        
        self.entryUsername=wid.create_entry(self.trenutni_window,141,30,width=179,height=23,manual_fin_fon=(True,"Polje"))
        self.entryIme=wid.create_entry(self.trenutni_window,141,74,width=179,height=23,manual_fin_fon=(True,"Polje"))
        self.entryPrezime=wid.create_entry(self.trenutni_window,141,118,width=179,height=23,manual_fin_fon=(True,"Polje"))
        self.entryLozinka=wid.create_entry(self.trenutni_window,141,162,width=179,height=23,manual_fin_fon=(True,"Lozinka"),placeholder="Lozinka")
        
        self.switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
        self.switchPaket.place(x=272,y=215)

        btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27,text_color="#FFFFFF", text="Napravi nalog",font=("Inter", 15),command=self.napravi_nalog)
        btnSacuvaj.place(x=88,y=268)
        wid.create_button(self.trenutni_window,"./src/img/Widget/btnOtkazi.png",x=136,y=303,width=72,height=17,command=self.trenutni_window.destroy)

        
    def napravi_nalog(self):
        username=self.entryUsername.get().strip()
        ime=self.entryIme.get().strip()
        prezime=self.entryPrezime.get().strip()
        lozinka=self.entryLozinka.get()
        admin=self.switchPaket.get()
        
        if(username=="" or ime=="" or prezime==""):
            helperFunctions.obavestenje("Sva polja moraju biti popunjena")
            return 
        if(len(lozinka)<6):
            helperFunctions.obavestenje("Lozinka mora da sadrži više od 6 karaktera")
            return 
        
        
        admin+=1
        datum_registracije=date.today().strftime("%Y-%m-%d")
        queries.napraviNalog(username, lozinka, ime, prezime, admin, 0, 0, datum_registracije, "")
        
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        
    def obrisi(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednog korisnika.")
            return
        
        pitaj = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabranog korisnika?")
        if not pitaj:
            return

        slctd_data = self.table.item(slctd_item)
        username = slctd_data["values"][0]

        komanda = "DELETE FROM Korisnici WHERE username = ?"
        queries.cursor.execute(komanda, (username,))
        queries.connection.commit()

        self.table.delete(slctd_item)
        helperFunctions.obavestenje(title="Brisanje", poruka="Korisnik je uspešno obrisan.")
            
        