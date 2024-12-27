import bp_korisnici
from imports import *
from ctk_rangeslider import *
import bp_programi

class ProgramiWindow(winTemplate):
    def __init__(self, window, main_window,uloga):
        super().__init__(window, main_window,uloga)
        self.promenljive_filteri()

    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        self.create_button("./src/img/Widget/btnFilteri.png", 687, 53, 142, 33, self.winProgramiFilteri)
        
        visoki=True
        if self.uloga=="admin": 
            self.create_button("./src/img/Widget/btnDodaj.png", 23, 543, 252, 40, lambda: self.winProgrami_Dodaj())
            self.create_button("./src/img/Widget/btnIzmeni.png", 300, 543, 252, 40, lambda: self.winProgrami_Izmeni())
            self.create_button("./src/img/Widget/btnObrisi.png", 577, 543, 252, 40, self.obrisi_program)
            visoki=False
            
        self.create_entry_search(self.pretrazi)
        
        self.kriterijumi=["Šifra", "Naziv", "Vrsta treninga", "Trajanje", "Instruktor", "Potreban paket", "Opis"]
        self.kriterijumiMap={
            "Šifra" : "id_programa", 
            "Naziv" : "naziv_programa",
            "Vrsta treninga" : "naziv_vrste_treninga",
            "Trajanje" : "trajanje",
            "Instruktor" : "instruktor_ime",
            "Potreban paket" : "potreban_paket",
            "Opis" : "opis"
        }
        
        self.create_cmbbxSearch(self.kriterijumi,524,53)
        
        self.create_table(self.kriterijumi,visoki)
        self.table.column("Potreban paket",width=100)
        self.table.column("Opis",width=100)
           

    def popuni_tabelu(self,tabela,kriterijum='id_programa',pretraga=''):
        for red in tabela.get_children(): tabela.delete(red)
                
        podaci=self.izlistaj_programe(kriterijum,pretraga)
        
        i=0
        for podatak in podaci:
            if(podatak[7]==1): 
                if(self.uloga=="admin"): tabela.insert("", "end", values=podatak[:-1],tags="obrisano"+str(i%2))
            else: tabela.insert("", "end", values=podatak[:-1],tags=str(i%2))
            i+=1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        
        
        for red in self.table.get_children():
            self.table.delete(red)
            
        if pretraga =="" or pretraga=="pretraži":
            pretraga=""
        else:
            if pretraga in "premium":
                pretraga = 1
            elif pretraga in "standard":
                pretraga = 0  
            else:
                pass

        self.popuni_tabelu(self.table,pretraga=pretraga,kriterijum=kriterijum)

    def winProgramiFilteri(self):
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(width=343,height=382,title="Filteri")

        self.cmbbxSifre=self.napravi_sql_cmbbx("Šifra:",64,39,172,31,"SELECT id_programa FROM Program WHERE obrisan IS NOT TRUE") #Kombo box za id
        self.cmbbxNaziv=self.napravi_sql_cmbbx("Naziv:",56,78,172,72,'SELECT DISTINCT Program.naziv FROM Program WHERE Program.obrisan IS NOT TRUE') #Kombo box za naziv
        self.filt_cmbbxVrsteTreninga=self.napravi_sql_cmbbx("Vrsta treninga:",26,121,172,115,'SELECT DISTINCT Vrste_treninga.naziv FROM Program JOIN Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga WHERE Vrste_treninga.obrisan IS NOT TRUE') #Kombo box za naziv
        self.filt_cmbbxInstruktor=self.napravi_sql_cmbbx("Trener:",52,233,172,225,"SELECT DISTINCT Korisnici.ime FROM Program JOIN Korisnici ON Program.id_instruktora = Korisnici.username WHERE Korisnici.username IS NOT 'obrisan_korisnik'") #Kombo box za naziv
        
        naziv = self.naziv if self.naziv != "" else "SVE"
        self.cmbbxNaziv.set(naziv)
        sifra = self.id_programa if self.id_programa != "" else "SVE"
        self.cmbbxSifre.set(sifra)
        naziv_vrste_treninga = self.naziv_vrste_treninga if self.naziv_vrste_treninga != "" else "SVE"
        self.filt_cmbbxVrsteTreninga.set(naziv_vrste_treninga)
        instruktor = self.instruktor if self.instruktor != "" else "SVE"
        self.filt_cmbbxInstruktor.set(instruktor)
        
        self.create_label("Potreban Premium Paket", 27, 280)
        self.filt_switchPaket=self.create_switch(252,278)        
        
        min,max=bp_programi.get_trajanje_range()
        self.create_label("Trajanje od do:",124,167)

        self.slajder=CTkRangeSlider(self.trenutni_window,height=16,width=288,from_=min, to=max,command=self.update_trajanje)
        self.slajder.configure(command=lambda value: self.update_trajanje())
        self.slajder.place(x=32,y=191)
        self.slajder.set([self.trajanjeOd,self.trajanjeDo])#nema funk jedini put da se pojavljuje
        
        
        self.entryTrajanjeOd=self.create_entry(32,166,width=59,height=18,auto_fin_fout=(True,"Polje"))
        self.entryTrajanjeDo=self.create_entry(261,166,width=59,height=18,auto_fin_fout=(True,"Polje"))
        self.entryTrajanjeOd.bind("<Return>", lambda event:self.apdejtuj_slajder(self.entryTrajanjeOd.get(),self.trajanjeDo))
        self.entryTrajanjeDo.bind("<Return>", lambda event: self.apdejtuj_slajder(self.trajanjeOd, self.entryTrajanjeDo.get()))
        self.update_trajanje()
        
        if (self.potrebanPaket): self.filt_switchPaket.select() 
        else: self.filt_switchPaket.deselect()
        
        self.create_text_button("Sačuvaj",102,323,self.ugasi_filteri)
        
        self.create_button("./src/img/Widget/btnObrisiFiltere.png", 135, 357, 72, 17, self.restartuj_filtere)
        self.top_level=False
        
    def on_entry_trajanjeOd_click(self,event):
        self.entryTrajanjeOd.configure(text_color="white")

    def on_focus_out_trajanjeOd(self,event):
        if self.entryTrajanjeOd.get() == "":
            self.entryTrajanjeOd.insert(0, self.trajanjeOd)
        self.entryTrajanjeOd.configure(text_color="gray")
        self.apdejtuj_slajder(self.entryTrajanjeOd.get(),self.trajanjeDo)
        
    def on_entry_trajanjeDo_click(self, event):
        self.entryTrajanjeDo.configure(text_color="white")

    def on_focus_out_trajanjeDo(self, event):
        if self.entryTrajanjeDo.get() == "":
            self.entryTrajanjeDo.insert(0, self.trajanjeDo)
        self.entryTrajanjeDo.configure(text_color="gray")
        self.apdejtuj_slajder(self.trajanjeOd, self.entryTrajanjeDo.get())

    def apdejtuj_slajder(self,x,y):
        self.slajder.set([int(x),int(y)])
        self.update_trajanje()
            
    def update_trajanje(self):
        self.trajanjeOd, self.trajanjeDo = self.slajder.get()
        
        self.entryTrajanjeOd.delete(0, ctk.END)
        self.entryTrajanjeOd.insert(0, int(self.trajanjeOd))
        
        self.entryTrajanjeDo.delete(0, ctk.END)
        self.entryTrajanjeDo.insert(0, int(self.trajanjeDo))
    
    def restartuj_filtere(self):
        self.promenljive_filteri()
        self.trenutni_window.destroy()
        self.trenutni_window = None
        self.popuni_tabelu(self.table)

    def izlistaj_programe(self,kriterijum='id_programa',pretraga=""):              
        return bp_programi.izlistaj_programe(pretraga,kriterijum,self.potrebanPaket,self.id_programa,self.naziv,self.naziv_vrste_treninga,self.trajanjeOd,self.trajanjeDo,self.instruktor)
    
    def promenljive_filteri(self):
        self.trajanjeOd, self.trajanjeDo=bp_programi.get_trajanje_range()
        self.potrebanPaket=1
        self.id_programa=''
        self.naziv=''
        self.naziv_vrste_treninga=''
        self.instruktor=''
    
    def ugasi_filteri(self):
        id=self.cmbbxSifre.get()
        self.id_programa = "" if id == "SVE" else id
        
        naziv=self.cmbbxNaziv.get()
        self.naziv = "" if naziv == "SVE" else naziv
        
        vrste_treninga=self.filt_cmbbxVrsteTreninga.get()
        self.naziv_vrste_treninga = "" if vrste_treninga == "SVE" else vrste_treninga
        
        instruktor=self.filt_cmbbxInstruktor.get()
        self.instruktor = "" if instruktor == "SVE" else instruktor
    
        self.potrebanPaket=self.filt_switchPaket.get()

        self.trenutni_window.destroy()
        self.trenutni_window = None
        self.popuni_tabelu(self.table)
    
    def obrisi_program(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan program za brisanje.")
            return
        
        slctd_data = self.table.item(slctd_item)
        program_id = slctd_data["values"][0]
        obrisan = self.table.item(slctd_item, "tags")

        totalno=False
        for tag in obrisan:
            if "obrisano" in tag:
                totalno=helperFunctions.pitaj("Ako obišete već obrisan program, on će biti trajno\n obrisan kao i sve što je vezano za njega.\n Da li ste sigurni da želite da nastavite?","Brisanje")
            
        if not totalno:
            if not helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabrani program?"):
                return
       
        bp_programi.obrisi_program(id_programa=program_id,totalno=totalno)
        
        self.popuni_tabelu(self.table)
        helperFunctions.obavestenje(title="Brisanje", poruka="Program je uspešno obrisan.")
                
    def winProgrami_Izmeni(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan program za izmenu.")
            return
        obrisan = self.table.item(slctd_item, "tags")

        for tag in obrisan:
            if "obrisano" in tag:
                helperFunctions.obavestenje("Ne možete izmeniti već obrisan program.",crveno=True)
                return
        self.top_level=True
        self.napravi_dodaj_izmeni_prozor()
        
        slctd_data = self.table.item(slctd_item)
        slctd_id = slctd_data["values"][0]
        slctd_naziv=slctd_data["values"][1]
        slctd_vrsta_treninga=slctd_data["values"][2]
        slctd_trajanje=str(slctd_data["values"][3]).split(" ")[0]
        slctd_instruktor=slctd_data["values"][4]
        slctd_paket=slctd_data["values"][5]
        if(slctd_paket=="Standard"):
            slctd_paket=0
        else:
            slctd_paket=1
        slctd_opis=slctd_data["values"][6]
        
        #Izmeni specificniwidgeti
        self.cmbbxVrsteTreninga=self.napravi_sql_cmbbx("Vrsta treninga:",26,121,172,115,"SELECT id_vrste_treninga, naziv FROM Vrste_treninga WHERE obrisan IS NOT TRUE",2,True) #Kombo box za naziv
        self.cmbbxInstruktor=self.napravi_sql_cmbbx("Trener:",52,220,172,212, "SELECT username,ime,prezime FROM Korisnici WHERE uloga=1 AND username IS NOT 'obrisan_korisnik'",3,True) #Kombo box za naziv
        
        self.selektuj_vrednost_comboBox(self.cmbbxVrsteTreninga,slctd_vrsta_treninga)
        self.selektuj_vrednost_comboBox(self.cmbbxInstruktor,slctd_instruktor)
        
        self.entrySifra=self.create_entry(141,30,width=179,height=23,belo=True,placeholder=slctd_id,state="disabled")
        
        self.zajednicke_Dodaj_Izmeni(slctd_naziv,slctd_trajanje,slctd_paket,slctd_opis,mode=1)
        self.top_level=False

    def winProgrami_Dodaj(self):
        self.top_level=True
        self.napravi_dodaj_izmeni_prozor()
        
        self.cmbbxVrsteTreninga=self.napravi_sql_cmbbx("Vrsta treninga:",26,121,172,115,"SELECT id_vrste_treninga, naziv FROM Vrste_treninga WHERE obrisan IS NOT TRUE",2,True) #Kombo box za naziv
        self.cmbbxInstruktor=self.napravi_sql_cmbbx("Trener:",52,220,172,212, "SELECT username,ime,prezime FROM Korisnici WHERE uloga=1 AND username IS NOT 'obrisan_korisnik'",3,True) #Kombo box za naziv
        
        self.entrySifra=self.create_entry(141,30,width=179,height=23,belo=True)
        
        self.zajednicke_Dodaj_Izmeni(mode=0)
        self.top_level=False
        
    def zajednicke_Dodaj_Izmeni(self,naziv="",trajanje="",paket=1,opis="",mode=0): # 0 za dodaj 1 za izmeni
        self.top_level=True
        # Postavljanje switch-a i label-e za potreban paket
        self.create_label("Potreban Premium Paket",60,280)
        self.switchPaket=self.create_switch(252,278)
        
        if (paket): self.switchPaket.select() 
        else: self.switchPaket.deselect()
        
        # sifra labela
        self.create_label("Šifra:",58,31)
        
        #ulaz za trajanje
        self.create_label("Trajanje:",46,169)
        self.entryTrajanje=self.create_entry(141,168,width=179,height=23,belo=True,placeholder=trajanje)
        
        #ulaz za naziv programa
        self.create_label("Naziv:",58,79)
        self.entryNaziv = self.create_entry(141,74,width=179,height=23,belo=True,placeholder=naziv)
        
        
        #ulaz za opis
        self.create_label("Opis:",27,308)

        self.txtbxOpis = ctk.CTkTextbox(self.trenutni_window,width=294,height=80,corner_radius=4,fg_color="#080A17")# i ovo se pojavljuje 2 puta ne vredi
        self.txtbxOpis.place(x=26,y=334)
        self.txtbxOpis.insert("0.0", opis)
        
        self.create_text_button("Sačuvaj",102,424,lambda: self.dodaj_izmeni_program(mode=mode))
        #dugme za otkazivanje
        self.create_button("./src/img/Widget/btnOtkazi.png", 136, 461, 72, 17, self.trenutni_window.destroy)
        self.top_level=False

        
        
    def dodaj_izmeni_program(self,mode=0):
        if(mode==1): 
            if(not helperFunctions.pitaj(title="Izmeni program",poruka="Da li ste sigurni da želite da izmenite program?")):return
        id=self.entrySifra.get()
        naziv=self.entryNaziv.get()
        vrsta_treninga=self.cmbbxVrsteTreninga.get()
        trajanje=self.entryTrajanje.get()
        instruktor=self.cmbbxInstruktor.get()
        paket=self.switchPaket.get()
        opis=self.txtbxOpis.get("0.0", END)
        if(id=="" or (not id.isdigit())):
            helperFunctions.obavestenje("Šifra ne sme biti prazna ili sadržati slova.")
            return
        if(naziv==""):
            helperFunctions.obavestenje("Naziv ne sme biti prazan.")
            return
        if(vrsta_treninga==""):
            helperFunctions.obavestenje("Vrsta treninga ne sme biti prazana.")
            return
        if(not trajanje.isdigit()):
            helperFunctions.obavestenje("Trajanje mora biti broj.")
            return
        if(instruktor==""):
            helperFunctions.obavestenje("Instruktor polje ne sme biti prazno.")
            return
        vrsta_treninga=vrsta_treninga.split(" ")[0]
        instruktor=instruktor.split(" ")[0]

        if(mode):
            if(bp_programi.azuriraj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis)): return
            helperFunctions.obavestenje(title="Izmena programa", poruka="Uspešno izmenjen program.")
        else:
            if(bp_programi.dodaj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis)): return
            helperFunctions.obavestenje(title="Dodaj program", poruka="Uspešno dodat program.")
        
        self.trenutni_window.destroy()
        self.trenutni_window=None
        
        self.txtbxOpis=None
        self.entryNaziv=None
        self.entrySifra=None
        self.cmbbxInstruktor=None
        self.cmbbxVrsteTreninga=None
        
        self.popuni_tabelu(self.table)
        
    def napravi_dodaj_izmeni_prozor(self):
        self.trenutni_window = helperFunctions.napravi_toplevel(height=485,title="Program")