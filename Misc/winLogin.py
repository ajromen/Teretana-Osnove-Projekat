from baza_podataka import BazaPodataka
from imports import *
import widgets as wid

class LoginWindow:
    def __init__(self,window):
        self.window = window
        
    def start(self):
        self.return_value = 0
        helperFunctions.setup_window(self.window,"Uloguj se","760x450","#03050B")
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value
            
    def create_widgets(self):
        #korisnicko ime
        self.entryUsername = wid.create_entry(canvas=self.canvas,x=403, y=225,corner_radius=0, back_color="#1A1B20", placeholder="Korisničko ime", auto_fin_fout=(True,"Polje")) 
        self.entryUsername.bind("<KeyRelease>", self.promeni_pozdrav)
        
        #lozinka
        self.entryPassword = wid.create_entry(self.canvas,x=403, y=281,back_color="#1A1B20",corner_radius=0, placeholder="Lozinka", auto_fin_fout=(True,"Lozinka")) 
        self.entryPassword.bind("<Return>", command=lambda event: self.prijavi_se())
        
        #login dugme
        wid.create_button(self.canvas,"src/img/login/button_1.png",475,351,160,35,self.prijavi_se)
        
        # nemas nalog dugme
        wid.create_button(self.canvas,"src/img/login/button_2.png",x=513.0, y=396.0, width=80.0, height=15.0,command=lambda: self.vrati("signup"))

    def create_canvas(self):
        self.canvas = Canvas(self.window, bg="#03050B", height=450, width=760, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        self.imgPozadina=wid.create_canvas_image(self.canvas,"src/img/login/image_1.png",0, 0)
        self.imgLogo = wid.create_canvas_image(self.canvas,"src/img/Logo/TopFormLogoBeliMali2.png",565-308//2,74)
        self.text_id = self.canvas.create_text(388.0, 171.0, anchor="nw", text="Pozdrav,", fill="#FFFFFF", font=("Inter", 24 * -1))
        self.canvas.create_rectangle(403, 247.7, 706, 248.0, fill="#FFFFFF", outline="")
        self.canvas.create_rectangle(403, 302.7, 706, 303.0, fill="#FFFFFF", outline="")
        
    def promeni_pozdrav(self, event):
        self.canvas.itemconfig(self.text_id, text="Pozdrav, " + str(self.entryUsername.get()))
    
    def vrati(self,text):
        self.window.quit()
        self.return_value=text
        
    def prijavi_se(self):
        korIme=str(self.entryUsername.get())
        loz=helperFunctions.hashPassword(str(self.entryPassword.get()))
        cursor=BazaPodataka.get_cursor()
        cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+str(korIme)+"' AND password='"+str(loz)+"'")
        ima=cursor.fetchall()
        if(len(ima)!=0):
            self.vrati(ima)
        else:
            helperFunctions.obavestenje("Pogrešno korisničko ime ili lozinka")
