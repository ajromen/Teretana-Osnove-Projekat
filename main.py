import tkinter as tk
from tkinter import ttk

import queries
import helperFunctions

queries.executeScriptsFromFile("Teretana.sql")
queries.executeScriptsFromFile("TeretanaUnosPodataka.sql")

win=tk.Tk()
win.title("TopForm")
win.geometry('700x450+0+0')
lblAloBre=ttk.Label(master=win,text="textOvaj",font="Calibri 16")
lblAloBre.pack()

win.mainloop()