from imports import *

class IzvestajiWindow(winTemplate):
    def __init__(self, window, main_window,uloga):
        super().__init__(window,main_window,uloga)
        
    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_table_bg(True)
        
        self.izvestajiMap={
            "Izveštaj A": "Lista rezervacija po datumu rezervacije",
            "Izveštaj B": "Lista rezervacija po datumu termina",
            "Izveštaj C": "Lista rezervacija po datumu rezervacije i instruktoru",
            "Izveštaj D": "Broj rezervacija za dan u nedelji",
            "Izveštaj E": "Broj rezervacija po instruktoru (30 dana)",
            "Izveštaj F": "Broj realizovanih rezervacija po paketu",
            "Izveštaj G": "Top 3 najpopularnija treninga",
            "Izveštaj H": "Najpopularniji dan u nedelji (1 godina)"
        }
        
        self.create_comboBox([self.izvestajiMap["Izveštaj "+slovo] for slovo in "ABCDEFGH"], 23, 54,width=184)