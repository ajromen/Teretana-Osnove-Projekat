import datetime
import sys
from tkinter import *
import customtkinter as ctk
import helperFunctions
import queries
import os
import ctypes
from CTkTable import *

class ProgramiWindow:
    def __init__(self, window):
        self.window = window
        self.current_canvas = None

    def start(self):
        if self.current_canvas:
            self.current_canvas.destroy()
        
        self.current_canvas=Canvas(self.window, bg="#04050C", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)

        self.imgBackground = PhotoImage(file="src/img/Main/imgPozadinaPrazna.png")
        self.current_canvas.create_image(655, 304, image=self.imgBackground)

        value = [[1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5]]

        table = CTkTable(master=self.window, row=5, column=5, values=value)
        
        table.pack(expand=False, fill="both", padx=20, pady=20)
        
        self.create_search_bar()

    def create_search_bar(self):
        self.search_var = StringVar()
        search_entry = Entry(self.current_canvas, textvariable=self.search_var, font=("Inter", 12), bg="#1A1B20", fg="#FFFFFF")
        search_entry.place(x=35, y=50, width=300, height=30)

        search_button = Button(self.current_canvas, text="Search", command=self.update_table)
        search_button.place(x=350, y=50, width=80, height=30)

        self.search_var.trace("w", lambda name, index, mode: self.update_table())

    def create_table(self):
        self.table_frame = Frame(self.current_canvas)
        self.table_frame.place(x=35, y=100)

        headers = ["Program", "Description", "Price"]
        for col, header in enumerate(headers):
            label = Label(self.table_frame, text=header, font=("Inter", 12, "bold"), bg="#04050C", fg="#FFFFFF", width=20)
            label.grid(row=0, column=col)

    def create_entry(self, x, y, placeholder, on_focus_in, on_focus_out, show=''):
        entry = Entry(
            bd=0, bg="#1A1B20", fg="#FFFFFF", highlightthickness=0, show=show
        )
        entry.place(x=x, y=y, width=303.0, height=20.0)
        entry.insert(0, placeholder)
        entry.configure(foreground="gray")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry