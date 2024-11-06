from tkinter import *
import customtkinter as ctk
import queries
import helperFunctions

class LoginWindow:
    def __init__(self, window):
        self.window = window
        self.return_value = 0
        self.setup_window()
        self.create_canvas()
        self.create_widgets()

    def setup_window(self):
        self.window.title("Uloguj se")
        self.window.geometry("760x450")
        self.window.configure(bg="#03050B")
        self.window.resizable(False, False)

    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#03050B",
            height=450,
            width=760,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load images and create image elements
        self.image_image_1 = PhotoImage(file="src/img/login/image_1.png")
        self.canvas.create_image(386.0, 226.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file="src/img/TopFormLogoBeliMali2.png")
        self.canvas.create_image(565.0, 74.0, image=self.image_image_2)

        self.text_id = self.canvas.create_text(
            388.0, 171.0, anchor="nw", text="Pozdrav,", fill="#FFFFFF", font=("Inter", 24 * -1)
        )

        self.canvas.create_rectangle(403, 247.7, 706, 248.0, fill="#FFFFFF", outline="")
        self.canvas.create_rectangle(403, 302.7, 706, 303.0, fill="#FFFFFF", outline="")

    def create_widgets(self):
        # Username Entry
        self.entryUsername = self.create_entry(403, 225, "Korisničko ime", self.on_entry_click_username, self.on_focus_out_username)
        self.entryUsername.bind("<KeyRelease>", self.update_greeting)
        
        # Password Entry
        self.entryPassword = self.create_entry(403, 281, "Lozinka", self.on_entry_click_password, self.on_focus_out_password, show='•')
        self.entryPassword.bind("<Return>", self.prijavi_se)

        # Login Button
        self.login_image = PhotoImage(file="src/img/login/button_1.png")
        self.btnLogin = Button(
            image=self.login_image, borderwidth=0, highlightthickness=0, 
            command=self.prijavi_se, relief="flat"
        )
        self.btnLogin.place(x=475.0, y=351.0, width=160.0, height=35.0)

        # Signup Button
        self.signup_image = PhotoImage(file="src/img/login/button_2.png")
        self.btnSignup = Button(
            image=self.signup_image, borderwidth=0, highlightthickness=0,
            command=lambda: self.vrati("signup"), relief="flat"
        )
        self.btnSignup.place(x=513.0, y=396.0, width=80.0, height=15.0)

        # Set custom tab order
        self.entryPassword.bind("<Tab>", self.set_custom_tab_order)
        self.entryUsername.bind("<Tab>", self.set_custom_tab_order)

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

    def vrati(self, text):
        self.return_value = text
        self.window.quit()

    def prijavi_se(self, event=None):
        korIme = str(self.entryUsername.get())
        loz = helperFunctions.hashPassword(str(self.entryPassword.get()))
        queries.cursor.execute(
            f"SELECT username, uloga FROM Korisnici WHERE username='{korIme}' AND password='{loz}'"
        )
        ima = queries.cursor.fetchall()
        if len(ima) != 0:
            self.vrati(str(ima))
        else:
            helperFunctions.pisi_eror("Pogrešno korisničko ime ili lozinka")

    def on_entry_click_username(self, event):
        if self.entryUsername.get() == "Korisničko ime":
            self.entryUsername.delete(0, END)
            self.entryUsername.configure(foreground="white")

    def on_focus_out_username(self, event):
        if self.entryUsername.get() == "":
            self.entryUsername.insert(0, "Korisničko ime")
            self.entryUsername.configure(foreground="gray")

    def on_entry_click_password(self, event):
        if self.entryPassword.get() == "Lozinka":
            self.entryPassword.delete(0, END)
            self.entryPassword.configure(foreground="white", show='•')

    def on_focus_out_password(self, event):
        if self.entryPassword.get() == "":
            self.entryPassword.insert(0, "Lozinka")
            self.entryPassword.configure(foreground="gray", show='')

    def update_greeting(self, event):
        self.canvas.itemconfig(self.text_id, text="Pozdrav, " + str(self.entryUsername.get()))

    def set_custom_tab_order(self, event):
        if event.widget == self.entryUsername:
            self.entryPassword.focus_set()
        elif event.widget == self.entryPassword:
            self.entryUsername.focus_set()
        else:
            self.entryUsername.focus_set()
        return "break"

    def start(self):
        self.window.mainloop()
        return self.return_value
