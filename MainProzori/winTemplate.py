# MainProzori/winTemplate.py
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

    def create_search_button(self, search_command):
        wid.create_button(self.current_canvas, "./src/img/Widget/btnSearch.png", 358, 53, 33, 33, search_command)

    def create_table(self, columns, velika=False):
        if velika: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina_duza.png", 23, 102)
            height = 480
        else: 
            self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina.png", 23, 102)
            height = 400
        
        self.table = wid.create_table(self.current_canvas, self.popuni_tabelu, tuple(columns), height=height)
        for column in columns:
            self.table.column(column, width=100)

    def create_cmbbxSearch(self, values, x=681, y=53):
        self.cmbbxSearch = self.create_comboBox(values, x, y)

    def create_comboBox(self, values, x, y):
        return wid.create_comboBox(self.current_canvas, values, x=x, y=y)

    def create_entry_search(self, command):
        self.searchPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/searchPozadina.png", 23, 53)
        self.entrySearch = wid.create_entry_search(self.current_canvas, command)

    def create_label(self, text, x, y, font_size=12):
        wid.create_label(self.current_canvas, text, x, y, font=("Inter", font_size * -1))

    def create_button(self, image_path, x, y, width, height, command):
        wid.create_button(self.current_canvas, image_path, x, y, width, height, command)

    def popuni_tabelu(self, tabela, kriterijum='', pretraga=''):
        raise NotImplementedError("This method should be overridden in the subclass")

    def pretrazi(self):
        raise NotImplementedError("This method should be overridden in the subclass")

    def izlistaj(self, kriterijum='', pretraga=''):
        raise NotImplementedError("This method should be overridden in the subclass")