from imports import *
import bp_korisnici
 
class ClanoviWindow(winTemplate):
    def __init__(self, window, escfunk=None, uloga=None,username=None, u_prozoru=False):
        super().__init__(window, escfunk, uloga, u_prozoru, username)
        
        self.broj_rez_kluc="potreban_broj_za_rezervacije"
        broj_rez=helperFunctions.ucitaj_iz_setup(self.broj_rez_kluc)
        self.broj_rezervacija_za_nagradjivanje=int(broj_rez) if broj_rez else 27
        

    def start(self):
        self.create_canvas()      
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        
        self.uloga=="admin" and self.create_button("./src/img/widget/btnNagradi.png",23,541,252,40,lambda: self.winClan_Izmeni("Nagradi")) # Dodaj Dugme
        
        self.create_button("./src/img/widget/btnAktiviraj.png",300,541,252,40,lambda: self.winClan_Izmeni("Aktiviraj"))
        self.create_button("./src/img/widget/btnObrisi.png", 576, 541, 252, 40, self.clan_delete)
        
        self.kriterijumiMap={
            "Korisničko ime" : "username",
            "Ime" : "ime",
            "Prezime" : "prezime",
            "Članstvo" : "status_clanstva",
            "Paket" : "uplacen_paket",
            "Datum registracije" : "datum_registracije",
        }
        self.kriterijumi=["Korisničko ime", "Ime", "Prezime", "Članstvo", "Paket","Datum registracije","Članarina obnovljena","Broj rezervacija"]
        
        self.create_entry_search(self.pretrazi)
        
        self.create_cmbbxSearch(self.kriterijumi[:-2])
        
        self.create_table(self.kriterijumi)
        self.table.column("Korisničko ime", width=90)
        self.table.column("Ime", width=100)
        self.table.column("Prezime", width=100)
        self.table.column("Datum registracije", width=100)
        self.table.column("Članarina obnovljena", width=120)    
        
        self.create_label("Zahtev za nagradu: ",421,62,12)
        self.entryBrojNagrada=self.create_entry(540,59,width=59,height=23,placeholder=self.broj_rezervacija_za_nagradjivanje,justify="center",belo=True)
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
        for red in tabela.get_children(): tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum=kriterijum,pretraga=pretraga)
        
        i=0
        for podatak in podaci:
            podatak=list(podatak)
            username=podatak[0]
            broj_rezervacija=bp_korisnici.broj_rezervacija_za_mesec(username)
            podatak.append(broj_rezervacija)
            if podatak[0]=="obrisan_korisnik": 
                continue
            elif(broj_rezervacija>=self.broj_rezervacija_za_nagradjivanje):
                tabela.insert("", "end", values=podatak,tags="za_aktivaciju")
            else: tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())

        for red in self.table.get_children():
            self.table.delete(red)
            
        if pretraga =="" or pretraga=="pretraži": pretraga=""
        else:
            if pretraga in "premium": pretraga = 1
            elif pretraga in "standard": pretraga = 0  
            elif pretraga in "aktiviran": pretraga = 1
            elif pretraga in "neaktiviran": pretraga = 0  
        
        self.popuni_tabelu(self.table,kriterijum=kriterijum,pretraga=pretraga)

    def izlistaj(self,kriterijum='username',pretraga=""):              
        return bp_korisnici.izlistaj_korisnike(pretraga,kriterijum)
    
    
    def winClan_Izmeni(self,mode="Nagradi"):# ili Aktiviraj
        self.top_level=True
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
        
        self.entryID=self.create_entry(70,11,width=203,height=23,placeholder=slctd_username+", "+slctd_ime+" "+slctd_prezime,justify="center",belo=True,state="disabled")
        
        if(mode=="Nagradi"):
            self.create_label("Broj realizovanih rezervacija u proteklih",45,52,font_size=15)
            self.create_label("mesec dana:",137,70,font_size=15)
            self.entryBrDana=self.create_entry(151,96,width=41,height=23,placeholder=slctd_br_rez,justify="center",belo=True,state="disabled")
            za_aktivaciju=slctd_data.get("tags")[0]
            if(za_aktivaciju=='za_aktivaciju'):
                self.create_text_button("Nagradi lojalnost", 89, 132, self.nagradi_lojalnost, width=166, height=27,hover_color=boje.dugme_zeleno_hover,fg_color=boje.dugme_zeleno)
            else:
                self.create_text_button("Nagradi lojalnost", 89, 132, lambda: None, width=166, height=27,hover_color=boje.dugme_disabled_hover,fg_color=boje.dugme_disabled)
        
        else:
            self.create_label("Trenutni status:",22,57)
            self.create_label("Premium paket:",22,93)
            self.entryStatus=self.create_entry(197,52,width=124,height=23,placeholder=slctd_aktiviran,justify="center",belo=True,state="disabled")
            self.switchPaket=self.create_switch(272,90)
            if (slctd_paket=="Premium"): self.switchPaket.select() 
            else: self.switchPaket.deselect()
            self.create_text_button("Aktiviraj status", 89, 132, self.aktiviraj_paket, width=166, height=27)
            
        self.create_button("./src/img/widget/btnOtkazi.png",x=136,y=166,width=72,height=17,command=self.trenutni_window.destroy)
        self.top_level=False
    
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
        
        if(not bp_korisnici.obrisi_korisnika(username)): return

        self.table.delete(slctd_item)
        helperFunctions.obavestenje(title="Brisanje", poruka="Korisnik je uspešno obrisan.")
        
    
    def nagradi_lojalnost(self):
        username = self.entryID.get().split(",")[0].strip()
        bp_korisnici.nagradi_lojalnost(username)
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        
    def aktiviraj_paket(self):
        username = self.entryID.get().split(",")[0].strip()
        paket=self.switchPaket.get()
        bp_korisnici.aktiviraj_paket(username,paket)
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        