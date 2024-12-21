from imports import *

class IzvestajiWindow(winTemplate):
    def __init__(self, window, main_window,uloga):
        super().__init__(window,main_window,uloga)
        
    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_table_bg(True)
        
        self.izvestajiMap={
            "A": "Lista rezervacija po datumu rezervacije",
            "B": "Lista rezervacija po datumu termina",
            "C": "Lista rezervacija po datumu rezervacije i instruktoru",
            "D": "Broj rezervacija za dan u nedelji",
            "E": "Broj rezervacija po instruktoru (30 dana)",
            "F": "Broj realizovanih rezervacija po paketu",
            "G": "Top 3 najpopularnija treninga",
            "H": "Najpopularniji dan u nedelji (1 godina)"
        }
        self.varIzvestaj=StringVar()
        self.cmbbxIzvestaj=self.create_comboBox([slovo+". "+self.izvestajiMap[slovo] for slovo in "ABCDEFGH"], 23, 54,width=184,variable=self.varIzvestaj)
        self.varIzvestaj.trace_add("write", self.on_combo_change)
        
    def on_combo_change(self, *args):
        opcija=self.varIzvestaj.get().split(". ")[0]
        match opcija:
            case "A": pass
            
    def a_izvestaj(self):
        pass