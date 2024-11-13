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


class ProgramiWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None
        self.promenljive_filteri()

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        self.create_button("./src/img/Widget/btnExit.png",812,9,33,33,self.switch_back_to_main)# EXit dugme
        self.create_button("./src/img/Widget/btnSearch.png",358,53,33,33,self.search_programs) # Search dugme
        self.create_button("./src/img/Widget/btnFilteri.png",687,55,142,33,self.winProgramiFilteri) # Filteri Dugme
        self.create_button("./src/img/Widget/btnDodaj.png",23,543,252,40,lambda: helperFunctions.pisi_eror("Dodaj")) # Dodaj Dugme
        self.create_button("./src/img/Widget/btnIzmeni.png",300,543,252,40,lambda: helperFunctions.pisi_eror("IZmeni")) # Izmeni Dugme
        self.create_button("./src/img/Widget/btnObrisi.png",577,543,252,40,lambda: helperFunctions.pisi_eror("Obrisi")) # Obrisi Dugme
        
        self.imgsearchPozadiga = PhotoImage(file="./src/img/Widget/searchPozadina.png")
        self.current_canvas.create_image(23, 53, image=self.imgsearchPozadiga, anchor='nw')
        
        self.tabelaPozadina = PhotoImage(file="./src/img/Widget/tabelaPozadina.png")
        self.current_canvas.create_image(23, 102, image=self.tabelaPozadina, anchor='nw')
        
        self.create_entry_search()
        
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
        self.cmbbxSearch=self.create_comboBox(self.current_canvas,self.kriterijumi)
        self.cmbbxSearch.place(x=524,y=55)
        
        self.create_table()
        
    def create_comboBox(self,canvas,values):
        return ctk.CTkComboBox(canvas,width=148,height=33,corner_radius=5,border_width=0, values=values,fg_color="#080A17",dropdown_fg_color="#080A17",button_color="#0D1026")
        
    def create_entry_search(self):
        self.entrySearch = self.create_entry(canvas=self.current_canvas,x=28,y=59,placeholder="Pretraži",on_focus_in=self.on_entry_click,on_focus_out=self.on_focus_out)
        self.entrySearch.bind("<Return>", lambda event:self.search_programs())
        self.entrySearch.bind("<KeyRelease>", lambda event: self.search_programs())

        
    def create_button(self, image_path, x, y, width, height, command):
        image = PhotoImage(file=image_path)
        button = Button(self.current_canvas,
            image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat"
        )
        button.image = image  
        button.place(x=x, y=y, width=width, height=height)
        return button
    
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
        self.main_window.unisti_win_programi()

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
        kolone = ("šifra", "naziv", "vrsta treninga", "trajanje", "instruktor", "potreban paket", "opis")
        self.table = ttk.Treeview(self.current_canvas, columns=kolone, show="headings", height=18)

        for kolona in kolone:
            self.table.heading(kolona, text=kolona.capitalize())
            self.table.column(kolona, anchor="center", width=120)
            
        
        self.table.column("instruktor", width=50)
        self.table.column("trajanje", width=30)
        self.table.column("potreban paket", width=50)
        self.table.column("opis", width=50)
        self.table.column("šifra", width=25)

        self.popuni_tabelu()

        self.table.place(x=31, y=112, width=787, height=401)

    def popuni_tabelu(self):
        for red in self.table.get_children():
            self.table.delete(red)
                
        podaci=self.izlistaj_programe()
        
        for podatak in podaci:
            self.table.insert("", "end", values=podatak)

    def search_programs(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())

        if not kriterijum:
            helperFunctions.pisi_eror("Nije moguće pretražiti nepostijeći kriterijum.")
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

    def create_entry(self, canvas, x, y, placeholder='', on_focus_in=print("focus"), on_focus_out=print("focus out"), show='',width=303,height=20):
        entry = ctk.CTkEntry(
            canvas,border_width=0,fg_color="#080A17", text_color="#FFFFFF", show=show,width=width,height=height
        )
        entry.place(x=x, y=y,)
        entry.insert(0, placeholder)
        #entry.configure(fg_color="#080A17")
        entry.configure(text_color="gray")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry

    def winProgramiFilteri(self):
        self.filteri_window = ctk.CTkToplevel(fg_color='#000000')
        self.filteri_window.title("Filteri")
        self.filteri_window.geometry("343x382")
        self.filteri_window.resizable(False,False)
        helperFunctions.centerWindow(self.filteri_window)

        self.cmbbxSifre=self.napravi_filter_cmbbx("Šifra:",64,39,172,31,"SELECT id_programa FROM Program") #Kombo box za id
        self.cmbbxNaziv=self.napravi_filter_cmbbx("Naziv:",56,78,172,72,"SELECT DISTINCT naziv FROM Program") #Kombo box za naziv
        self.cmbbxVrsteTreninga=self.napravi_filter_cmbbx("Vrsta treninga:",26,121,172,115,"SELECT DISTINCT Vrste_treninga.naziv FROM Program JOIN Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga") #Kombo box za naziv
        self.cmbbxInstruktor=self.napravi_filter_cmbbx("Trener:",52,233,172,225,"SELECT DISTINCT Korisnici.ime FROM Program JOIN Korisnici ON Program.id_instruktora = Korisnici.username") #Kombo box za naziv
        
        naziv = self.naziv if self.naziv != "" else "SVE"
        self.cmbbxNaziv.set(naziv)
        sifra = self.id_programa if self.id_programa != "" else "SVE"
        self.cmbbxSifre.set(sifra)
        naziv_vrste_treninga = self.naziv_vrste_treninga if self.naziv_vrste_treninga != "" else "SVE"
        self.cmbbxVrsteTreninga.set(naziv_vrste_treninga)
        instruktor = self.instruktor if self.instruktor != "" else "SVE"
        self.cmbbxInstruktor.set(instruktor)
        
        lblPaket = ctk.CTkLabel(self.filteri_window, text="Potreban Premium Paket:", font=("Inter",15 * -1),anchor='nw')
        lblPaket.place(x=27,y=280)
        self.switchPaket=ctk.CTkSwitch(self.filteri_window,width=43,height=24,text='')
        self.switchPaket.place(x=252,y=278)
        
        
        queries.cursor.execute("SELECT MIN(trajanje), MAX(trajanje) FROM Program")
        rez=queries.cursor.fetchall()[0]
        min=rez[0]
        max=rez[1]
        lblTrajanje = ctk.CTkLabel(self.filteri_window, text="Trajanje od do:", font=("Inter",15 * -1),anchor='nw')
        lblTrajanje.place(x=124,y=167)
        self.slajder=CTkRangeSlider(self.filteri_window,height=16,width=288,from_=min, to=max,command=self.update_trajanje)
        self.slajder.place(x=32,y=191)
        self.slajder.set([self.trajanjeOd,self.trajanjeDo])
        
        
        self.entryTrajanjeOd=self.create_entry(canvas=self.filteri_window,x=32,y=166,width=59,height=18,on_focus_in=self.on_entry_trajanjeOd_click,on_focus_out=self.on_focus_out_trajanjeOd)
        self.entryTrajanjeDo=self.create_entry(canvas=self.filteri_window,x=261,y=166,width=59,height=18)
        self.update_trajanje()
        
        if (self.potrebanPaket): self.switchPaket.select() 
        else: self.switchPaket.deselect()
        
        btnSacuvaj = ctk.CTkButton(self.filteri_window, text="Sačuvaj", command=self.ugasi_filteri)
        btnSacuvaj.place(x=102,y=323)
        self.imgObrisiFiltere = PhotoImage(file="./src/img/Widget/btnObrisiFiltere.png")
        btnObrisiFiltere = Button(self.filteri_window,image=self.imgObrisiFiltere, borderwidth=0, highlightthickness=0, relief="flat")
        self.slajder.configure(command=lambda value: self.update_trajanje())
        btnObrisiFiltere.place(x=135,y=357,width=72,height=17)
        
    def on_entry_trajanjeOd_click(self,event):
        self.entryTrajanjeDo.configure(text_color="white")

    def on_focus_out_trajanjeOd(self,event):
        if self.entrySearch.get() == "":
            self.entrySearch.insert(0, self.trajanjeOd)
        self.entrySearch.configure(text_color="gray")

    def apdejtujSlajder():
        self.update_trajanje()
            
    def update_trajanje(self):
        self.trajanjeOd, self.trajanjeDo = self.slajder.get()
        
        self.entryTrajanjeOd.delete(0, ctk.END)
        self.entryTrajanjeOd.insert(0, int(self.trajanjeOd))
        
        self.entryTrajanjeDo.delete(0, ctk.END)
        self.entryTrajanjeDo.insert(0, int(self.trajanjeDo))
        
    def napravi_filter_cmbbx(self,text,labelX,labelY,comboX,comboY,query):
        lblSifra = ctk.CTkLabel(self.filteri_window, text=text, font=("Inter",15 * -1),anchor='nw')
        lblSifra.place(x=labelX,y=labelY)
        queries.cursor.execute(query)
        listaSifre=queries.cursor.fetchall()
        lista=["SVE"]
        for sifra in listaSifre:
            lista.append(str(sifra[0]))
        cmbbx=self.create_comboBox(self.filteri_window, values=lista)
        cmbbx.place(x=comboX,y=comboY) 
        return cmbbx
    
    def restartuj_filtere(self):
        self.promenljive_filteri()
        self.filteri_window.destroy()
        self.filteri_window = None

    def izlistaj_programe(self,kriterijum='id_programa',pretraga=""):
        komanda=''' SELECT 
                        Program.id_programa,
                        Program.naziv AS naziv_programa,
                        Vrste_treninga.naziv AS naziv_vrste_treninga,
                        Program.trajanje || ' min' AS trajanje,
                        Korisnici.ime AS instruktor_ime,
                        CASE 
                            WHEN Program.potreban_paket = 0 THEN 'Standard'
                            WHEN Program.potreban_paket = 1 THEN 'Premium'
                        END AS potreban_paket,
                        Program.opis
                    FROM 
                        Program
                    JOIN 
                        Vrste_treninga ON Program.id_vrste_treninga = Vrste_treninga.id_vrste_treninga
                    JOIN 
                        Korisnici ON Program.id_instruktora = Korisnici.username'''
       
        komanda += f''' WHERE {kriterijum} LIKE ? 
                        AND id_programa LIKE ? 
                        AND naziv_programa LIKE ? 
                        AND naziv_vrste_treninga LIKE ?
                        AND trajanje >= ?
                        AND trajanje <= ?
                        AND instruktor_ime LIKE ?'''
        if(self.potrebanPaket==0):
            komanda += "AND potreban_paket = 0"
        queries.cursor.execute(komanda, ('%' + str(pretraga) + '%','%' + str(self.id_programa) + '%','%' + str(self.naziv) + '%','%' + str(self.naziv_vrste_treninga) + '%', self.trajanjeOd,self.trajanjeDo,'%' + str(self.instruktor) + '%',))
       
                                
        return queries.cursor.fetchall()
    
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
        
        vrste_treninga=self.cmbbxVrsteTreninga.get()
        self.naziv_vrste_treninga = "" if vrste_treninga == "SVE" else vrste_treninga
        
        instruktor=self.cmbbxInstruktor.get()
        self.instruktor = "" if instruktor == "SVE" else instruktor
    
        self.potrebanPaket=self.switchPaket.get()

        self.filteri_window.destroy()
        self.filteri_window = None
        self.popuni_tabelu()