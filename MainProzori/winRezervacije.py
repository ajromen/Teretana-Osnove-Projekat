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
        self.create_button("./src/img/widget/btnDodaj.png", 23, 541, 252, 40, self.rezervacija_dodaj)  
         
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
        if bp_korisnici.obnovljena_clanarina(self.username)==False:
            helperFunctions.obavestenje(poruka="Vaša članarina je istekla. Molimo vas da obnovite članarinu.",crveno=True)
            return
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(title="Rezervisi trening",height=207)
        
        self.create_label("Šifra termina:", 31, 31)
        self.create_label("Oznaka mesta:", 39, 86)
        
        self.btnTermin=self.create_text_button("Izaberite termin", 154, 28, width=170,height=28, command=self.dodaj_termine)
        self.btnOznakaMesta=self.create_text_button("Izaberite oznaku mesta", 154, 83, width=170,height=28,fg_color=boje.dugme_disabled,hover_color=boje.dugme_disabled_hover,command=None)    
        
        self.btnSacuvaj=self.create_text_button("Sačuvaj", 102, 146,command=None,hover_color=boje.dugme_disabled_hover,fg_color=boje.dugme_disabled)
        self.create_button("./src/img/widget/btnOtkazi.png",136,183,command=self.trenutni_window.destroy)
        
        self.top_level=False
    
    def dodaj_termine(self):
        self.dodatni_window=helperFunctions.napravi_toplevel(title="Izaberite termin",height=608,width=850)
        self.dodatni_window.protocol("WM_DELETE_WINDOW", self.dodaj_termine_kraj)
        termini_window=winTermini.TerminiWindow(self.dodatni_window,lambda termin:self.dodaj_termine_kraj(termin),u_prozoru=True,username=self.username)
        termini_window.start()
        
    def dodaj_termine_kraj(self, termin="Izaberite termin"):
        self.dodatni_window.destroy()
        self.trenutni_window.grab_set()
        self.btnTermin.configure(text=termin)
        helperFunctions.onemoguci_dugme(self.btnOznakaMesta)
        helperFunctions.onemoguci_dugme(self.btnSacuvaj)
        self.btnOznakaMesta.configure(text="Izaberite oznaku mesta")
        self.sala=None
        self.btnOznakaMesta.configure(command=None)
        if termin=="Izaberite termin":
            return
        self.termin=termin.strip()
        self.sala=bp_termini.get_sala(termin)
        helperFunctions.omoguci_dugme(self.btnOznakaMesta,self.dodaj_oznaka_mesta)
        
    def dodaj_oznaka_mesta(self):
        self.sale_window=winSale.SaleWindow(self.sala,lambda oznaka_mesta="Izaberite oznaku mesta":self.dodaj_oznaka_mesta_kraj(oznaka_mesta))
        self.sale_window.start()
        
    def dodaj_oznaka_mesta_kraj(self,oznaka_mesta="Izaberite oznaku mesta"):
        self.btnOznakaMesta.configure(text=oznaka_mesta)
        self.sale_window.window.destroy()
        self.trenutni_window.grab_set()
        
        if oznaka_mesta=="Izaberite oznaku mesta": 
            helperFunctions.onemoguci_dugme(self.btnSacuvaj)
            return
        self.oznaka_mesta=oznaka_mesta.strip()
        helperFunctions.omoguci_dugme(self.btnSacuvaj,self.rezervacija_dodaj_kraj)
         
    def rezervacija_dodaj_kraj(self):
        danas=datetime.datetime.now().strftime("%Y-%m-%d")
        bp_rezervacije.dodaj_rezervaciju(self.username,self.termin,self.oznaka_mesta,danas)
        self.trenutni_window.destroy()
        self.pretrazi()
    
    def rezervacija_izmeni(self):
        pass
    
    def omoguci_sacuvaj(self):
        self.btnSacuvaj.configure(state="disabled")
    
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
       