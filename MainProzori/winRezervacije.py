import bp_korisnici
import bp_rezervacije
import bp_termini
from imports import *
import winSale
import winTermini

class RezervacijeWindow(winTemplate):
    def __init__(self, window, escfunk=None, uloga=None,username=None, u_prozoru=False):
        super().__init__(window, escfunk, uloga, u_prozoru, username)
        self.username=username
        self.termin=None
        self.oznaka_mesta=None
        self.odabrani_korisnik=None
        self.odabrana_rezervacija=None
        
    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        
        kriterijumi=["Šifra termina","Datum održavanja","Oznaka mesta","Datum rezervacije","Šifra rezervacije"]
        if self.uloga=="instruktor" or self.uloga=="admin":
            kriterijumi.insert(4,"Korisnik")#username ime i prezime
            self.create_button("./src/img/widget/btnIzmeni.png",300,541,252,40,self.rezervacija_izmeni)
        else:
            kriterijumi.insert(4,"Instruktor")#ime i prezime
        
        self.create_table(kriterijumi) 
        
        self.create_button("./src/img/widget/btnObrisi.png", 576, 541, 252, 40, self.rezervacija_obrisi)
        btnDodaj=self.create_button("./src/img/widget/btnDodaj.png", 23, 541, 252, 40, self.rezervacija_dodaj)  
        if self.uloga=="instruktor":
            btnDodaj.configure(command=self.promeni_rezervaciju)
         
        self.kriterijumiMap={
            "Šifra termina" : "Rezervacija.id_termina",
            "Datum održavanja" : "Termin.datum_odrzavanja",
            "Oznaka mesta" : "Rezervacija.oznaka_reda_kolone",
            "Datum rezervacije" : "Rezervacija.datum",
            "Korisnik" : "korisnik",
            "Instruktor" : "instruktor",
            "Šifra rezervacije" : "Rezervacija.id_rezervacije",
        }
        
        self.create_entry_search(self.pretrazi)
        self.create_cmbbxSearch(kriterijumi)
    
        
    def rezervacija_dodaj(self):
        if bp_korisnici.get_status(self.username)==False:
            helperFunctions.obavestenje(poruka="Vaša članarina je istekla. Molimo vas da obnovite članarinu.",crveno=True)
            return
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(title="Rezervacija",height=207)
        
        self.create_label("Šifra termina:", 31, 31)
        self.create_label("Oznaka mesta:", 39, 86)
        
        self.btnTermin=self.create_text_button("Izaberite termin", 154, 28, width=170,height=28, command=self.izaberi_termine)
        self.btnOznakaMesta=self.create_text_button("Izaberite oznaku mesta", 154, 83, width=170,height=28,fg_color=boje.dugme_disabled,hover_color=boje.dugme_disabled_hover,command=None)    
        
        self.btnSacuvaj=self.create_text_button("Sačuvaj", 102, 146,command=None,hover_color=boje.dugme_disabled_hover,fg_color=boje.dugme_disabled)
        self.create_button("./src/img/widget/btnOtkazi.png",136,183,command=self.trenutni_window.destroy)
        
        self.top_level=False
    
    def izaberi_termine(self):
        self.dodatni_window=helperFunctions.napravi_toplevel(title="Izaberite termin",height=608,width=850)
        self.dodatni_window.protocol("WM_DELETE_WINDOW", lambda:self.izaberi_termine_kraj(self.termin))
        termini_window=winTermini.TerminiWindow(self.dodatni_window,lambda termin:self.izaberi_termine_kraj(termin),self.uloga,u_prozoru=True,username=self.username,username_korisnika=self.odabrani_korisnik,selektovani_termin=self.termin)
        termini_window.start()
        
    def izaberi_termine_kraj(self, termin="Izaberite termin"):
        self.dodatni_window.destroy()
        self.trenutni_window.grab_set()
        self.btnTermin.configure(text=termin)
        helperFunctions.onemoguci_dugme(self.btnOznakaMesta)
        helperFunctions.onemoguci_dugme(self.btnSacuvaj)
        self.btnOznakaMesta.configure(text="Izaberite oznaku mesta")
        self.sala=None
        self.btnOznakaMesta.configure(command=None)
        if termin=="Izaberite termin" or termin==None:
            return
        self.termin=termin.strip()
        self.sala=bp_termini.get_sala(termin)
        helperFunctions.omoguci_dugme(self.btnOznakaMesta,self.izaberi_oznaku_mesta)
        
    def izaberi_oznaku_mesta(self):
        self.sale_window=winSale.SaleWindow(self.sala,lambda oznaka_mesta="Izaberite oznaku mesta":self.izaberi_oznaku_mesta_kraj(oznaka_mesta),id_termina=self.termin,oznaka_mesta=self.oznaka_mesta,id_rezervacije=self.odabrana_rezervacija)
        self.sale_window.start()
        
    def izaberi_oznaku_mesta_kraj(self,oznaka_mesta="Izaberite oznaku mesta"):
        self.btnOznakaMesta.configure(text=oznaka_mesta)
        self.sale_window.window.destroy()
        self.trenutni_window.grab_set()
        
        if oznaka_mesta=="Izaberite oznaku mesta" or oznaka_mesta==None: 
            self.oznaka_mesta=None
            helperFunctions.onemoguci_dugme(self.btnSacuvaj)
            return
        self.oznaka_mesta=oznaka_mesta.strip()
        helperFunctions.omoguci_dugme(self.btnSacuvaj,self.rezervacija_dodaj_kraj)
         
    def rezervacija_dodaj_kraj(self):
        danas=datetime.datetime.now().strftime("%Y-%m-%d")
        bp_rezervacije.dodaj_rezervaciju(self.username,self.termin,self.oznaka_mesta,danas)
        self.trenutni_window.destroy()
        self.pretrazi()
    
    def promeni_rezervaciju(self):
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(title="Rezervacija",height=272)
        
        self.create_label("Šifra termina:", 25, 85)
        self.create_label("Oznaka mesta:", 33, 140)
        
        self.varKorisnik=StringVar()
        self.cmbbxKorisnici=self.napravi_sql_cmbbx("Izaberite korisnika:", 21, 32, 174, 24, "SELECT username,ime,prezime FROM Korisnici WHERE uloga=0 AND username IS NOT 'obrisan_korisnik'",3,True,variable=self.varKorisnik,font_size=12)
        self.varKorisnik.trace_add("write",self.promenjen_korisnik)
        if self.odabrani_korisnik:
            self.selektuj_vrednost_comboBox(self.cmbbxKorisnici,self.odabrani_korisnik)
        else:
            self.odabrani_korisnik=self.cmbbxKorisnici.get().split(" ")[0]
        
        self.btnTermin=self.create_text_button("Izaberite termin", 154, 82, width=170,height=28, command=self.izaberi_termine)
        self.btnOznakaMesta=self.create_text_button("Izaberite oznaku mesta", 154, 137, width=170,height=28,fg_color=boje.dugme_disabled,hover_color=boje.dugme_disabled_hover,command=None)    
             
        self.btnSacuvaj=self.create_text_button("Sačuvaj", 102, 199,command=None,hover_color=boje.dugme_disabled_hover,fg_color=boje.dugme_disabled)
        self.create_button("./src/img/widget/btnOtkazi.png",136,236,command=self.trenutni_window.destroy)
        self.top_level=False
    
    def promenjen_korisnik(self,*args):
        if self.varKorisnik.get()=='':
            return
        korisnik=self.cmbbxKorisnici.get().split(" ")[0]
        status_korisnika=bp_korisnici.get_status(korisnik)
        if status_korisnika==False:
            helperFunctions.obavestenje(poruka="Odabrani korisnik nema aktivnu članarinu.",crveno=True)
            self.selektuj_vrednost_comboBox(self.cmbbxKorisnici,self.odabrani_korisnik)
            return
        
        if self.termin is None:
            self.odabrani_korisnik=korisnik
            return
        potreban_premium=bp_termini.get_paket(self.termin)
        paket_korisnika=bp_korisnici.get_paket(korisnik)
        if paket_korisnika==0 and potreban_premium:
            helperFunctions.obavestenje(poruka="Za ovaj termin je potreban Premium paket, a korisnik ima Standard.",crveno=True)
            self.selektuj_vrednost_comboBox(self.cmbbxKorisnici,self.odabrani_korisnik)
            return
        self.odabrani_korisnik=korisnik
        
    
    def rezervacija_izmeni(self):
        slctd_item=self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednu rezervaciju za izmenu.",crveno=True)
            return
        slctd_data=self.table.item(slctd_item)
        if datetime.datetime.strptime(slctd_data["values"][1],"%Y-%m-%d")<datetime.datetime.now():
            helperFunctions.obavestenje(poruka="Nije moguće izmeniti rezervaciju koja je već prošla.",crveno=True)
            return
        self.promeni_rezervaciju()
        self.odabrani_korisnik=slctd_data["values"][4].split(" ")[0]
        self.termin=slctd_data["values"][0]
        self.oznaka_mesta=str(slctd_data["values"][2])
        self.odabrana_rezervacija=slctd_data["values"][5]
        self.sala=bp_termini.get_sala(self.termin)
        
        
        
        self.selektuj_vrednost_comboBox(self.cmbbxKorisnici,self.odabrani_korisnik)
        
        helperFunctions.omoguci_dugme(self.btnTermin,self.izaberi_termine)
        helperFunctions.omoguci_dugme(self.btnOznakaMesta,self.izaberi_oznaku_mesta)
        helperFunctions.omoguci_dugme(self.btnSacuvaj,self.rezervacija_izmeni_kraj)
        
        self.btnOznakaMesta.configure(text=self.oznaka_mesta)
        self.btnTermin.configure(text=self.termin)
        
    
    def rezervacija_izmeni_kraj(self):
        danas=datetime.datetime.now().strftime('%Y-%m-%d')
        bp_rezervacije.azuriraj_rezervaciju(self.odabrana_rezervacija,self.odabrani_korisnik,self.termin,self.oznaka_mesta,danas)
        self.trenutni_window.destroy()
        self.pretrazi()
        self.odabrana_rezervacija=None
        
    
    def rezervacija_obrisi(self):
        slctd_item=self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednu rezervaciju za brisanje.",crveno=True)
            return
        slctd_data=self.table.item(slctd_item)
        id_rezervacije=slctd_data["values"][5]
        datum_termina=slctd_data["values"][1]
        if datetime.datetime.strptime(datum_termina,"%Y-%m-%d")<datetime.datetime.now():
            helperFunctions.obavestenje(poruka="Nije moguće obrisati rezervaciju koja je već prošla.",crveno=True)
            return
        if not helperFunctions.pitaj(poruka="Da li ste sigurni da želite da obrišete rezervaciju?"):
            return
        bp_rezervacije.obrisi_rezervaciju(id_rezervacije)
        self.pretrazi()
        helperFunctions.obavestenje(poruka="Uspešno ste obrisali rezervaciju.")
        
    def popuni_tabelu(self,tabela,kriterijum='username',pretraga=""):
        for red in tabela.get_children(): tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum=kriterijum,pretraga=pretraga)
        
        i=0
        for podatak in podaci:
            tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())

        for red in self.table.get_children():
            self.table.delete(red)
            
        if pretraga =="" or pretraga=="pretraži": pretraga=""
        
        self.popuni_tabelu(self.table,kriterijum=kriterijum,pretraga=pretraga)

    def izlistaj(self,kriterijum='id_rezervacije',pretraga=""):
        if self.uloga=="instruktor" or self.uloga=="admin":     
            return bp_rezervacije.izlistaj_po_instruktoru(kriterijum,pretraga,self.username)
        return bp_rezervacije.izlistaj_po_korisniku(kriterijum,pretraga,self.username)
       