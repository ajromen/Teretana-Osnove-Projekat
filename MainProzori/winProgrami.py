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


class ProgramiWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None

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
        self.cmbbxSearch=ctk.CTkComboBox(self.current_canvas,width=148,height=33,corner_radius=5,border_width=0, values=self.kriterijumi,fg_color="#080A17",dropdown_fg_color="#080A17",button_color="#080A17")
        self.cmbbxSearch.place(x=524,y=55)
        
        self.create_table()
        
    def create_entry_search(self):
        self.search_var = StringVar()
        self.entrySearch = ctk.CTkEntry(self.current_canvas, width=303.0, height=20.0, corner_radius=0, fg_color="#080A17",textvariable=self.search_var,font=("Inter", 12),border_width=0)
        self.entrySearch.insert(0, "Pretraži")
        self.entrySearch.bind("<FocusIn>", self.on_entry_click)
        self.entrySearch.bind("<FocusOut>", self.on_focus_out)
        self.entrySearch.configure(fg_color="#080A17")
        self.entrySearch.place(x=28, y=59)
        self.entrySearch.bind("<Return>", self.search_programs)

        
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
        columns = ("šifra", "naziv", "vrsta treninga", "trajanje", "instruktor", "potreban paket", "opis")
        self.table = ttk.Treeview(self.current_canvas, columns=columns, show="headings", height=18)

        for col in columns:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, anchor="center", width=120)
            
        
        self.table.column("instruktor", width=50)
        self.table.column("trajanje", width=30)
        self.table.column("potreban paket", width=50)
        self.table.column("opis", width=50)
        self.table.column("šifra", width=25)

        self.popuni_tabelu()

        self.table.place(x=31, y=112, width=787, height=401)

    def popuni_tabelu(self):
        for row in self.table.get_children():
            self.table.delete(row)
                
        
        queries.cursor.execute('''SELECT 
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
                                    Korisnici ON Program.id_instruktora = Korisnici.username;''')
        rows = queries.cursor.fetchall()
        for row in rows:
            self.table.insert("", "end", values=row)

    def search_programs(self,event=None):
        search_term = self.search_var.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())

        if not kriterijum:
            helperFunctions.pisi_eror("Nije moguće pretražiti nepostijeći kriterijum.")
            return

        for row in self.table.get_children():
            self.table.delete(row)
            
        if search_term =="" or search_term=="Pretraži":
            search_term=""
        else:
            if search_term in "premium":
                search_term = 1
            elif search_term in "standard":
                search_term = 0  
            else:
                pass


        # Corrected SQL query with fully qualified column names
        query = '''SELECT 
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
                        Korisnici ON Program.id_instruktora = Korisnici.username
                    WHERE 
                        {} LIKE ?'''.format(kriterijum)  # Insert the column for searching

        # Execute the query with the parameterized search term
        queries.cursor.execute(query, ('%' + str(search_term) + '%',))
        rows = queries.cursor.fetchall()

        # Insert fetched rows into the table
        for row in rows:
            self.table.insert("", "end", values=row)



    def create_entry(self, x, y, placeholder, on_focus_in, on_focus_out, show=''):
        entry = Entry(
            self.current_canvas, bd=0, bg="#1A1B20", fg="#FFFFFF", highlightthickness=0, show=show
        )
        entry.place(x=x, y=y, width=303.0, height=20.0)
        entry.insert(0, placeholder)
        entry.configure(foreground="gray")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry

    def winProgramiFilteri(self):
        self.filteri_window = ctk.CTkToplevel()
        self.filteri_window.title("Filteri")

        self.filteri_window.update_idletasks()
        screen_width = self.filteri_window.winfo_screenwidth()
        screen_height = self.filteri_window.winfo_screenheight()
        window_width = 343
        window_height = 346
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.filteri_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.filteri_window.focus()
        self.filteri_window.grab_set()

        lblSifra = ctk.CTkLabel(self.filteri_window, text="Šifra", fg_color="red")
        lblSifra.place(x=64,y=39)

        close_button = ctk.CTkButton(self.filteri_window, text="Zatvori", command=self.filteri_window.destroy)
        close_button.pack(pady=10)