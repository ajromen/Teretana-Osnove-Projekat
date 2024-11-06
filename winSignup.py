from pathlib import Path

from tkinter import *
import customtkinter as ctk
import queries
from datetime import date
import helperFunctions



def start(user=''):
    window=ctk.CTk()
    window.title('Kreiraj nalog')
    window.geometry("760x450")
    global return_value
    return_value = 0

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 450,
        width = 760,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(file=("src/img/Signup/image_1.png"))
    
    image_1 = canvas.create_image(
        380.0,
        225.0,
        image=image_image_1
    )
    
    def vrati(window,text):
        global return_value
        return_value=text
        window.quit()
        window.destroy()
    
    def napraviNalog():
        username=entyUsername.get()
        imeIPrezime=entryName.get().split(" ")
        if(len(imeIPrezime)!=2):
            helperFunctions.pisi_eror("Polje ime i prezime mora da ima samo 2 argumenta")
            return
        ime=imeIPrezime[0]
        prezime=imeIPrezime[1]
        lozinka=entryPassword.get()
        uloga=0
        status_clanstva=1
        uplacen_paket=0
        datum_registracije=date.today().strftime("%Y-%m-%d")
        if(queries.napraviNalog(username,lozinka,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije)=="vecPostoji"):
            helperFunctions.pisi_eror("Nalog sa korisničkim imenom već postoje")
            
    def on_name_click(event):
        if entryName.get() == "Ime i Prezime":
            entryName.delete(0, END)
            entryName.configure(foreground="white")

    def on_name_out(event):
        if entryName.get() == "":
            entryName.insert(0, "Ime i Prezime")
            entryName.configure(foreground="gray",show='')
            
    def change_welcome_text(event):
        canvas.itemconfig(text_id, text="Dobrodošao/la, "+str((entryName.get().split(' '))[0]))
        
    
    def on_username_click(event):
        if entyUsername.get() == "Korisničko ime":
            entyUsername.delete(0, END)
            entyUsername.configure(foreground="white")

    def on_username_out(event):
        if entyUsername.get() == "":
            entyUsername.insert(0, "Korisničko ime")
            entyUsername.configure(foreground="gray",show='')
            
    def on_password_click(event):
        if entryPassword.get() == "Lozinka":
            entryPassword.delete(0, END)
            entryPassword.configure(foreground="white")
            entryPassword.configure(show='•')

    def on_password_out(event):
        if entryPassword.get() == "":
            entryPassword.insert(0, "Lozinka")
            entryPassword.configure(foreground="gray",show='')
    

    name_image = PhotoImage(
        file=("src/img/Signup/entry_1.png"))
    name_bg = canvas.create_image(
        197.5,
        220.0,
        image=name_image
    )
    entryName = Entry(
        bd=0,
        bg="#131419",
        fg="#000716",
        highlightthickness=0
    )
    entryName.place(
        x=46.0,
        y=209.0,
        width=303.0,
        height=20.0
    )
    entryName.configure(foreground="gray")
    entryName.insert(0, "Ime i Prezime")
    entryName.bind("<FocusIn>", on_name_click)
    entryName.bind("<FocusOut>", on_name_out)
    entryName.bind("<KeyRelease>",change_welcome_text)

    username_image = PhotoImage(
        file=("src/img/Signup/entry_2.png"))
    username_bg = canvas.create_image(
        197.5,
        264.0,
        image=username_image
    )
    entyUsername = Entry(
        bd=0,
        bg="#131419",
        fg="#000716",
        #highlightthickness=0
    )
    entyUsername.place(
        x=46.0,
        y=253.0,
        width=303.0,
        height=20.0
    )
    entyUsername.configure(foreground="gray")
    entyUsername.insert(0, "Korisničko ime")
    entyUsername.bind("<FocusIn>", on_username_click)
    entyUsername.bind("<FocusOut>", on_username_out)
    

    password_image = PhotoImage(
        file=("src/img/Signup/entry_3.png"))
    password_bg = canvas.create_image(
        197.5,
        304.0,
        image=password_image
    )
    entryPassword = Entry(
        bd=0,
        bg="#131419",
        fg="#000716",
        highlightthickness=0
    )
    entryPassword.place(
        x=46.0,
        y=293.0,
        width=303.0,
        height=20.0
    )
    
    entryPassword.configure(foreground="gray")
    entryPassword.insert(0, "Lozinka")
    entryPassword.bind("<FocusIn>", on_password_click)
    entryPassword.bind("<FocusOut>", on_password_out)
    entryPassword.bind("<Return>", napraviNalog)

    

    
    
    login_image = PhotoImage(
        file=("src/img/Signup/button_1.png"))
    btnLogin = Button(
        image=login_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vrati(window,"login"),
        relief="flat"
    )
    btnLogin.place(
        x=163.0,
        y=379.0,
        width=76.0,
        height=15.0
    )

    canvas.create_rectangle(
        42.0,
        230.00000474521948,
        352.0,
        231.02317810058594,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        41.0,
        274.0,
        352.0000120401364,
        275.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        41.0,
        313.0,
        352.0000098859837,
        314.9935898159913,
        fill="#FFFFFF",
        outline="")

    text_id=canvas.create_text(
        39.0,
        172.0,
        anchor="nw",
        text="Dobrodošao/la, ",
        fill="#FFFFFF",
        font=("Inter SemiBold", 24 * -1)
    )

    def gostf():
        queries.cursor.execute("SELECT * FROM Korisnici")
        print(queries.cursor.fetchall())
    
    btnGost_image = PhotoImage(
        file=("src/img/Signup/button_2.png"))
    btnGost = Button(
        image=btnGost_image,
        borderwidth=0,
        highlightthickness=0,
        command=gostf,
        relief="flat"
    )
    btnGost.place(
        x=588.0,
        y=394.0,
        width=153.0,
        height=40.0
    )

    signup_image = PhotoImage(
        file=("src/img/Signup/button_3.png"))
    btnSignup = Button(
        image=signup_image,
        borderwidth=0,
        highlightthickness=0,
        command=napraviNalog,
        relief="flat"
    )
    btnSignup.place(
        x=121.0,
        y=337.0,
        width=160.0,
        height=35.0
    )

    image_image_2 = PhotoImage(file="src/img/TopFormLogoBeliMali2.png")
    image_2 = canvas.create_image(
        201.0,
        76.0,
        image=image_image_2
    )
    
    
    window.resizable(False, False)
    window.mainloop()
    
    return return_value
