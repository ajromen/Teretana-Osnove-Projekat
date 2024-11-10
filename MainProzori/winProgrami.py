import datetime
import sys
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import sqlite3
import os
import ctypes
import queries


class ProgramiWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#04050C", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)

        #self.imgBackground = PhotoImage(file="src/img/Main/imgPozadinaPrazna.png")
        #self.current_canvas.create_image(0, 0, anchor="nw", image=self.imgBackground)

        self.create_table()
        self.create_search_bar()
        self.create_back_button()

    def create_back_button(self):
        back_button = Button(self.current_canvas, text="Back", command=self.switch_back_to_main)
        back_button.place(x=35, y=50, width=80, height=30)
        
    def create_button(self, image_path, x, y, width, height, command):
        image = PhotoImage(file=image_path)
        button = Button(
            image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat"
        )
        button.image = image  
        button.place(x=x, y=y, width=width, height=height)
        return button
    
    def switch_back_to_main(self):
        if self.current_canvas:
            self.current_canvas.destroy()
        self.main_window.unisti_win_programi()

    def create_search_bar(self):
        self.search_var = StringVar()
        search_entry = Entry(self.current_canvas, textvariable=self.search_var, font=("Inter", 12), bg="#1A1B20", fg="#FFFFFF")
        search_entry.place(x=35, y=50, width=300, height=30)

        search_button = Button(self.current_canvas, text="Search", command=self.search_programs)
        search_button.place(x=350, y=50, width=80, height=30)

    def create_table(self):
        self.current_canvas.create_rectangle(35, 100, 825, 500, fill="#000000", outline="#04050C")

        columns = ("id_programa", "naziv", "id_vrste_treninga", "trajanje", "id_instruktora", "potreban_paket", "opis")
        self.table = ttk.Treeview(self.current_canvas, columns=columns, show="headings", height=18)

        for col in columns:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, anchor="center", width=120)

        self.populate_table()

        self.table.place(x=35, y=100, width=790, height=400)

    def populate_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        
        queries.cursor.execute("SELECT * FROM Program")
        rows = queries.cursor.fetchall()
        for row in rows:
            self.table.insert("", "end", values=row)

    def search_programs(self):
        search_term = self.search_var.get().strip().lower()
        for row in self.table.get_children():
            self.table.delete(row)

        queries.cursor.execute("SELECT * FROM Program WHERE id_programa LIKE ?", ('%' + search_term + '%',))
        rows = queries.cursor.fetchall()

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
