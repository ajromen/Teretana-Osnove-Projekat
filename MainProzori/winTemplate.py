# MainProzori/winTemplate.py
import os
from imports import *

class winTemplate:
    def __init__(self, window, main_window, uloga):
        self.window = window
        self.main_window = main_window
        self.uloga = uloga
        self.current_canvas = None

    def create_canvas(self, bg_color="#010204", height=618, width=860):
        self.current_canvas = Canvas(self.window, bg=bg_color, height=height, width=width, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)

    def create_exit_button(self):
        wid.create_button(self.current_canvas, "./src/img/Widget/btnExit.png", 812, 9, 33, 33, lambda: self.main_window.unisti_trenutni_win())

    def create_search_button(self, command):
        wid.create_button(self.current_canvas, "./src/img/Widget/btnSearch.png", 358, 53, 33, 33, command)

    def create_table_bg(self, velika=False)->int:
        if velika: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina_duza.png", 23, 102)
            return 470
        else: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina.png", 23, 102)
            return 400
            
    def create_table(self, columns, velika=False):
        height=self.create_table_bg(velika)
        self.table = wid.create_table(self.current_canvas, self.popuni_tabelu, tuple(columns), height=height)
        for column in columns:
            self.table.column(column, width=100)

    def create_cmbbxSearch(self, values, x=681, y=53):
        self.create_label("Pretraži po:", x-71, 62)
        self.cmbbxSearch = self.create_comboBox(values, x, y)

    def create_comboBox(self, values, x, y, width=148,top_level=False,variable=None):
        canvas=self.if_top_level_canvas(top_level)
        return wid.create_comboBox(canvas, values, x=x, y=y,width=width,variable=variable)

    def create_entry_search(self, command):
        self.searchPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/searchPozadina.png", 23, 53)
        self.entrySearch = wid.create_entry_search(self.current_canvas, command)

    def create_label(self, text, x, y, font_size=12,top_level=False):
        canvas=self.if_top_level_canvas(top_level)
        wid.create_label(canvas, text, x, y, font_size)

    def create_button(self, image_path, x, y, width, height, command,top_level=False):
        canvas=self.if_top_level_canvas(top_level)
        wid.create_button(canvas, image_path, x, y, width, height, command)
        
    def napravi_sql_cmbbx(self, text, labelX, labelY, comboX, comboY, query, broj_kolona=1, specificni=False,top_level=False):  
        canvas=self.if_top_level_canvas(top_level)
        return wid.napravi_sql_cmbbx(canvas, text, labelX, labelY, comboX, comboY, query, broj_kolona, specificni)
        
    def selektuj_vrednost_comboBox(self, cmbbx, vrednost):
        wid.selektuj_vrednost_comboBox(cmbbx, vrednost)
        
    def create_switch(self, x, y, width=43, height=24,top_level=False):
        canvas=self.if_top_level_canvas(top_level)
        swtch=ctk.CTkSwitch(canvas,width=width,height=height,text='')
        swtch.place(x=x,y=y)
        return swtch

    def create_text_button(self, text, x, y, command=None,width=140,height=28,top_level=False,hover_color="#144870",fg_color="#1F6AA5"):
        canvas=self.if_top_level_canvas(top_level)
        btn = ctk.CTkButton(canvas, text=text, command=command,width=width,height=height,font=("Inter", 15),fg_color=fg_color,hover_color=hover_color)
        btn.place(x=x,y=y)
        return btn
        
    def if_top_level_canvas(self,top_level)->Canvas:
        if top_level:canvas=self.trenutni_window
        else:canvas=self.current_canvas
        return canvas
        
    def create_entry(self, x, y, on_focus_in=None, on_focus_out=None, placeholder='',width=303,height=20,belo=False,state="normal",corner_radius=5,back_color="#080A17",manual_fin_fon=(False,"Polje"),justify="left",top_level=False):
        canvas=self.if_top_level_canvas(top_level)
        return wid.create_entry(canvas, x, y, on_focus_in, on_focus_out, placeholder, width, height, belo, state, corner_radius, back_color, manual_fin_fon, justify)
    
    def popuni_tabelu(self):
        raise NotImplementedError("Metoda popuni_tabelu nije implementirana")