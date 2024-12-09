from tkinter import *
import customtkinter as ctk
import Queries.queries as queries
import helperFunctions
import widgets as wid


class ClanoviWindow:
    def __init__(self, window, main_window,uloga):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None
        self.broj_rez_kluc="potreban_broj_za_rezervacije"
        broj_rez=helperFunctions.ucitaj_iz_setup(self.broj_rez_kluc)
        self.broj_rezervacija_za_nagradjivanje=int(broj_rez) if broj_rez else 27
        
        self.uloga=uloga
        

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        wid.create_button(self.current_canvas,"./src/img/Widget/btnExit.png",812,9,33,33,lambda: self.main_window.unisti_trenutni_win())# EXit dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnSearch.png",358,53,33,33,self.pretrazi) # Search dugme
        self.uloga=="admin" and wid.create_button(self.current_canvas,"./src/img/Widget/btnNagradi.png",23,541,252,40,lambda: self.winClan_Izmeni("Nagradi")) # nagradi
        wid.create_button(self.current_canvas,"./src/img/Widget/btnAktiviraj.png",300,541,252,40,lambda: self.winClan_Izmeni("Aktiviraj")) # aktiviraj
        wid.create_button(self.current_canvas,"./src/img/Widget/btnObrisi.png",576,541,252,40,self.clan_delete) # delete
        
        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/searchPozadina.png",23,53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/tabelaPozadina.png",23,102)
        
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
        
        self.current_canvas.create_text(610,65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch=wid.create_comboBox(self.current_canvas,self.kriterijumi,x=681,y=53)
        self.cmbbxSearch.configure(values=self.kriterijumi[:-1])
        
        self.table=wid.create_table(self.current_canvas,self.popuni_tabelu,tuple(self.kriterijumi))
        self.table.column("Korisničko ime", width=90)
        self.table.column("Ime", width=100)
        self.table.column("Prezime", width=100)
        self.table.column("Datum registracije", width=100)
        self.table.column("Članarina obnovljena", width=120)    
        
        wid.create_label(self.current_canvas,"Zahtev za nagradu",421,64,12)
        self.entryBrojNagrada=wid.create_entry(self.current_canvas,540,60,width=59,height=23,belo=True,justify="center",placeholder=self.broj_rezervacija_za_nagradjivanje)
        self.entryBrojNagrada.bind("<Return>",command=lambda event: self.promeni_broj_rezervacija())
        
        
    def promeni_broj_rezervacija(self):
        brdana=self.entryBrojNagrada.get().strip()
        if(brdana=="" or int(brdana)==0 or not brdana.isdigit()): 
            helperFunctions.obavestenje("Zahtev mora biti broj veći od 0.")
            return
        self.broj_rezervacija_za_nagradjivanje=int(brdana)
        helperFunctions.azuriraj_setup(self.broj_rez_kluc, str(brdana))
        self.popuni_tabelu(self.table)

    def popuni_tabelu(self,tabela,kriterijum='username',pretraga=""):
        for red in tabela.get_children():
            tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum=kriterijum,pretraga=pretraga)
        
        i=0
        for podatak in podaci:
            podatak=list(podatak)
            username=podatak[0]
            broj_rezervacija=queries.broj_rezervacija_za_mesec(username)
            podatak.append(broj_rezervacija)
            if podatak[0]=="obrisan_korisnik": 
                tabela.insert("", "end", values=podatak,tags="obrisano"+str(i%2))
            elif(broj_rezervacija>=self.broj_rezervacija_za_nagradjivanje):
                tabela.insert("", "end", values=podatak,tags="za_aktivaciju")
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
        
        self.popuni_tabelu(kriterijum=kriterijum,pretraga=pretraga)

    def izlistaj(self,kriterijum='username',pretraga=""):              
        return queries.izlistaj_korisnike(pretraga,kriterijum)
    
    
    def winClan_Izmeni(self,mode="Nagradi"):# ili Aktiviraj
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
        slctd_aktiviran=slctd_data["values"][3]
        slctd_paket=slctd_data["values"][4]
        
        self.entryID=wid.create_entry(self.trenutni_window,70,11,width=203,height=23,placeholder=slctd_username+", "+slctd_ime+" "+slctd_prezime,justify="center",belo=True,state="disabled")
        
        if(mode=="Nagradi"):
            wid.create_label(self.trenutni_window,"Broj realizovanih rezervacija u proteklih",34,52)
            wid.create_label(self.trenutni_window,"mesec dana:",126,70)
            self.entryBrDana=wid.create_entry(self.trenutni_window,151,96,width=41,height=23,placeholder=slctd_br_rez,justify="center",belo=True,state="disabled")
            za_aktivaciju=slctd_data.get("tags")[0]
            if(za_aktivaciju=='za_aktivaciju'):
                fg_color="#3DA928"
                btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27,text_color="#FFFFFF", text="Nagradi lojalnost",font=("Inter", 15),fg_color=fg_color,hover_color="#87E175", command=self.nagradi_lojalnost)
                btnSacuvaj.place(x=89,y=132)
            else:
                fg_color="#2B2B2B"
                btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27, text="Nagradi lojalnost",font=("Inter", 15),fg_color=fg_color,hover_color="#6B6969", command=lambda: None)
                btnSacuvaj.place(x=89,y=132)
        
        else:
            wid.create_label(self.trenutni_window,"Trenutni status:",22,57)
            wid.create_label(self.trenutni_window,"Premium paket:",22,93)
            self.entryStatus=wid.create_entry(self.trenutni_window,197,52,width=124,height=23,placeholder=slctd_aktiviran,justify="center",belo=True,state="disabled")
            self.switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
            self.switchPaket.place(x=272,y=90)
            if (slctd_paket=="Premium"): self.switchPaket.select() 
            else: self.switchPaket.deselect()
            btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27, text="Aktiviraj status",font=("Inter", 15), command=self.aktiviraj_paket)
            btnSacuvaj.place(x=89,y=132)
            
        wid.create_button(self.trenutni_window,"./src/img/Widget/btnOtkazi.png",x=136,y=166,width=72,height=17,command=self.trenutni_window.destroy)
    
    def clan_delete(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednog korisnika.")
            return
        
        pitaj = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabranog korisnika?")
        if not pitaj:
            return

        slctd_data = self.table.item(slctd_item)
        username = slctd_data["values"][0]
        
        if(not queries.obrisi_korisnika(username)): return

        self.table.delete(slctd_item)
        helperFunctions.obavestenje(title="Brisanje", poruka="Korisnik je uspešno obrisan.")
        
    
    def nagradi_lojalnost(self):
        username = self.entryID.get().split(",")[0].strip()
        queries.nagradi_lojalnost(username)
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        
    def aktiviraj_paket(self):
        username = self.entryID.get().split(",")[0].strip()
        paket=self.switchPaket.get()
        queries.aktiviraj_paket(username,paket)
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        