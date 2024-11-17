import datetime
import sys
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import sqlite3
import os
import ctypes
import queries
import helperFunctions
from ctk_rangeslider import *
import widgets as wid


class TreningWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        wid.create_button(self.current_canvas,"./src/img/Widget/btnExit.png",812,9,33,33,self.switch_back_to_main)# EXit dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnSearch.png",358,53,33,33,self.pretrazi) # Search dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnDodaj.png",23,543,252,40,lambda: self.winTrening_Dodaj()) # Dodaj Dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnIzmeni.png",300,543,252,40,lambda: self.winTrening_Izmeni()) # Izmeni Dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnObrisi.png",577,543,252,40,self.obrisi_trening) # Obrisi Dugme
        
        self.imgsearchPozadiga = PhotoImage(file="./src/img/Widget/searchPozadina.png")
        self.current_canvas.create_image(23, 53, image=self.imgsearchPozadiga, anchor='nw')
        
        self.tabelaPozadina = PhotoImage(file="./src/img/Widget/tabelaPozadina.png")
        self.current_canvas.create_image(23, 102, image=self.tabelaPozadina, anchor='nw')
        
        self.kriterijumiMap={
            "Šifra" : "id_treninga",
            "Sala" : "naziv_sale",
            "Vreme početka" : "vreme_pocetka",
            "Vreme kraja" : "vreme_kraja",
            "Dani nedelje" : "dani",
            "Program" : "naziv_programa"
        }
        self.kriterijumi=["Šifra", "Sala", "Vreme početka", "Vreme kraja", "Dani nedelje", "Program"]
        self.create_entry_search(self.current_canvas,self.kriterijumi,self.pretrazi,self.on_entry_click,self.on_focus_out)
        
        self.current_canvas.create_text(450,65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch=wid.create_comboBox(self.current_canvas,self.kriterijumi,x=524,y=55)
        
        self.create_table()
    
    def on_entry_click(self,event):
        if self.entrySearch.get() == "Pretraži":
            self.entrySearch.delete(0, END)
            self.entrySearch.configure(text_color="white")

    def on_focus_out(self,event):
        if self.entrySearch.get() == "":
            self.entrySearch.insert(0, "Pretraži")
            self.entrySearch.configure(text_color="gray")
    
    def switch_back_to_main(self):
        if self.current_canvas:
            self.current_canvas.destroy()
        self.main_window.unisti_trenutni_win()

    def create_table(self):
        style = ttk.Style()
    
        style.theme_use("default")
    
        style.configure("Treeview",
                            background="#121633",
                            foreground="white",
                            rowheight=25,
                            fieldbackground="#080A17",
                            bordercolor="#343638",
                            borderwidth=0)
        style.map('Treeview', background=[('selected', '#3e4cb3')])
    
        style.configure("Treeview.Heading",
                            background="#2d3680",
                            foreground="white",
                            relief="flat")
        style.map("Treeview.Heading",
                      background=[('active', '#3484F0')])
        kolone = ("Šifra", "Sala", "Vreme početka", "Vreme kraja", "Dani nedelje", "Program")
        self.table = ttk.Treeview(self.current_canvas, columns=kolone, show="headings", height=18)

        for kolona in kolone:
            self.table.heading(kolona, text=kolona.capitalize())
            self.table.column(kolona, anchor="center", width=120)

        self.popuni_tabelu()

        self.table.place(x=31, y=112, width=787, height=401)

    def popuni_tabelu(self):
        for red in self.table.get_children():
            self.table.delete(red)
                
        podaci=self.izlistaj()
        
        for podatak in podaci:
            podatak=list(podatak)
            sifra_sale=podatak[6]
            sifra_programa=podatak[7]
            podatak[1]=str(sifra_sale)+" "+podatak[1]
            podatak[5]=str(sifra_programa)+" "+podatak[5]
            self.table.insert("", "end", values=podatak)

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

        podaci=self.izlistaj(pretraga=pretraga,kriterijum=kriterijum)
        
        for podatak in podaci:
            podatak=list(podatak)
            sifra_sale=podatak[6]
            sifra_programa=podatak[7]
            podatak[1]=str(sifra_sale)+" "+podatak[1]
            podatak[5]=str(sifra_programa)+" "+podatak[5]
            self.table.insert("", "end", values=podatak)


    

    def izlistaj(self,kriterijum='id_treninga',pretraga=""):              
        return queries.izlistaj_trening(pretraga,kriterijum)
    
    def obrisi_trening(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan trening za brisanje.")
            return

        pitaj = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabrani trening?")
        if not pitaj:
            return

        slctd_data = self.table.item(slctd_item)
        trening_id = slctd_data["values"][0]  

        try:
            komanda = "DELETE FROM Trening WHERE id_treninga = ?"
            queries.cursor.execute(komanda, (trening_id,))
            queries.connection.commit()

            self.table.delete(slctd_item)
            helperFunctions.obavestenje(title="Brisanje", poruka="Trening je uspešno obrisan.")

        except Exception as e:
            helperFunctions.obavestenje(title="Greška", poruka=f"Došlo je do greške prilikom brisanja trenigna: {e}")
            
    
    def selektuj_pravi(self,komboBox,kriterijum):
        vrednosti=komboBox.cget('values')
        for vrednost in vrednosti:
            if kriterijum.strip() == vrednost.strip():
                komboBox.set(vrednost)
                
    def winTrening_Izmeni(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan trening za izmenu.")
            return
        
        self.napravi_dodaj_izmeni_prozor()
        
        slctd_data = self.table.item(slctd_item)
        slctd_id = slctd_data["values"][0]
        slctd_sala=slctd_data["values"][1]
        slctd_vreme_pocetka=slctd_data["values"][2]
        slctd_vreme_kraja=slctd_data["values"][3]
        slctd_dani=slctd_data["values"][4]
        slctd_program=slctd_data["values"][5]
        # sifra
        self.entrySifra = wid.create_entry(self.trenutni_window,141,30,width=179,height=23,belo=True,placeholder=slctd_id,state="disabled")
        
        self.cmbbxSala=wid.napravi_sql_cmbbx(self.trenutni_window,"Sale:",59,75,170,69,"SELECT id_sale, naziv FROM Sala",2,True) #Kombo box za naziv
        self.cmbbxProgram=wid.napravi_sql_cmbbx(self.trenutni_window,"Program:",44,207,170,199,"SELECT id_programa,naziv FROM Program",2,True) #Kombo box za naziv
        self.selektuj_pravi(self.cmbbxSala,slctd_sala)
        self.selektuj_pravi(self.cmbbxProgram,slctd_program)
        
        self.zajednicke_Dodaj_Izmeni(slctd_vreme_pocetka,slctd_vreme_kraja,mode=1)

    def winTrening_Dodaj(self):
        self.napravi_dodaj_izmeni_prozor()
        
        self.cmbbxSala=wid.napravi_sql_cmbbx(self.trenutni_window,"Sale:",59,75,170,69,"SELECT id_sale, naziv FROM Sala",2,True) #Kombo box za naziv
        self.cmbbxProgram=wid.napravi_sql_cmbbx(self.trenutni_window,"Program:",44,207,170,199,"SELECT id_programa,naziv FROM Program",2,True) #Kombo box za naziv
        
        self.entrySifra = wid.create_entry(self.trenutni_window,141,30,width=179,height=23,belo=True)
        
        self.zajednicke_Dodaj_Izmeni(mode=0)
        
    def zajednicke_Dodaj_Izmeni(self,vreme_pocetka="00:00",vreme_kraja="00:00",mode=0,dani=""): # 0 za dodaj 1 za izmeni
        #ulaz za sifru
        lblSifra = ctk.CTkLabel(self.trenutni_window, text="Šifra:", font=("Inter",15 * -1),anchor='nw')
        lblSifra.place(x=58,y=31)
        
        #labele za vreme
        lblTrajanje = ctk.CTkLabel(self.trenutni_window, text="Vreme početka:", font=("Inter",15 * -1),anchor='nw')
        lblTrajanje.place(x=20,y=122)
        lblSatiPocetak = ctk.CTkLabel(self.trenutni_window, text="h   :", font=("Inter",15 * -1),anchor='nw')
        lblSatiPocetak.place(x=204,y=121)
        lblMinutaPocetak = ctk.CTkLabel(self.trenutni_window, text="min", font=("Inter",15 * -1),anchor='nw')
        lblMinutaPocetak.place(x=288,y=121)
        
        lblTrajanje = ctk.CTkLabel(self.trenutni_window, text="Vreme kraja:", font=("Inter",15 * -1),anchor='nw')
        lblTrajanje.place(x=33,y=162)
        lblSatiPocetak = ctk.CTkLabel(self.trenutni_window, text="h   :", font=("Inter",15 * -1),anchor='nw')
        lblSatiPocetak.place(x=204,y=161)
        lblMinutaPocetak = ctk.CTkLabel(self.trenutni_window, text="min", font=("Inter",15 * -1),anchor='nw')
        lblMinutaPocetak.place(x=288,y=161)
        
        lblMinutaPocetak = ctk.CTkLabel(self.trenutni_window, text="Dani:", font=("Inter",15 * -1),anchor='nw')
        lblMinutaPocetak.place(x=23,y=243)
        
        vreme_pocetka=(vreme_pocetka.strip()).split(":")
        pocetak_sati=vreme_pocetka[0]
        pocetak_minuti=vreme_pocetka[1]
        
        vreme_kraja=(vreme_kraja.strip()).split(":")
        kraj_sati=vreme_kraja[0]
        kraj_minuti=vreme_kraja[1]
        
        self.entryPocetakSati = wid.create_entry(self.trenutni_window,156,119,width=42,height=23,belo=True,placeholder=pocetak_sati)
        self.entryPocetakMinuti = wid.create_entry(self.trenutni_window,241,119,width=42,height=23,belo=True,placeholder=pocetak_minuti)
        self.entryKrajSati = wid.create_entry(self.trenutni_window,156,160,width=42,height=23,belo=True,placeholder=kraj_sati)
        self.entryKrajMinuti = wid.create_entry(self.trenutni_window,242,160,width=42,height=23,belo=True,placeholder=kraj_minuti)
        
        self.switch_dani(dani)

        
        #Kreiranje dugmadi za dane
        self.btnPon=self.button_dani("Pon",self.trenutni_window,16,272)
        self.btnUto=self.button_dani("Uto",self.trenutni_window,61,272)
        self.btnSre=self.button_dani("Sre",self.trenutni_window,106,272)
        self.btnCet=self.button_dani("Čet",self.trenutni_window,151,272)
        self.btnPet=self.button_dani("Pet",self.trenutni_window,196,272)
        self.btnSub=self.button_dani("Sub",self.trenutni_window,241,272)
        self.btnNed=self.button_dani("Ned",self.trenutni_window,286,272)
        
        
        btnSacuvaj = ctk.CTkButton(self.trenutni_window, text="Sačuvaj", command=lambda: self.dodaj_izmeni(mode=mode))
        btnSacuvaj.place(x=102,y=325)
        #dugme za otkazivanje
        self.imgOtkazi = PhotoImage(file="./src/img/Widget/btnOtkazi.png")
        btnOtkazi = Button(self.trenutni_window,image=self.imgOtkazi, borderwidth=0, highlightthickness=0, relief="flat",command=self.trenutni_window.destroy) 
        btnOtkazi.place(x=136,y=362,width=72,height=17)
        
        
    def dodaj_izmeni(self,mode=0):
        if(mode==1): 
            if(not helperFunctions.pitaj(title="Izmeni program",poruka="Da li ste sigurni da želite da izmenite program?")):return
        id=self.entrySifra.get()
        id_sale=self.cmbbxSala.get()
        #vreme
        vreme_pocetak_sat=self.entryPocetakSati.get()
        vreme_pocetak_minuti=self.entryPocetakMinuti.get()
        vreme_kraj_sat=self.entryKrajSati.get()
        vreme_kraj_minuti=self.entryKrajMinuti.get()
        dani=self.switch_dani_toStr()
        
        id_programa=self.cmbbxProgram.get()
        
        if(id=="" or (not id.isdigit())):
            helperFunctions.obavestenje("Šifra ne sme biti prazna ili sadržati slova.")
            return
        if(len(id)!=4):
            helperFunctions.obavestenje("Šifra mora imati tačno 4 cifre.")
            return
        if(id_sale==""):
            helperFunctions.obavestenje("Polje sala ne sme biti prazano.")
            return
        if(id_programa==""):
            helperFunctions.obavestenje("Polje program ne sme biti prazano.")
            return
        id_sale=id_sale.split(" ")[0]
        id_programa=id_programa.split(" ")[0]
        
        #provera unosa za vreme
        if(len(vreme_pocetak_sat)!=2 or (not vreme_pocetak_sat.isdigit())):
            helperFunctions.obavestenje("Polje vreme pocetka/sat mora sadržati tačno dve cifre.")
            return
        if(len(vreme_pocetak_minuti)!=2 or (not vreme_pocetak_minuti.isdigit())):
            helperFunctions.obavestenje("Polje vreme pocetka/minuti mora sadržati tačno dve cifre.")
            return
        if(len(vreme_kraj_sat)!=2 or (not vreme_kraj_sat.isdigit())):
            helperFunctions.obavestenje("Polje vreme kraja/sat mora sadržati tačno dve cifre.")
            return
        if(len(vreme_kraj_minuti)!=2 or (not vreme_kraj_minuti.isdigit())):
            helperFunctions.obavestenje("Polje vreme kraja/minuti mora sadržati tačno dve cifre.")
            return
        
        #proveravanje da li je uneti broj u opsegu
        if(int(vreme_pocetak_sat)>23):
            helperFunctions.obavestenje("Polje vreme početka/sat mora biti u opsegu od 0-24.")
            return
        if(int(vreme_pocetak_minuti)>59):
            helperFunctions.obavestenje("Polje vreme početka/minuti mora biti u opsegu od 0-60.")
            return
        if(int(vreme_kraj_sat)>23):
            helperFunctions.obavestenje("Polje vreme kraja/sat mora biti u opsegu od 0-24.")
            return
        if(int(vreme_kraj_minuti)>59):
            helperFunctions.obavestenje("Polje vreme kraja/minuti mora biti u opsegu od 0-60.")
            return
        vreme_pocetka=str(vreme_pocetak_sat)+":"+str(vreme_pocetak_minuti)
        vreme_kraja=str(vreme_kraj_sat)+":"+str(vreme_kraj_minuti)
        

        if(mode):
            if(queries.azuriraj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani, id_programa)): return
            helperFunctions.obavestenje(title="Izmena programa", poruka="Uspešno izmenjen program.")
        else:
            if(queries.dodaj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani, id_programa)): return
            helperFunctions.obavestenje(title="Dodaj program", poruka="Uspešno dodat program.")
        queries.connection.commit()
        self.popuni_tabelu()
        
        self.trenutni_window.destroy()
        self.trenutni_window=None
        
        
        self.entryNaziv=None
        self.entrySifra=None
        self.cmbbxInstruktor=None
        self.cmbbxVrsteTreninga=None
        
    def napravi_dodaj_izmeni_prozor(self):
        self.trenutni_window = ctk.CTkToplevel(fg_color='#000000')
        self.trenutni_window.title("Trening")
        self.trenutni_window.geometry("343x390")
        self.trenutni_window.resizable(False,False)
        helperFunctions.centerWindow(self.trenutni_window) # Pravi se novi prozor za dodaj/izmeni
        
    def button_dani(self,dan,window,x,y):
        aktiviran=self.dani_dict[dan]
        button = ctk.CTkButton(window, text=dan, corner_radius=5,font=("Inter",12), width=41, height=26)
        if aktiviran: button.configure(fg_color="#1F6AA5")
        else: button.configure(fg_color="#080A17")
        button.place(x=x, y=y)
        button.configure(command=lambda: self.switch_dugme(dan, button))
        return button
    
    def switch_dani(self,dani_str):
        self.dani_dict = {
            "Pon": False,
            "Uto": False,
            "Sre": False,
            "Čet": False,
            "Pet": False,
            "Sub": False,
            "Ned": False,
        }
        if(dani_str==""): return
        dani_list=dani_str.split(",")
        for dan in dani_list:
            self.dani_dict[dan]=True
            
    def switch_dani_toStr(self):
        string=""
        for dan in self.dani_dict.items():
            if(dan[1]):string+=dan[0]+","
        string = string[:-1] if string.endswith(",") else string
        return string
        
    def switch_dugme(self,dan,dugme):
        self.dani_dict[dan] = not self.dani_dict[dan]
        if dugme.cget("fg_color")=="#1F6AA5":
            dugme.configure(fg_color="#080A17")
        else:
            dugme.configure(fg_color="#1F6AA5")