from imports import *

class SaleWindow(winTemplate):
    def __init__(self, window, escfunk=None, uloga=None, sala=None, u_prozoru=False):
        super().__init__(window, escfunk, uloga, u_prozoru)
        self.sala=sala
        
    def start(self):
        
        self.create_canvas()
    
    