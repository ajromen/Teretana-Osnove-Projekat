from imports import *
import re
import bp_korisnici

class AdminWindow(winTemplate):
    def __init__(self, window, escfunk=None, uloga=None,username=None, u_prozoru=False):
        super().__init__(window, escfunk, uloga, u_prozoru, username)
        self.title="Administratori i instruktori"

    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)       
        
        self.create_button("./src/img/widget/btnDodaj.png",23,543,252,40,lambda: self.winAdmin_Dodaj()) # Dodaj Dugme
        self.create_button("./src/img/widget/btnObrisi.png",577,543,252,40,self.obrisi) # Obrisi Dugme
        
        self.kriterijumiMap={
            "Korisničko ime" : "username",
            "Ime" : "ime",
            "Uloga" : "uloga",
            "Prezime" : "prezime",
            "Članstvo" : "status_clanstva",
        }
        self.kriterijumi=["Korisničko ime", "Ime", "Prezime","Uloga","Datum registracije"]
        self.create_entry_search(self.pretrazi)
        
        self.create_cmbbxSearch(self.kriterijumi)
        
        self.create_table(self.kriterijumi)
        self.table.column("Korisničko ime", width=90)
        self.table.column("Ime", width=100)
        self.table.column("Prezime", width=100) 
        

    def popuni_tabelu(self,tabela,kriterijum='username',pretraga=""):
        for red in tabela.get_children(): tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum=kriterijum,pretraga=pretraga)
        
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
            elif pretraga in "instruktor":
                pretraga = 1
            elif pretraga in "admin":
                pretraga = 2
            else:
                pass
        
        self.popuni_tabelu(self.table,pretraga=pretraga,kriterijum=kriterijum)

    def izlistaj(self,kriterijum='username',pretraga=""):              
        return bp_korisnici.izlistaj_instruktore_admine(pretraga,kriterijum)
    
    def winAdmin_Dodaj(self):
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(height=341,title="Dodaj administrarota")
        
        self.create_label("Korisničko ime:",23,31)
        self.create_label("Ime:",62,76)
        self.create_label("Prezime:",46,120)
        self.create_label("Lozinka:",47,164)
        self.create_label("Administrator:",27,218)
        
        self.entryUsername=self.create_entry(141,30,width=179,height=23,auto_fin_fout=(True,"Polje"))
        self.entryIme=self.create_entry(141,74,width=179,height=23,auto_fin_fout=(True,"Polje"))
        self.entryPrezime=self.create_entry(141,118,width=179,height=23,auto_fin_fout=(True,"Polje"))
        self.entryLozinka=self.create_entry(141,162,width=179,height=23,auto_fin_fout=(True,"Lozinka"),placeholder="Lozinka")
        
        self.switchPaket=self.create_switch(272,215)

        self.create_text_button("Napravi nalog",88,268,self.napravi_nalog,width=166)
        self.create_button("./src/img/widget/btnOtkazi.png",136,303,72,17,command=self.trenutni_window.destroy)
        self.top_level=False
        
    def napravi_nalog(self):
        username=self.entryUsername.get().strip()
        ime=self.entryIme.get().strip()
        prezime=self.entryPrezime.get().strip()
        lozinka=self.entryLozinka.get()
        admin=self.switchPaket.get()
        
        if(username=="" or ime=="" or prezime==""):
            helperFunctions.obavestenje("Sva polja moraju biti popunjena",crveno=True)
            return 
        if(len(lozinka)<6):
            helperFunctions.obavestenje("Lozinka mora da sadrži više od 6 karaktera",crveno=True)
            return 
        if(not re.search(r'\d', lozinka)):
            helperFunctions.obavestenje("Lozinka mora sadržati bar jednu cifru",crveno=True)
            return 
        
        admin+=1
        datum_registracije=datetime.date.today().strftime("%Y-%m-%d")
        bp_korisnici.dodaj_korisnika(username, lozinka, ime, prezime, admin, 0, 0, datum_registracije, "")
        
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        
    def obrisi(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednog korisnika.",crveno=True)
            return
        
        pitaj = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabranog korisnika?")
        if not pitaj:
            return

        slctd_data = self.table.item(slctd_item)
        username = slctd_data["values"][0]

        bp_korisnici.obrisi_korisnika(username,True)

        self.popuni_tabelu(self.table)
        helperFunctions.obavestenje(title="Brisanje", poruka="Korisnik je uspešno obrisan.")
            
        