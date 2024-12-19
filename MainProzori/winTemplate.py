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

    def create_table(self, columns, velika=False):
        if velika: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina_duza.png", 23, 102)
            height = 470
        else: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina.png", 23, 102)
            height = 400
        
        self.table = wid.create_table(self.current_canvas, self.popuni_tabelu, tuple(columns), height=height)
        for column in columns:
            self.table.column(column, width=100)

    def create_cmbbxSearch(self, values, x=681, y=53):
        self.create_label("Pretraži po:", x-71, 62)
        self.cmbbxSearch = self.create_comboBox(values, x, y)

    def create_comboBox(self, values, x, y):
        return wid.create_comboBox(self.current_canvas, values, x=x, y=y)

    def create_entry_search(self, command):
        self.searchPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/searchPozadina.png", 23, 53)
        self.entrySearch = wid.create_entry_search(self.current_canvas, command)

    def create_label(self, text, x, y, font_size=12):
        wid.create_label(self.current_canvas, text, x, y, font_size)

    def create_button(self, image_path, x, y, width, height, command):
        wid.create_button(self.current_canvas, image_path, x, y, width, height, command)
        
    def napravi_sql_cmbbx(self, text, labelX, labelY, comboX, comboY, query, broj_kolona=1, specificni=False):
        return wid.napravi_sql_cmbbx(self.current_canvas, text, labelX, labelY, comboX, comboY, query, broj_kolona, specificni)
        
    def selektuj_vrednost_comboBox(self, cmbbx, vrednost):
        wid.selektuj_vrednost_comboBox(cmbbx, vrednost)
        
    def create_entry(self, x, y, on_focus_in=None, on_focus_out=None, placeholder='',width=303,height=20,belo=False,state="normal",corner_radius=5,back_color="#080A17",manual_fin_fon=(False,"Polje"),justify="left"):
        return wid.create_entry(self.current_canvas, x, y, on_focus_in, on_focus_out, placeholder, width, height, belo, state, corner_radius, back_color, manual_fin_fon, justify)