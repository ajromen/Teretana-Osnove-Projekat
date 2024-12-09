from imports import *

class SignupWindow:
    def __init__(self,window):
        self.window = window
          
    def start(self,user=''):
        self.user=user
        self.guest=0
        if(len(user)>0): self.guest=1
        self.return_value = 0
        helperFunctions.setup_window(self.window,"Kreiraj nalog","760x450","#000000")
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value
 
    
    def create_canvas(self):
        self.canvas = Canvas(self.window, bg="#03050B", height=450, width=760, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        self.imgPozadina=wid.create_canvas_image(self.canvas,"src/img/Signup/image_1.png",0, 0)
        self.imgLogo=wid.create_canvas_image(self.canvas,"src/img/Logo/TopFormLogoBeliMali2.png",201-303//2, 76.0)

        self.text_id = self.canvas.create_text(39,172, anchor="nw", text="Dobrodošao/la, ", fill="#FFFFFF", font=("Inter SemiBold", 24 * -1))
        self.canvas.create_rectangle(41.0, 230, 352.0, 231, fill="#FFFFFF",outline="")
        self.canvas.create_rectangle(41.0, 274.0, 352, 275.0, fill="#FFFFFF", outline="")
        self.canvas.create_rectangle(41.0, 313.0, 352, 314, fill="#FFFFFF", outline="")
    
    def create_widgets(self):
        self.entryName = wid.create_entry(self.canvas,x=41.0, y=209.0,width=312,corner_radius=0,back_color="#1A1B20", placeholder="Ime i Prezime",manual_fin_fon=(True,"Polje"))
        self.entryName.bind("<KeyRelease>", lambda event: self.promeni_dobrodosao())

        self.entyUsername = wid.create_entry(self.canvas,x=41.0, y=253.0,width=312,corner_radius=0,back_color="#1A1B20", placeholder="Korisničko ime", manual_fin_fon=(True,"Polje"))
        
        if(self.guest):
            self.entyUsername.delete(0, END)
            self.entyUsername.insert(0,self.user)
            self.entyUsername.configure(text_color="white")

        self.entryPassword = wid.create_entry(self.canvas,x=41.0, y=293.0,width=312,corner_radius=0,back_color="#1A1B20", placeholder="Lozinka", manual_fin_fon=(True,"Lozinka"))
        self.entryPassword.bind("<Return>", lambda event: self.napraviNalog())

        wid.create_button(self.canvas,"src/img/Signup/button_3.png", x=121.0, y=337.0, width=160.0, height=35.0, command=self.napraviNalog)
        wid.create_button(self.canvas,"src/img/Signup/button_2.png", x=588.0, y=394.0, width=153.0, height=40.0, command=lambda: self.vrati("gost"))
        wid.create_button(self.canvas,"src/img/Signup/button_1.png", x=163.0, y=379.0, width=76.0, height=15.0, command=lambda: self.vrati("login"))
        wid.create_button(self.canvas,"src/img/Signup/button_3.png", x=0, y=0.0, width=160.0, height=35, command=lambda: self.izlistaj())
    

    def promeni_dobrodosao(self):
        self.canvas.itemconfig(self.text_id, text="Dobrodošao/la, "+str((self.entryName.get().split(' '))[0]))
        
    
    def vrati(self,text):
        self.return_value=text
        self.window.quit()
    
    def napraviNalog(self):
        username=self.entyUsername.get()
        imeIPrezime=self.entryName.get().split(" ")
        if(len(imeIPrezime)!=2):
            helperFunctions.obavestenje("Polje ime i prezime mora da ima samo 2 argumenta")
            return
        ime=imeIPrezime[0]
        prezime=imeIPrezime[1]
        lozinka=self.entryPassword.get()
        if(len(lozinka)<6):
            helperFunctions.obavestenje("Lozinka mora da sadrži više od 6 karaktera")
            return 0
        if(not re.search(r'\d', lozinka)):
            helperFunctions.obavestenje("Lozinka mora sadržati bar jednu cifru")
            return 0
        uloga=0
        status_clanstva=1
        uplacen_paket=0
        datum_registracije=datetime.date.today().strftime("%Y-%m-%d")
        obnova_clanarine=datum_registracije
        if(not self.guest):
            nalog=queries.napraviNalog(username, lozinka, ime, prezime, uloga,status_clanstva, uplacen_paket,datum_registracije,obnova_clanarine)
        else:
            nalog=queries.azurirajNalog(self.user, username, lozinka, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije,obnova_clanarine)
        self.vrati(nalog)

    def izlistaj(self):
        queries.cursor.execute("SELECT * FROM Rezervacija")
        print(queries.cursor.fetchall())