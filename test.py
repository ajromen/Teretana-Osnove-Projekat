import tkinter as tk
from tkinter import ttk
import sqlite3

connection=sqlite3.connect("baza.db")
cursor=connection.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS
               teretana(id INTEGER PRIMARY_KEY,
               imeTeretane TEXT)
               """)

cursor.execute("""
               INSERT INTO teretana(id,imeTeretane) 
                    VALUES(0,'TopForm'),
                          (1,'ClassicGym'),
                          (2,'Colosseum')
               """)

cursor.execute("SELECT * FROM teretana")


txtTekst=cursor.fetchall()
print(txtTekst[0][1])
win=tk.Tk()
win.title("TopForm")
win.geometry('700x450+0+0')

#title
lblTitle= ttk.Label(master=win, text="TOPFORM",font="Calibri 24 bold")
lblTitle.pack()
#input
frmInput=ttk.Frame(master=win)

txtbxUsername=ttk.Entry(master=frmInput)
btnSubmit=ttk.Button(master=frmInput, text='Tea')
txtbxUsername.pack()
btnSubmit.pack()
frmInput.pack()

lblAloBre=ttk.Label(master=win,text=txtTekst,font="Calibri 24 bold")
lblAloBre.pack()

win.mainloop()