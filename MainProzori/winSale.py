import bp_sale
from imports import *

class SaleWindow(winTemplate):
    def __init__(self,sala,escfunk=None,broj_mesta=None):
        super().__init__(window=None,escfunk=escfunk)
        self.id_sale=sala
        self.window=None
        
        
    def start(self):
        self.get_sala_info()
        width=self.br_kolona*40+40
        height=self.br_redoova*40+140
        self.window=helperFunctions.napravi_toplevel(title="Sala",height=height,width=width)
        self.window.protocol("WM_DELETE_WINDOW", self.escfunk)

        self.create_canvas(width=width,height=height)
    
    def get_sala_info(self):
        self.sala_naziv,self.br_redoova,self.oznaka_kolona=bp_sale.get_sala(self.id_sale)
        self.br_kolona=len(self.oznaka_kolona)