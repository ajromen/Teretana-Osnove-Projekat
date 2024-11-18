from tkinter import *
import customtkinter as ctk
import queries
import helperFunctions
from ctk_rangeslider import *
import widgets as wid


class ProgramiWindow:
    def __init__(self, window, main_window,uloga):
        self.window = window
        self.main_window=main_window
        self.uloga=uloga
        self.current_canvas = None
        self.promenljive_filteri()

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        wid.create_button(self.current_canvas,"./src/img/Widget/btnExit.png",812,9,33,33,lambda: self.main_window.unisti_trenutni_win())# EXit dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnSearch.png",358,53,33,33,self.pretrazi) # Search dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnFilteri.png",687,55,142,33,self.winProgramiFilteri) # Filteri Dugme
        self.uloga=="admin" and wid.create_button(self.current_canvas,"./src/img/Widget/btnDodaj.png",23,543,252,40,lambda: self.winProgrami_Dodaj()) # Dodaj Dugme
        self.uloga=="admin" and wid.create_button(self.current_canvas,"./src/img/Widget/btnIzmeni.png",300,543,252,40,lambda: self.winProgrami_Izmeni()) # Izmeni Dugme
        self.uloga=="admin" and wid.create_button(self.current_canvas,"./src/img/Widget/btnObrisi.png",577,543,252,40,self.obrisi_program) # Obrisi Dugme
        
        
        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/searchPozadina.png",23,53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/tabelaPozadina.png",23,102)

        
        self.entrySearch=wid.create_entry_search(self.current_canvas,self.pretrazi)
        
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
        self.current_canvas.create_text(450,65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch=wid.create_comboBox(self.current_canvas,self.kriterijumi,524,55)
        
        self.table=wid.create_table(self.current_canvas,self.popuni_tabelu,self.kriterijumi)
           

    def popuni_tabelu(self,tabela):
        for red in tabela.get_children():
            tabela.delete(red)
                
        podaci=self.izlistaj_programe()
        
        for podatak in podaci:
            tabela.insert("", "end", values=podatak)

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())

        if not kriterijum:
            helperFunctions.obavestenje("Nije moguće pretražiti nepostijeći kriterijum.")
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
            else:
                pass

        podaci=self.izlistaj_programe(pretraga=pretraga,kriterijum=kriterijum)
        
        for podatak in podaci:
            self.table.insert("", "end", values=podatak)

    def winProgramiFilteri(self):
        self.trenutni_window = ctk.CTkToplevel(fg_color='#000000')
        self.trenutni_window.title("Filteri")
        self.trenutni_window.geometry("343x382")
        self.trenutni_window.resizable(False,False)
        helperFunctions.centerWindow(self.trenutni_window)

        self.cmbbxSifre=wid.napravi_sql_cmbbx(self.trenutni_window,"Šifra:",64,39,172,31,"SELECT id_programa FROM Program") #Kombo box za id
        self.cmbbxNaziv=wid.napravi_sql_cmbbx(self.trenutni_window,"Naziv:",56,78,172,72,"SELECT DISTINCT naziv FROM Program") #Kombo box za naziv
        self.filt_cmbbxVrsteTreninga=wid.napravi_sql_cmbbx(self.trenutni_window,"Vrsta treninga:",26,121,172,115,"SELECT DISTINCT Vrste_treninga.naziv FROM Program JOIN Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga") #Kombo box za naziv
        self.filt_cmbbxInstruktor=wid.napravi_sql_cmbbx(self.trenutni_window,"Trener:",52,233,172,225,"SELECT DISTINCT Korisnici.ime FROM Program JOIN Korisnici ON Program.id_instruktora = Korisnici.username") #Kombo box za naziv
        
        naziv = self.naziv if self.naziv != "" else "SVE"
        self.cmbbxNaziv.set(naziv)
        sifra = self.id_programa if self.id_programa != "" else "SVE"
        self.cmbbxSifre.set(sifra)
        naziv_vrste_treninga = self.naziv_vrste_treninga if self.naziv_vrste_treninga != "" else "SVE"
        self.filt_cmbbxVrsteTreninga.set(naziv_vrste_treninga)
        instruktor = self.instruktor if self.instruktor != "" else "SVE"
        self.filt_cmbbxInstruktor.set(instruktor)
        
        wid.create_label(self.trenutni_window, text="Potreban Premium Paket:",x=27,y=280)
        
        self.filt_switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
        self.filt_switchPaket.place(x=252,y=278)
        
        
        queries.cursor.execute("SELECT MIN(trajanje), MAX(trajanje) FROM Program")
        rez=queries.cursor.fetchall()[0]
        min=rez[0]
        max=rez[1]
        wid.create_label(self.trenutni_window, text="Trajanje od do:",x=124,y=167)

        self.slajder=CTkRangeSlider(self.trenutni_window,height=16,width=288,from_=min, to=max,command=self.update_trajanje)
        self.slajder.configure(command=lambda value: self.update_trajanje())
        self.slajder.place(x=32,y=191)
        self.slajder.set([self.trajanjeOd,self.trajanjeDo])
        
        
        self.entryTrajanjeOd=wid.create_entry(canvas=self.trenutni_window,x=32,y=166,width=59,height=18,manual_fin_fon=(True,"Polje"))
        self.entryTrajanjeDo=wid.create_entry(canvas=self.trenutni_window,x=261,y=166,width=59,height=18,manual_fin_fon=(True,"Polje"))
        self.entryTrajanjeOd.bind("<Return>", lambda event:self.apdejtuj_slajder(self.entryTrajanjeOd.get(),self.trajanjeDo))
        self.entryTrajanjeDo.bind("<Return>", lambda event: self.apdejtuj_slajder(self.trajanjeOd, self.entryTrajanjeDo.get()))
        self.update_trajanje()
        
        if (self.potrebanPaket): self.filt_switchPaket.select() 
        else: self.filt_switchPaket.deselect()
        
        btnSacuvaj = ctk.CTkButton(self.trenutni_window, text="Sačuvaj", command=self.ugasi_filteri)
        btnSacuvaj.place(x=102,y=323)
        self.imgObrisiFiltere = PhotoImage(file="./src/img/Widget/btnObrisiFiltere.png")
        btnObrisiFiltere = Button(self.trenutni_window,image=self.imgObrisiFiltere, borderwidth=0, highlightthickness=0, relief="flat",command=self.restartuj_filtere) 
        btnObrisiFiltere.place(x=135,y=357,width=72,height=17)
        
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
        return queries.izlistaj_programe(pretraga,kriterijum,self.potrebanPaket,self.id_programa,self.naziv,self.naziv_vrste_treninga,self.trajanjeOd,self.trajanjeDo,self.instruktor)
    
    def promenljive_filteri(self):
        queries.cursor.execute("SELECT MIN(trajanje), MAX(trajanje) FROM Program")
        rez=queries.cursor.fetchall()[0]
        self.trajanjeOd=rez[0]
        self.trajanjeDo=rez[1]
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

        response = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabrani program?")
        if not response:
            return

        slctd_data = self.table.item(slctd_item)
        program_id = slctd_data["values"][0]  

        try:
            komanda = "DELETE FROM Program WHERE id_programa = ?"
            queries.cursor.execute(komanda, (program_id,))
            queries.connection.commit()

            self.table.delete(slctd_item)
            helperFunctions.obavestenje(title="Brisanje", poruka="Program je uspešno obrisan.")

        except Exception as e:
            helperFunctions.obavestenje(title="Greška", poruka=f"Došlo je do greške prilikom brisanja programa: {e}")
                
    def winProgrami_Izmeni(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan program za izmenu.")
            return
        
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
        self.cmbbxVrsteTreninga=wid.napravi_sql_cmbbx(self.trenutni_window,"Vrsta treninga:",26,121,172,115,"SELECT id_vrste_treninga, naziv FROM Vrste_treninga",2,True) #Kombo box za naziv
        self.cmbbxInstruktor=wid.napravi_sql_cmbbx(self.trenutni_window,"Trener:",52,220,172,212,"SELECT username,ime,prezime FROM Korisnici WHERE uloga=1",3,True) #Kombo box za naziv
        
        wid.selektuj_vrednost_comboBox(self.cmbbxVrsteTreninga,slctd_vrsta_treninga)
        wid.selektuj_vrednost_comboBox(self.cmbbxInstruktor,slctd_instruktor)
        
        self.entrySifra = wid.create_entry(self.trenutni_window,141,30,width=179,height=23,belo=True,placeholder=slctd_id,state="disabled")
        
        self.zajednicke_Dodaj_Izmeni(slctd_naziv,slctd_trajanje,slctd_paket,slctd_opis,mode=1)

    def winProgrami_Dodaj(self):
        self.napravi_dodaj_izmeni_prozor()
        
        self.cmbbxVrsteTreninga=wid.napravi_sql_cmbbx(self.trenutni_window,"Vrsta treninga:",26,121,172,115,"SELECT id_vrste_treninga, naziv FROM Vrste_treninga",2,True) #Kombo box za naziv
        self.cmbbxInstruktor=wid.napravi_sql_cmbbx(self.trenutni_window,"Trener:",52,220,172,212,"SELECT username,ime,prezime FROM Korisnici WHERE uloga=1",3,True) #Kombo box za naziv
        
        self.entrySifra = wid.create_entry(self.trenutni_window,141,30,width=179,height=23,belo=True)
        
        self.zajednicke_Dodaj_Izmeni(mode=0)
        
    def zajednicke_Dodaj_Izmeni(self,naziv="",trajanje="",paket=1,opis="",mode=0): # 0 za dodaj 1 za izmeni
        # Postavljanje switch-a i label-e za potreban paket
        wid.create_label(self.trenutni_window, text="Potreban Premium Paket:",x=60,y=280)
        self.switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
        self.switchPaket.place(x=252,y=278)
        
        if (paket): self.switchPaket.select() 
        else: self.switchPaket.deselect()
        
        # sifra labela
        wid.create_label(self.trenutni_window, text="Šifra:",x=58,y=31)
        
        #ulaz za trajanje
        wid.create_label(self.trenutni_window, text="Trajanje:",x=46,y=169)
        self.entryTrajanje = wid.create_entry(self.trenutni_window,141,168,width=179,height=23,belo=True,placeholder=trajanje)
        
        #ulaz za naziv programa
        wid.create_label(self.trenutni_window, text="Naziv:",x=58,y=79)
        self.entryNaziv = wid.create_entry(self.trenutni_window,141,74,width=179,height=23,placeholder=naziv,belo=True)
        
        
        #ulaz za opis
        wid.create_label(self.trenutni_window, text="Opis:",x=27,y=308)

        self.txtbxOpis = ctk.CTkTextbox(self.trenutni_window,width=294,height=80,corner_radius=4,fg_color="#080A17")
        self.txtbxOpis.place(x=26,y=334)
        self.txtbxOpis.insert("0.0", opis)
        
        
        btnSacuvaj = ctk.CTkButton(self.trenutni_window, text="Sačuvaj", command=lambda: self.dodaj_izmeni_program(mode=mode))
        btnSacuvaj.place(x=102,y=424)
        #dugme za otkazivanje
        self.imgOtkazi = PhotoImage(file="./src/img/Widget/btnOtkazi.png")
        btnOtkazi = Button(self.trenutni_window,image=self.imgOtkazi, borderwidth=0, highlightthickness=0, relief="flat",command=self.trenutni_window.destroy) 
        btnOtkazi.place(x=136,y=461,width=72,height=17)
        
        
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
            if(queries.azuriraj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis)): return
            helperFunctions.obavestenje(title="Izmena programa", poruka="Uspešno izmenjen program.")
        else:
            if(queries.dodaj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis)): return
            helperFunctions.obavestenje(title="Dodaj program", poruka="Uspešno dodat program.")
        queries.connection.commit()
        self.popuni_tabelu(self.table)
        
        self.trenutni_window.destroy()
        self.trenutni_window=None
        
        
        self.entryNaziv=None
        self.entrySifra=None
        self.cmbbxInstruktor=None
        self.cmbbxVrsteTreninga=None
        
    def napravi_dodaj_izmeni_prozor(self):
        self.trenutni_window = ctk.CTkToplevel(fg_color='#000000')
        self.trenutni_window.title("Program")
        self.trenutni_window.geometry("343x485")
        self.trenutni_window.resizable(False,False)
        helperFunctions.centerWindow(self.trenutni_window) # Pravi se novi prozor za dodaj/izmeni