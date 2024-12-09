'''Termin
id_termina          CHAR(6) PRIMARY KEY NOT NULL,
datum_odrzavanja    DATE,
id_treninga         CHAR(4),
obrisan             BOOLEAN,

FOREIGN KEY (id_treninga) REFERENCES Trening(id_treninga)
'''