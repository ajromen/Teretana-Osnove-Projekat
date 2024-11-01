import tkinter as tk
from customtkinter import *
# import PyQt6.QtWidgets as QtWidgets
import sys


import queries
import helperFunctions

queries.executeScriptsFromFile("src/sql/Teretana.sql")
queries.executeScriptsFromFile("src/sql/TeretanaUnosPodataka.sql")

set_appearance_mode('Dark')

win=CTk()
win.title("TopForm")
win.geometry('700x450+0+0')
lblAloBre=CTkLabel(master=win,text="textOvaj",font=("Calibri", 16))
lblAloBre.pack()

win.mainloop()