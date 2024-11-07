from tkinter import *
import customtkinter as ctk

window = ctk.CTk()
window.title("TopForm")
window.geometry("1080x608")
window.configure(bg = "#04050C")


canvas = Canvas(
    window,
    bg = "#04050C",
    height = 608,
    width = 1080,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_imgPozadina = PhotoImage(
    file="src/img/Main/imgPozadina.png")
imgPozadina = canvas.create_image(
    655.0,
    304.0,
    image=image_imgPozadina
)

button_image_1 = PhotoImage(
    file="src/img/Main/btnVrsteTreninga.png")
btnVrsteTreninga = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnVrsteTreninga clicked"),
    relief="flat"
)
btnVrsteTreninga.place(
    x=0.0,
    y=501.0,
    width=230.0,
    height=63.0
)

button_image_2 = PhotoImage(
    file="src/img/Main/btnTreninzi.png")
btnTreninzi = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnTreninzi clicked"),
    relief="flat"
)
btnTreninzi.place(
    x=0.0,
    y=439.0,
    width=230.0,
    height=63.0
)

button_image_3 = PhotoImage(
    file="src/img/Main/btnIzvestaji.png")
btnIzvestaji = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnIzvestaji clicked"),
    relief="flat"
)
btnIzvestaji.place(
    x=0.0,
    y=375.0,
    width=230.0,
    height=63.0
)

button_image_4 = PhotoImage(
    file="src/img/Main/btnAdmin.png")
btnAdmin = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnAdmin clicked"),
    relief="flat"
)
btnAdmin.place(
    x=0.0,
    y=313.0,
    width=230.0,
    height=63.0
)

button_image_5 = PhotoImage(
    file="src/img/Main/btnClanovi.png")
btnClanovi = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnClanovi clicked"),
    relief="flat"
)
btnClanovi.place(
    x=0.0,
    y=250.0,
    width=230.0,
    height=63.0
)

button_image_6 = PhotoImage(
    file="src/img/Main/btnTermini.png")
btnTermini = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnTermini clicked"),
    relief="flat"
)
btnTermini.place(
    x=0.0,
    y=187.0,
    width=230.0,
    height=63.0
)

button_image_7 = PhotoImage(
    file="src/img/Main/btnRezervacije.png")
btnRezervacije = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnRezervacije clicked"),
    relief="flat"
)
btnRezervacije.place(
    x=0.0,
    y=125.0,
    width=230.0,
    height=63.0
)

button_image_8 = PhotoImage(
    file="src/img/Main/btnProgrami.png")
btnProgrami = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnProgrami clicked"),
    relief="flat"
)
btnProgrami.place(
    x=0.0,
    y=63.0,
    width=230.0,
    height=63.0
)

image_imgUser = PhotoImage(
    file="src/img/Main/imgUser.png")
imgUser = canvas.create_image(
    115.0,
    31.0,
    image=image_imgUser
)

canvas.create_text(
    64.0,
    25.0,
    anchor="nw",
    text="Username",
    fill="#FFFFFF",
    font=("Inter Medium", 12 * -1)
)

canvas.create_text(
    455.0,
    175.0,
    anchor="nw",
    text="19:49",
    fill="#DFDFDF",
    font=("DigitalNumbers Regular", 100 * -1)
)

canvas.create_text(
    540.0,
    313.0,
    anchor="nw",
    text="Saturday /  01.11.2024",
    fill="#DFDFDF",
    font=("Inter", 24 * -1)
)

canvas.create_rectangle(
    218.0,
    0.0,
    230.0,
    62.0,
    fill="#FFFFFF",
    outline="")

button_image_9 = PhotoImage(
    file="src/img/Main/btnRegistrujSe.png")
btnRegistrujSe = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnRegistrujSe clicked"),
    relief="flat"
)
btnRegistrujSe.place(
    x=35.0,
    y=559.0,
    width=160.0,
    height=35.0
)

button_image_10 = PhotoImage(
    file="src/img/Main/btnOdjaviSe.png")
btnOdjaviSe = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("btnOdjaviSe clicked"),
    relief="flat"
)
btnOdjaviSe.place(
    x=35.0,
    y=559.0,
    width=160.0,
    height=35.0
)

window.resizable(False, False)
window.mainloop()
