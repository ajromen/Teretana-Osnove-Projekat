def winProgrami_Dodaj(self):
        self.trenutni_window = ctk.CTkToplevel(fg_color='#000000')
        self.trenutni_window.title("Dodaj")
        self.trenutni_window.geometry("343x485")
        self.trenutni_window.resizable(False,False)
        helperFunctions.centerWindow(self.trenutni_window)

       
        self.dodaj_cmbbxVrsteTreninga=self.napravi_sql_cmbbx(self.trenutni_window,"Vrsta treninga:",26,121,172,115,"SELECT id_vrste_treninga, naziv FROM Vrste_treninga",2,True) #Kombo box za naziv
        self.izemni_cmbbxInstruktor=self.napravi_sql_cmbbx(self.trenutni_window,"Trener:",52,220,172,212,"SELECT username,ime,prezime FROM Korisnici WHERE uloga=1",3,True) #Kombo box za naziv
        
        lblPaket = ctk.CTkLabel(self.trenutni_window, text="Potreban Premium Paket:", font=("Inter",15 * -1),anchor='nw')
        lblPaket.place(x=60,y=280)
        self.dodaj_switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
        self.dodaj_switchPaket.place(x=252,y=278)
        
        if (self.potrebanPaket): self.dodaj_switchPaket.select() 
        else: self.dodaj_switchPaket.deselect()
        
        
        lblSifra = ctk.CTkLabel(self.trenutni_window, text="Šifra:", font=("Inter",15 * -1),anchor='nw')
        lblSifra.place(x=58,y=31)
        self.dodaj_entrySifra = self.create_entry(self.trenutni_window,141,30,width=179,height=23,belo=True)
        
        lblNaziv = ctk.CTkLabel(self.trenutni_window, text="Naziv:", font=("Inter",15 * -1),anchor='nw')
        lblNaziv.place(x=58,y=79)
        self.dodaj_entryNaziv = self.create_entry(self.trenutni_window,141,74,width=179,height=23,belo=True)
        
        lblTrajanje = ctk.CTkLabel(self.trenutni_window, text="Trajanje:", font=("Inter",15 * -1),anchor='nw')
        lblTrajanje.place(x=46,y=169)
        self.dodaj_entryTrajanje = self.create_entry(self.trenutni_window,141,168,width=179,height=23,belo=True)
        
        lblOpis = ctk.CTkLabel(self.trenutni_window, text="Opis:", font=("Inter",15 * -1),anchor='nw')
        lblOpis.place(x=27,y=308)
        
        
        self.dodaj_txtbxOpis = ctk.CTkTextbox(self.trenutni_window, width=294, height=80,corner_radius=4, fg_color="#080A17")
        self.dodaj_txtbxOpis.place(x=26,y=334)
        self.trenutni_window.bind("<Map>", lambda e: self.dodaj_txtbxOpis.focus_set())
        
        btnSacuvaj = ctk.CTkButton(self.trenutni_window, text="Dodaj", command=self.napravi_program)
        btnSacuvaj.place(x=102,y=424)
        self.imgOtkazi = PhotoImage(file="./src/img/Widget/btnOtkazi.png")
        btnObrisiFiltere = Button(self.trenutni_window,image=self.imgOtkazi, borderwidth=0, highlightthickness=0, relief="flat",command=self.trenutni_window.destroy) 
        btnObrisiFiltere.place(x=136,y=461,width=72,height=17)
        
    def napravi_program(self):
        id=self.entrySifra.get()
        naziv=self.entryNaziv.get()
        vrsta_treninga=self.cmbbxVrsteTreninga.get()
        trajanje=self.entryTrajanje.get()
        instruktor=self.cmbbxInstruktor.get()
        paket=self.switchPaket.get()
        opis=self.txtbxOpis.get("0.0", END)
        if(naziv==""):
            helperFunctions.obavestenje("Naziv ne sme biti prazan.")
            return
        if(id=="" or (not id.isdigit())):
            helperFunctions.obavestenje("Šifra ne sme biti prazna ili sadržati slova.")
            return
        if(vrsta_treninga==""):
            helperFunctions.obavestenje("Vrsta treninga ne sme biti prazna.")
            return
        if(not trajanje.isdigit()):
            helperFunctions.obavestenje("Trajanje mora biti broj.")
            return
        if(instruktor==""):
            helperFunctions.obavestenje("Instruktor polje ne sme biti prazno.")
            return
        instruktor=instruktor.split(" ")[0]
        vrsta_treninga=vrsta_treninga.split(" ")[0]
        
        if(queries.dodaj_program(id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis)): return
        helperFunctions.obavestenje(title="Dodaj program", poruka="Uspešno dodat program.")
        self.popuni_tabelu()

        self.trenutni_window.destroy()
        self.trenutni_window=None
        
    def azuriraj_program(self):
        if(not helperFunctions.pitaj(title="Izmeni program",poruka="Da li ste sigurni da želite da izmenite program?")):return
        naziv=self.izmeni_entryNaziv.get()
        vrsta_treninga=self.izmeni_cmbbxVrsteTreninga.get()
        trajanje=self.izmeni_entryTrajanje.get()
        instruktor=self.izemni_cmbbxInstruktor.get()
        paket=self.izmeni_switchPaket.get()
        opis=self.izmeni_txtbxOpis.get("0.0", END)
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
        
        if(queries.azuriraj_program(self.slctd_id,naziv,vrsta_treninga,trajanje,instruktor,paket,opis)): return
        helperFunctions.obavestenje(title="Izmena programa", poruka="Uspešno izmenjen program.")
        
        self.popuni_tabelu()
        
        self.trenutni_window.destroy()
        self.trenutni_window=None
        
        
def winProgrami_Izmeni(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan program za izmenu.")
            return
        
        slctd_data = self.table.item(slctd_item)
        self.slctd_id = slctd_data["values"][0]
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
        
        self.winProgrami_Dodaj_Izmeni(self.slctd_id,slctd_naziv,slctd_vrsta_treninga,slctd_trajanje,slctd_instruktor,slctd_paket,slctd_opis,mode=1)
        
        self.trenutni_window = ctk.CTkToplevel(fg_color='#000000')
        self.trenutni_window.title("Izmeni")
        self.trenutni_window.geometry("343x485")
        self.trenutni_window.resizable(False,False)
        helperFunctions.centerWindow(self.trenutni_window)

       
        self.izmeni_cmbbxVrsteTreninga=self.napravi_sql_cmbbx(self.trenutni_window,"Vrsta treninga:",26,121,172,115,"SELECT id_vrste_treninga, naziv FROM Vrste_treninga",2,True) #Kombo box za naziv
        self.izemni_cmbbxInstruktor=self.napravi_sql_cmbbx(self.trenutni_window,"Trener:",52,220,172,212,"SELECT username,ime,prezime FROM Korisnici WHERE uloga=1",3,True) #Kombo box za naziv
        self.selektuj_pravi(self.izmeni_cmbbxVrsteTreninga,slctd_vrsta_treninga)
        self.selektuj_pravi(self.izemni_cmbbxInstruktor,slctd_vrsta_treninga)
        
        lblPaket = ctk.CTkLabel(self.trenutni_window, text="Potreban Premium Paket:", font=("Inter",15 * -1),anchor='nw')
        lblPaket.place(x=60,y=280)
        self.izmeni_switchPaket=ctk.CTkSwitch(self.trenutni_window,width=43,height=24,text='')
        self.izmeni_switchPaket.place(x=252,y=278)
        
        if (self.potrebanPaket): self.izmeni_switchPaket.select() 
        else: self.izmeni_switchPaket.deselect()
        
        lblSifra = ctk.CTkLabel(self.trenutni_window, text="Šifra: "+str(self.slctd_id), font=("Inter",15 * -1),anchor='nw')
        lblSifra.place(x=142,y=29)
        
        lblNaziv = ctk.CTkLabel(self.trenutni_window, text="Naziv:", font=("Inter",15 * -1),anchor='nw')
        lblNaziv.place(x=58,y=79)
        self.izmeni_entryNaziv = self.create_entry(self.trenutni_window,141,74,width=179,height=23,placeholder=slctd_naziv,belo=True)
        
        lblTrajanje = ctk.CTkLabel(self.trenutni_window, text="Trajanje:", font=("Inter",15 * -1),anchor='nw')
        lblTrajanje.place(x=46,y=169)
        self.izmeni_entryTrajanje = self.create_entry(self.trenutni_window,141,168,width=179,height=23,placeholder=slctd_trajanje,belo=True)
        
        
        
        lblOpis = ctk.CTkLabel(self.trenutni_window, text="Opis:", font=("Inter",15 * -1),anchor='nw')
        lblOpis.place(x=27,y=308)
        
        
        self.izmeni_txtbxOpis = ctk.CTkTextbox(self.trenutni_window,width=294,height=80,corner_radius=4,fg_color="#080A17")
        self.izmeni_txtbxOpis.place(x=26,y=334)
        self.izmeni_txtbxOpis.insert("0.0", slctd_opis)
        
        btnSacuvaj = ctk.CTkButton(self.trenutni_window, text="Izmeni", command=self.azuriraj_program)
        btnSacuvaj.place(x=102,y=424)
        self.imgOtkazi = PhotoImage(file="./src/img/Widget/btnOtkazi.png")
        btnObrisiFiltere = Button(self.trenutni_window,image=self.imgOtkazi, borderwidth=0, highlightthickness=0, relief="flat",command=self.trenutni_window.destroy) 
        btnObrisiFiltere.place(x=136,y=461,width=72,height=17)
        