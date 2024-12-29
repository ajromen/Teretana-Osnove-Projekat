
import bp_sale
from imports import *

class SaleWindow(winTemplate):
    def __init__(self,sala,escfunk=None,oznaka_mesta=None):
        super().__init__(window=None,escfunk=escfunk)
        self.id_sale=sala
        self.window=None
        self.btn_width=50
        self.btn_prostor=6
        self.selektovano_dugme=oznaka_mesta
        
    def start(self):
        self.get_sala_info()
        width=self.br_kolona*self.btn_width+self.btn_prostor*(self.br_kolona-1)+2*20
        height=39+self.br_redoova*self.btn_width+self.btn_prostor*(self.br_redoova-1)+20
        self.window=helperFunctions.napravi_toplevel(title="Sala",height=height,width=width)
        self.window.protocol("WM_DELETE_WINDOW", self.escfunk)
        self.create_canvas(height=height,width=width,x=0,y=0)
        
        self.create_label(self.sala_naziv,14,8,15)
        
        self.napravi_dugmad()
        
    
    def get_sala_info(self):
        self.sala_naziv,self.br_redoova,self.oznaka_kolona=bp_sale.get_sala(self.id_sale)
        self.br_kolona=len(self.oznaka_kolona)
        self.iskoriscena_mesta=bp_sale.get_mesta(self.id_sale)
        
    def napravi_dugmad(self):
        x=20
        y=39
        iskoriscena_mesta_set={mesto[0] for mesto in self.iskoriscena_mesta}
        for i in range(self.br_redoova):
            x=20
            for j in range(self.br_kolona):
                text=self.oznaka_kolona[j]+str(i+1)
                fg_color=boje.dugme
                hover_color=boje.dugme_hover
                command = lambda t=text: self.selektuj_dugme(t)
                if self.selektovano_dugme==text: fg_color=boje.dugme_selected#neki deafult argument
                elif text in iskoriscena_mesta_set: 
                    fg_color = boje.dugme_disabled
                    text = 'X'
                    command = None
                    hover_color = boje.dugme_disabled_hover
                    
                self.create_text_button(text,x,y,width=self.btn_width,height=self.btn_width,fg_color=fg_color,command=command,hover_color=hover_color)
                x+=self.btn_width+self.btn_prostor
            y+=self.btn_width+self.btn_prostor
                
    def selektuj_dugme(self,dugme:str=""):
        self.escfunk(dugme)
    