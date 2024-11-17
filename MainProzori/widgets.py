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
    combo.place(x,y)

def create_entry_search(canvas,pretrazi,on_click,on_focus_out):
    entrySearch = create_entry(canvas=canvas,x=28,y=59,placeholder="Pretraži",on_focus_in=on_click,on_focus_out=on_focus_out,corner_radius=0)
    entrySearch.bind("<Return>", lambda event: pretrazi())
    entrySearch.bind("<KeyRelease>", lambda event: pretrazi())
    return entrySearch