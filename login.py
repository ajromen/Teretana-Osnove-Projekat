
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import *
import customtkinter as ctk
import queries
import helperFunctions


def start(window):
    
    window.title("Uloguj se")


    window.geometry("760x450")
    window.configure(bg = "#03050B")

    global return_value
    return_value = 0
    
    canvas = Canvas(
        window,
        bg = "#03050B",
        height = 450,
        width = 760,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    def vrati(window,text):
        global return_value
        return_value=text
        window.quit()
    def prijavi_se(event):
        korIme=str(username.get())
        loz=helperFunctions.hashPassword(str(password.get()))
        queries.cursor.execute("SELECT uloga FROM Korisnici WHERE username=='{korIMe}' AND password=='{loz}'")
        ima=queries.cursor.fetchall()
        vrati(window,str(ima))

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=("src/img/login/image_1.png"))
    image_1 = canvas.create_image(
        386.0,
        226.0,
        image=image_image_1
    )

    text_id=canvas.create_text(
        388.0,
        171.0,
        anchor="nw",
        text="Pozdrav,",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    canvas.create_rectangle(
        403,
        247.69999998807907,
        706,
        248.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        403,
        302.69999998807907,
        706,
        303.0,
        fill="#FFFFFF",
        outline="")

    image_image_2 = PhotoImage(
        file=("src/img/TopFormLogoBeliMali2.png"))
    image_2 = canvas.create_image(
        565.0,
        74.0,
        image=image_image_2
    )

    
    entry_image_1 = PhotoImage(
        file=("src/img/login/entry_1.png"))
    entry_bg_1 = canvas.create_image(
        555.5,
        292.0,
        image=entry_image_1
    )
    password = Entry(
        bd=0,
        bg="#1A1B20",
        fg="#FFFFFF",
        highlightthickness=0
    )
    password.place(
        x=403.0,
        y=281.0,
        width=303.0,
        height=20.0
    )

    def on_entry_click(event):
        if password.get() == "Lozinka":
            password.delete(0, END)
            password.configure(foreground="white")
            password.configure(show='•')

    def on_focus_out(event):
        if password.get() == "":
            password.insert(0, "Lozinka")
            password.configure(foreground="gray",show='')

    password.configure(foreground="gray")
    password.insert(0, "Lozinka")
    password.bind("<FocusIn>", on_entry_click)
    password.bind("<FocusOut>", on_focus_out)
    password.bind("<Return>",prijavi_se)

    entry_image_2 = PhotoImage(
        file=("src/img/login/entry_2.png"))
    entry_bg_2 = canvas.create_image(
        554.5,
        236.0,
        image=entry_image_2
    )
    username = Entry(
        bd=0,
        bg="#1A1B20",
        fg="#FFFFFF",
        highlightthickness=0
    )
    username.place(
        x=403,
        y=225.0,
        width=303.0,
        height=20.0
    )

    def on_entry_click2(event):
        if username.get() == "Korisničko ime":
            username.delete(0, END)
            username.configure(foreground="white")

    def on_focus_out2(event):
        if username.get() == "":
            username.insert(0, "Korisničko ime")
            username.configure(foreground="gray")
        

    def funk(event):
        canvas.itemconfig(text_id, text="Pozdrav, "+str(username.get()))

    username.configure(foreground="gray")
    username.insert(0, "Korisničko ime")
    username.bind("<FocusIn>", on_entry_click2)
    username.bind("<FocusOut>", on_focus_out2)
    username.bind("<KeyRelease>", funk)

    
    

    button_image_1 = PhotoImage(
        file=("src/img/login/button_1.png"))
    login = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: prijavi_se,
        relief="flat"
    )
    login.place(
        x=475.0,
        y=351.0,
        width=160.0,
        height=35.0
    )
    

    button_image_2 = PhotoImage(
        file=("src/img/login/button_2.png"))
    signup = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vrati(window,"signup"),
        relief="flat"
    )
    signup.place(
        x=513.0,
        y=396.0,
        width=80.0,
        height=15.0
    )

    def set_custom_tab_order(event):
        if event.widget == username:
            password.focus_set()
        elif event.widget == password:
            username.focus_set()
        else:
            username.focus_set()
        return "break"

    password.bind("<Tab>", set_custom_tab_order)
    username.bind("<Tab>", set_custom_tab_order)

    window.resizable(False, False)
    window.mainloop()

    return return_value