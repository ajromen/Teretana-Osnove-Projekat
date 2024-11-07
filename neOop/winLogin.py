from pathlib import Path

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
        korIme=str(entryUsername.get())
        loz=helperFunctions.hashPassword(str(entryPassword.get()))
        queries.cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+str(korIme)+"' AND password='"+str(loz)+"'")
        ima=queries.cursor.fetchall()
        if(len(ima)!=0):
            vrati(window,str(ima))
        else:
            helperFunctions.pisi_eror("Pogrešno korisničko ime ili lozinka")

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
   ######################################################
    
    entry_image_1 = PhotoImage(
        file=("src/img/login/entry_1.png"))
    entry_bg_1 = canvas.create_image(
        555.5,
        292.0,
        image=entry_image_1
    )
    entryPassword = Entry(
        bd=0,
        bg="#1A1B20",
        fg="#FFFFFF",
        highlightthickness=0
    )
    entryPassword.place(
        x=403.0,
        y=281.0,
        width=303.0,
        height=20.0
    )

    def on_entry_click(event):
        if entryPassword.get() == "Lozinka":
            entryPassword.delete(0, END)
            entryPassword.configure(foreground="white")
            entryPassword.configure(show='•')

    def on_focus_out(event):
        if entryPassword.get() == "":
            entryPassword.insert(0, "Lozinka")
            entryPassword.configure(foreground="gray",show='')

    entryPassword.configure(foreground="gray")
    entryPassword.insert(0, "Lozinka")
    entryPassword.bind("<FocusIn>", on_entry_click)
    entryPassword.bind("<FocusOut>", on_focus_out)
    entryPassword.bind("<Return>",prijavi_se)

    entry_image_2 = PhotoImage(
        file=("src/img/login/entry_2.png"))
    entry_bg_2 = canvas.create_image(
        554.5,
        236.0,
        image=entry_image_2
    )
    entryUsername = Entry(
        bd=0,
        bg="#1A1B20",
        fg="#FFFFFF",
        highlightthickness=0
    )
    entryUsername.place(
        x=403,
        y=225.0,
        width=303.0,
        height=20.0
    )

    def on_entry_click2(event):
        if entryUsername.get() == "Korisničko ime":
            entryUsername.delete(0, END)
            entryUsername.configure(foreground="white")

    def on_focus_out2(event):
        if entryUsername.get() == "":
            entryUsername.insert(0, "Korisničko ime")
            entryUsername.configure(foreground="gray")
        

    def funk(event):
        canvas.itemconfig(text_id, text="Pozdrav, "+str(entryUsername.get()))

    entryUsername.configure(foreground="gray")
    entryUsername.insert(0, "Korisničko ime")
    entryUsername.bind("<FocusIn>", on_entry_click2)
    entryUsername.bind("<FocusOut>", on_focus_out2)
    entryUsername.bind("<KeyRelease>", funk)

    
    

    login_image = PhotoImage(
        file=("src/img/login/button_1.png"))
    btnLogin = Button(
        image=login_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: prijavi_se(''),
        relief="flat"
    )
    btnLogin.place(
        x=475.0,
        y=351.0,
        width=160.0,
        height=35.0
    )
    

    signup_image = PhotoImage(
        file=("src/img/login/button_2.png"))
    btnSignup = Button(
        image=signup_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vrati(window,"signup"),
        relief="flat"
    )
    btnSignup.place(
        x=513.0,
        y=396.0,
        width=80.0,
        height=15.0
    )

    def set_custom_tab_order(event):
        if event.widget == entryUsername:
            entryPassword.focus_set()
        elif event.widget == entryPassword:
            entryUsername.focus_set()
        else:
            entryUsername.focus_set()
        return "break"

    entryPassword.bind("<Tab>", set_custom_tab_order)
    entryUsername.bind("<Tab>", set_custom_tab_order)

    window.resizable(False, False)
    window.mainloop()

    return return_value