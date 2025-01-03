# mainProzori/winTemplate.py
import os
from imports import *
import widgets as wid

class winTemplate:
    def __init__(self, window, escfunk=None, uloga=None, u_prozoru=False, username=None):
        self.window = window
        self.current_canvas = None
        self.uloga = uloga
        self.u_prozoru=u_prozoru
        self.escfunk = escfunk
        self.top_level=False
        self.username=username
        self.pozicija_pomeranje={"x":0,"y":0}
        self.pomeranje_window=None
        self.height=608
        self.width=860

    def create_canvas(self, bg_color=boje.crna, height=608, width=860,x=230,y=0):
        if self.u_prozoru: x=0;y=-39;height+=39
        self.current_canvas = Canvas(self.window, bg=bg_color, height=height, width=width, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=x, y=y)
        if not self.u_prozoru:
            self.pomeranje_ikona=PhotoImage(file="src/img/main/pomeranje.png")
            self.current_canvas.bind("<ButtonPress-1>", self.pomeranje_start)
            self.current_canvas.bind("<B1-Motion>", self.pomeranje)
            self.current_canvas.bind("<ButtonRelease-1>", self.pomeranje_kraj)
            
    def pomeranje_start(self, event):
        self.pozicija_pomeranje["x"]=event.x
        self.pozicija_pomeranje["y"]=event.y
        x=self.window.winfo_pointerx()
        y=self.window.winfo_pointery()
        self.pomeranje_window=ctk.CTkToplevel(self.window)
        self.pomeranje_window.geometry(f"118x25+{x}+{y}")
        self.pomeranje_window.overrideredirect(True)
        # self.pomeranje_window.attributes("-transparentcolor", "white")
        canv=Canvas(self.pomeranje_window, width=118, height=25, bd=0, highlightthickness=0, bg="white")
        canv.create_image(0,0,anchor="nw",image=self.pomeranje_ikona)
        canv.pack()
        
    def pomeranje(self, event):
        if self.pomeranje_window:
            x=self.window.winfo_pointerx()
            y=self.window.winfo_pointery()
            self.pomeranje_window.geometry(f"+{x}+{y}")
        
    def pomeranje_kraj(self, event):
        if self.pomeranje_window:
            self.pomeranje_window.destroy()
            self.pomeranje_window=None
        width=self.current_canvas.winfo_width()
        height=self.current_canvas.winfo_height()
        if event.x<0 or event.y<0 or event.x>width or event.y>height:
            self.prebaci_u_prozor()
            self.escfunk()
            
    def prebaci_u_prozor(self):
        x=self.window.winfo_pointerx()
        y=self.window.winfo_pointery() 
        novi_window=ctk.CTkToplevel(self.window)
        novi_window.geometry(f"{self.width}x{self.height-50}+{x}+{y}")
        novi_window.resizable(False, False)
        prozorski=self.__class__(window=novi_window,escfunk=self.escfunk,uloga=self.uloga,u_prozoru=True,username=self.username)
        prozorski.start()

    def create_exit_button(self,x=812,y=9):
        wid.create_button(self.current_canvas, "./src/img/widget/btnExit.png", x, y, 33, 33, self.escfunk)

    def create_search_button(self, command):
        wid.create_button(self.current_canvas, "./src/img/widget/btnSearch.png", 358, 53, 33, 33, command=command)

    def create_table_bg(self, velika=False)->int:
        if velika: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/widget/tabelaPozadina_duza.png", 23, 102)
            return 470
        else: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/widget/tabelaPozadina.png", 23, 102)
            return 400
            
    def create_table(self, columns, velika=False):
        height=self.create_table_bg(velika)
        self.table = wid.create_table(self.current_canvas, self.popuni_tabelu, tuple(columns), height=height)
        for column in columns:
            self.table.column(column, width=100)

    def create_cmbbxSearch(self, values, x=681, y=53):
        self.create_label("Pretraži po:", x-71, 62)
        self.cmbbxSearchVar = StringVar()
        self.cmbbxSearch = self.create_comboBox(values, x, y,variable=self.cmbbxSearchVar,on_change=self.pretrazi)

    def create_comboBox(self, values, x, y, width=148,variable=None,on_change=None):
        return wid.create_comboBox(self.get_canvas(), values,x, y,width,variable,on_change)
    
    def napravi_sql_cmbbx(self, text, labelX, labelY, comboX, comboY, query, broj_kolona=1, specificni=False,font_size=15,variable=None,on_change=None):  
        return wid.napravi_sql_cmbbx(self.get_canvas(), text, labelX, labelY, comboX, comboY, query, broj_kolona, specificni,font_size,variable,on_change)

    def create_entry_search(self, command):
        self.searchPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/widget/searchPozadina.png", 23, 53)
        self.entrySearch = wid.create_entry_search(self.current_canvas, command)

    def create_label(self, text, x, y, font_size=12):
        wid.create_label(self.get_canvas(), text, x, y, font_size)

    def create_button(self, image_path, x, y, width=None, height=None, command=None):
        return wid.create_button(self.get_canvas(), image_path, x, y, width, height, command)
        
    def selektuj_vrednost_comboBox(self, cmbbx, vrednost):
        wid.selektuj_vrednost_comboBox(cmbbx, vrednost)
        
    def create_switch(self, x, y, width=43, height=24,):
        swtch=ctk.CTkSwitch(self.get_canvas(),width=width,height=height,text='')
        swtch.place(x=x,y=y)
        return swtch

    def create_text_button(self, text, x, y, command=None,width=140,height=28,hover_color=boje.dugme_hover,fg_color=boje.dugme):
        btn = ctk.CTkButton(self.get_canvas(), text=text, command=command,width=width,height=height,font=("Inter", 15),fg_color=fg_color,hover_color=hover_color)
        btn.place(x=x,y=y)
        return btn
        
    def get_canvas(self)->Canvas:
        if self.top_level:canvas=self.trenutni_window
        else:canvas=self.current_canvas
        return canvas
        
    def create_entry(self, x, y, on_focus_in=None, on_focus_out=None, placeholder='',width=303,height=20,belo=False,state="normal",corner_radius=5,back_color=boje.entry_main,auto_fin_fout=(False,"Polje"),justify="left",key_release=None):
        return wid.create_entry(self.get_canvas(), x, y, on_focus_in, on_focus_out, placeholder, width, height, belo, state, corner_radius, back_color, auto_fin_fout, justify, key_release)
    
    def create_date_picker(self,x,y,variable=None):
        return wid.create_date_picker(self.get_canvas(), x, y, variable)
    
    def popuni_tabelu(self):
        raise NotImplementedError("Metoda popuni_tabelu nije implementirana")
    