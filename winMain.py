from tkinter import *
import customtkinter as ctk

window = ctk.CTk()
window.title("ACINNAZIV")
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
image_image_1 = PhotoImage(
    file="src/img/Main/image_1.png")
image_1 = canvas.create_image(
    655.0,
    304.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file="src/img/Main/button_1.png")
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=0.0,
    y=501.0,
    width=230.0,
    height=63.0
)

button_image_2 = PhotoImage(
    file="src/img/Main/button_2.png")
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=0.0,
    y=439.0,
    width=230.0,
    height=63.0
)

button_image_3 = PhotoImage(
    file="src/img/Main/button_3.png")
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=0.0,
    y=375.0,
    width=230.0,
    height=63.0
)

button_image_4 = PhotoImage(
    file="src/img/Main/button_4.png")
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=0.0,
    y=313.0,
    width=230.0,
    height=63.0
)

button_image_5 = PhotoImage(
    file="src/img/Main/button_5.png")
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=0.0,
    y=250.0,
    width=230.0,
    height=63.0
)

button_image_6 = PhotoImage(
    file="src/img/Main/button_6.png")
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=0.0,
    y=187.0,
    width=230.0,
    height=63.0
)

button_image_7 = PhotoImage(
    file="src/img/Main/button_7.png")
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=0.0,
    y=125.0,
    width=230.0,
    height=63.0
)

button_image_8 = PhotoImage(
    file="src/img/Main/button_8.png")
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=0.0,
    y=63.0,
    width=230.0,
    height=63.0
)

image_image_2 = PhotoImage(
    file="src/img/Main/image_2.png")
image_2 = canvas.create_image(
    115.0,
    31.0,
    image=image_image_2
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
    file="src/img/Main/button_9.png")
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(
    x=35.0,
    y=559.0,
    width=160.0,
    height=35.0
)

button_image_10 = PhotoImage(
    file="src/img/Main/button_10.png")
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=35.0,
    y=559.0,
    width=160.0,
    height=35.0
)
window.resizable(False, False)
window.mainloop()
