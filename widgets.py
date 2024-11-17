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

def create_button(canvas,image_path, x, y, width, height, command):
    image = PhotoImage(file=image_path)
    button = Button(canvas, image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat")
    button.image = image  
    button.place(x=x, y=y, width=width, height=height)
    return button

def create_entry(canvas, x, y, on_focus_in=None, on_focus_out=None, placeholder='', show='',width=303,height=20,belo=False,state="normal",corner_radius=5):
    entry = ctk.CTkEntry(
        canvas,border_width=0,
        fg_color="#080A17",
        text_color="#FFFFFF",
        show=show,width=width,height=height,
        corner_radius=corner_radius
    )
    entry.place(x=x, y=y,)
    entry.delete(0,END)
    entry.insert(0, placeholder)
    not belo and entry.configure(text_color="gray")
    belo and entry.configure(text_color="white")
    entry.configure(state=state)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry

def napravi_sql_cmbbx(canvas,text,labelX,labelY,comboX,comboY,query,broj_kolona=1,specificni=False):
    lblSifra = ctk.CTkLabel(canvas, text=text, font=("Inter",15 * -1),anchor='nw')
    lblSifra.place(x=labelX,y=labelY)
    queries.cursor.execute(query)
    listaSifre=queries.cursor.fetchall()
    lista=[] if specificni else ["SVE"]
    for sifra in listaSifre:
        tekst=""
        for i in range(0,broj_kolona):
            tekst+=str(sifra[i])+" "
        lista.append(tekst)
    cmbbx=create_comboBox(canvas, values=lista,x=comboX,y=comboY)
    return cmbbx

def create_comboBox(canvas,values,x,y):
    combo= ctk.CTkComboBox(
        canvas,
        width=148,height=33,
        corner_radius=5,
        border_width=0,
        values=values,
        fg_color="#080A17",
        dropdown_fg_color="#080A17",
        button_color="#0D1026",
        state="readonly")
    combo.place(x=x,y=y)
    return combo

def create_entry_search(canvas,pretrazi,on_click,on_focus_out):
    entrySearch = create_entry(canvas=canvas,x=28,y=59,placeholder="Pretraži",on_focus_in=on_click,on_focus_out=on_focus_out,corner_radius=0)
    entrySearch.bind("<Return>", lambda event: pretrazi())
    entrySearch.bind("<KeyRelease>", lambda event: pretrazi())
    return entrySearch

def create_table(canvas,popuni_tabelu,kolone,x=31,y=112,width=787,height=401):
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
    
    style.configure("Treeview.Heading", background="#2d3680", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])
        
    table = ttk.Treeview(canvas, columns=kolone, show="headings", height=18)

    for kolona in kolone:
        table.heading(kolona, text=kolona.capitalize())
        table.column(kolona, anchor="center", width=80)

        popuni_tabelu(table)
    
    max_sirina = 200 
    
    for kolona in table["columns"]:
        max_sirina_kolone = len(table.heading(kolona, "text"))+2
        
        for item in table.get_children():
            deo_text = str(table.item(item, "values")[table["columns"].index(kolona)])
            finalna_sirina = max(max_sirina_kolone, len(deo_text))
        
        table.column(kolona, width=min(finalna_sirina * 8 , max_sirina))

    table.place(x=x, y=y, width=width, height=height)
    return table

def selektuj_vrednost_comboBox(komboBox,kriterijum):
    vrednosti=komboBox.cget('values')
    for vrednost in vrednosti:
        if kriterijum.strip() == vrednost.strip():
            komboBox.set(vrednost)
            
def create_label(window,text,x,y,font_size=15):
    labela = ctk.CTkLabel(window, text=text, font=("Inter",font_size * -1),anchor='nw')
    labela.place(x=x,y=y)
    return labela

"""self.table.column("instruktor", width=50)
        self.table.column("trajanje", width=30)
        self.table.column("potreban paket", width=50)
        self.table.column("opis", width=50)
        self.table.column("šifra", width=25)"""