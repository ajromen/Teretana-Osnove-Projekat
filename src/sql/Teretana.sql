PRAGMA foreign_keys = ON;

--RESTARTOVANJE TABELA 
DROP TABLE IF EXISTS Korisnici;
CREATE TABLE Korisnici
	( username CHAR(25) PRIMARY KEY NOT NULL,
	  password CHAR(64),
	  ime CHAR(25),
	  prezime CHAR(25),
	  uloga SMALLINT,
	  status_clanstva BOOLEAN,
	  uplacen_paket BOOLEAN,
	  datum_registracije DATE,
	  obnova_clanarine DATE,
	  nagradjen BOOLEAN
	  );

DROP TABLE IF EXISTS Trening;
CREATE TABLE Trening 
	( id_treninga CHAR(4) PRIMARY KEY NOT NULL,
	  id_sale INTEGER, 
	  vreme_pocetka TIME,
	  vreme_kraja TIME,
	  dani_nedelje CHAR(28),
	  id_programa INTEGER,
	  obrisan BOOLEAN,
	  FOREIGN KEY (id_sale) REFERENCES Sala(id_sale)
	  FOREIGN KEY (id_programa) REFERENCES Program(id_programa)
	  );
	  
DROP TABLE IF EXISTS Sala;
CREATE TABLE Sala 
	( id_sale INTEGER PRIMARY KEY NOT NULL,
	  naziv CHAR(15),
	  broj_redova SMALLINT,
	  oznaka_mesta CHAR(20),
	  obrisana BOOLEAN
	);
	
DROP TABLE IF EXISTS Program;
CREATE TABLE Program 
	( id_programa INTEGER PRIMARY KEY NOT NULL,
	  naziv CHAR(30),
	  id_vrste_treninga INTEGER,
	  trajanje SMALLINT,
	  id_instruktora CHAR(25),
	  potreban_paket BOOLEAN,
	  opis BLOB,
	  obrisan BOOLEAN,
	  FOREIGN KEY (id_vrste_treninga) REFERENCES Vrste_treninga(id_vrste_treninga),
	  FOREIGN KEY (id_instruktora) REFERENCES Korisnici(username)
	  );

DROP TABLE IF EXISTS Vrste_treninga;
CREATE TABLE Vrste_treninga 
	( id_vrste_treninga INTEGER PRIMARY KEY NOT NULL,
	  naziv BLOB, 
	  obrisan BOOLEAN
	  );

DROP TABLE IF EXISTS Termin;
CREATE TABLE Termin 
	( id_termina CHAR(6) PRIMARY KEY NOT NULL,
	  datum_odrzavanja DATE,
	  id_treninga CHAR(4),
	  obrisan BOOLEAN,
	  FOREIGN KEY (id_treninga) REFERENCES Trening(id_treninga)
	  );

DROP TABLE IF EXISTS Rezervacija;
CREATE TABLE Rezervacija 
	( id_rezervacije INTEGER PRIMARY KEY NOT NULL,
	  id_korisnika CHAR(25),
	  id_termina CHAR(6),
	  oznaka_reda_kolone CHAR(5),--A123548
	  datum DATE,
	  FOREIGN KEY (id_korisnika) REFERENCES Korisnici(username)
	  FOREIGN KEY (id_termina) REFERENCES Termin(id_termina)
	  );
	