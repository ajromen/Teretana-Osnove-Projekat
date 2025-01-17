import bp_korisnici
from imports import *
import widgets as wid
import re

class SignupWindow:
    def __init__(self,window):
        self.window = window
          
    def start(self,user=''):
        self.user=user
        self.guest=0
        if(len(user)>0): self.guest=1
        self.return_value = 0
        helperFunctions.setup_window(self.window, "Kreiraj nalog", "760x450", boje.crna)
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value
 
    
    def create_canvas(self):
        self.canvas = Canvas(self.window, bg=boje.crna_main_window, height=450, width=760, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        self.imgPozadina=wid.create_canvas_image(self.canvas,"src/img/signup/image_1.png",0, 0)
        self.imgLogo=wid.create_canvas_image(self.canvas,"src/img/logo/TopFormLogoBeliMali2.png",201-303//2, 76.0)

        self.text_id = self.canvas.create_text(39, 172, anchor="nw", text="Dobrodošao/la, ", fill=boje.bela, font=("Inter SemiBold", 24 * -1))
        self.canvas.create_rectangle(41.0, 230, 352.0, 231, fill=boje.bela, outline="")
        self.canvas.create_rectangle(41.0, 274.0, 352, 275.0, fill=boje.bela, outline="")
        self.canvas.create_rectangle(41.0, 313.0, 352, 314, fill=boje.bela, outline="")
    
    def create_widgets(self):
        self.entryName = wid.create_entry(self.canvas, x=41.0, y=209.0, width=312, corner_radius=0, back_color=boje.entry_login, placeholder="Ime i Prezime", auto_fin_fout=(True, "Polje"))
        self.entryName.bind("<KeyRelease>", lambda event: self.promeni_dobrodosao())

        self.entyUsername = wid.create_entry(self.canvas, x=41.0, y=253.0, width=312, corner_radius=0, back_color=boje.entry_login, placeholder="Korisničko ime", auto_fin_fout=(True, "Polje"))
        
        if(self.guest):
            self.entyUsername.delete(0, END)
            self.entyUsername.insert(0,self.user)
            self.entyUsername.configure(text_color="white")

        self.entryPassword = wid.create_entry(self.canvas, x=41.0, y=293.0, width=312, corner_radius=0, back_color=boje.entry_login, placeholder="Lozinka", auto_fin_fout=(True, "Lozinka"))
        self.entryPassword.bind("<Return>", lambda event: self.dodaj_korisnika())

        wid.create_button(self.canvas,"src/img/signup/button_3.png", x=121.0, y=337.0, width=160.0, height=35.0, command=self.dodaj_korisnika)
        wid.create_button(self.canvas,"src/img/signup/button_2.png", x=588.0, y=394.0, width=153.0, height=40.0, command=lambda: self.vrati("gost"))
        wid.create_button(self.canvas,"src/img/signup/button_1.png", x=163.0, y=379.0, width=76.0, height=15.0, command=lambda: self.vrati("login"))
        
    def promeni_dobrodosao(self):
        self.canvas.itemconfig(self.text_id, text="Dobrodošao/la, "+str((self.entryName.get().split(' '))[0]))
    
    def vrati(self,text):
        self.return_value=text
        self.window.quit()
    
    def dodaj_korisnika(self):
        username=self.entyUsername.get()
        imeIPrezime=self.entryName.get().split(" ")
        if(len(imeIPrezime)!=2):
            helperFunctions.obavestenje("Polje ime i prezime mora sadržati i ime i prezime", crveno=True)
            return
        ime=imeIPrezime[0]
        prezime=imeIPrezime[1]
        if(ime[0].islower() or prezime[0].islower()):
            helperFunctions.obavestenje("Ime i prezime moraju počinjati velikim slovom", crveno=True)
            return 
        lozinka=self.entryPassword.get()
        if(len(lozinka)<6):
            helperFunctions.obavestenje("Lozinka mora da sadrži više od 6 karaktera", crveno=True)
            return 
        if(not re.search(r'\d', lozinka)):
            helperFunctions.obavestenje("Lozinka mora sadržati bar jednu cifru", crveno=True)
            return 
        uloga=0
        status_clanstva=1
        uplacen_paket=0
        datum_registracije=datetime.date.today().strftime("%Y-%m-%d")
        obnova_clanarine=datum_registracije
        
        if(not self.guest):
            nalog=bp_korisnici.dodaj_korisnika(username, lozinka, ime, prezime, uloga,status_clanstva, uplacen_paket,datum_registracije,obnova_clanarine)
            if nalog==0: return
        else:
            nalog=bp_korisnici.azuriraj_korisnika(self.user, username, lozinka, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije,obnova_clanarine)
            if nalog==0: return 
        self.vrati(nalog)