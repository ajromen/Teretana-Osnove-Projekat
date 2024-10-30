import tkinter as tk
from tkinter import ttk

win=tk.Tk()
win.title("TopForm")
win.geometry('700x450+0+0')

#title
lblTitle= ttk.Label(master=win, text="TOPFORM",font="Calibri 24 bold")
lblTitle.pack()
#input
frmInput=ttk.Frame(master=win)

txtbxUsername=ttk.Entry(master=frmInput)
btnSubmit=ttk.Button(master=frmInput, text='Submit')
txtbxUsername.pack()
btnSubmit.pack()
frmInput.pack()

lblAloBre=ttk.Label(master=win,text="nista",font="Calibri 24 bold")
lblAloBre.pack()

win.mainloop()