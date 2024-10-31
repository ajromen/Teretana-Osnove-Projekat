DROP TABLE IF EXISTS Korisnici;
CREATE TABLE Korisnici 
	( username CHAR(25) PRIMARY KEY NOT NULL,
	  password CHAR(64),
	  ime_prezime CHAR(40),
	  uloga SMALLINT,
	  status_clanstva BOOLEAN,
	  uplacen_paket BOOLEAN,
	  datum_registracije DATE
	  );

DROP TABLE IF EXISTS Trening;
CREATE TABLE Trening 
	( id_treninga CHAR(4) PRIMARY KEY NOT NULL,
	  id_sala INTEGER,
	  vreme_pocetka TIME,
	  vreme_kraja TIME,
	  dani_nedelje CHAR(7),
	  id_programa INTEGER
	  );
	  
DROP TABLE IF EXISTS Sala;
CREATE TABLE Sala 
	( id_sale INTEGER PRIMARY KEY NOT NULL,
	  naziv CHAR(15),
	  broj_redova SMALLINT,
	  oznaka_mesta CHAR(15)
	);
	
DROP TABLE IF EXISTS Program;
CREATE TABLE Program 
	( id_programa INTEGER PRIMARY KEY NOT NULL,
	  naziv CHAR(20),
	  id_vrste_treninga INTEGER,
	  trajanje TIME,
	  id_instruktora INTEGER,
	  potreban_paket BOOLEAN,
	  opis BLOB
	  );

DROP TABLE IF EXISTS Vrste_treninga;--OPCIONALNO OBRISI AKO SE PREDOMISLIS
CREATE TABLE Vrste_treninga 
	( id_vrste_treninga INTEGER PRIMARY KEY NOT NULL,
	  naziv CHAR(20)
	  );

DROP TABLE IF EXISTS Instruktor_program;
CREATE TABLE Instruktor_program 
	( id_instruktor_program INTEGER PRIMARY KEY,
	  id_instruktora INTEGER,
	  id_programa INTEGER
	  );

DROP TABLE IF EXISTS Termin;
CREATE TABLE Termin 
	( id_termina CHAR(6) PRIMARY KEY NOT NULL,
	  datum_odrzavanja DATE,
	  id_treninga CHAR(4)
	  );

DROP TABLE IF EXISTS Rezervacija;
CREATE TABLE Rezervacija 
	( id_rezervacije INTEGER PRIMARY KEY NOT NULL,
	  id_korisnika INTEGER,
	  id_termina INTEGER,
	  oznaka_reda_kolone INTEGER,
	  datum DATE
	  );

