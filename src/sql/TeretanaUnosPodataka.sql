PRAGMA foreign_keys = ON;

INSERT INTO Korisnici(username,password,ime,prezime,uloga,status_clanstva,uplacen_paket,datum_registracije,obnova_clanarine)
	VALUES  ('admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', NULL, NULL, 2, NULL, NULL, NULL, NULL),
			('donald', 'ea94aac9173c51185e3358cf16c30d7150157e5fa584c2ba11bddea64f79178c', 'Donald', 'Tramp', 2, NULL, NULL, '2024-11-09', NULL),
			-- Instruktori --
			("milovan", '1d9e5f02731c9caaccb9edb760273a55f19e6d45bbe3c6e173d416d6b7d9a66d', 'Milovan', 'Arsenović', 1, NULL, NULL, '2024-11-09', NULL),
			('ljuba', 'a2018358dbac5a9a2e45b3ebe0341611ef74772d9f1e02259003956c39330824', 'Ljubinka', 'Leposavić', 1, NULL, NULL, '2024-11-09', NULL),
			('momir', 'c6476556a13b4d96f1c86143979bbf68f2586861f462aef3c1bc65bb214a0cbd', 'Momir', 'Stanojević', 1, NULL, NULL, '2024-11-09', NULL),
			('milica', '6de0eacc1cb7082381fb0424a9362a148dbaf8c0e828d970bdf89a966b17e115', 'Milica', 'Adamović', 1, NULL, NULL, '2024-11-09', NULL),
			-- Korisnici --
			('nekoime', '61fe830be79fdb5beb2a858e96764346e0e0a914dce5470a7a3c85b284ab1643', 'Aleksandar', 'Pavlović', 0, 1, 0, '2024-11-09', '2024-01-09'),
			('aqua', 'aca3dddfa02ed7bb64a0248be5980963da0f610430e2c83aa40d5ee673c405da', 'Akva', 'Vivić', 0, 1, 0, '2024-11-09', '2024-11-09'),
			('dragan', '612a1fe34b1ca6b77952919d4a96e80bdd29baa44f1d0cb22d1333b405a25e75', 'Dragan', 'Nedeljković', 0, 1, 1, '2024-11-09', '2024-11-09'),
			('rolex', 'fd1bb71bf48668c662f44a0ae0213cbaa2a34c3099076cc2b20a1312d84bff2c', 'Rolex', 'Jovanović', 0, 1, 1, '2024-11-09', '2024-12-20'),
			-- Gosti --
			('gost', '612a1fe34b1ca6b77952919d4a96e80bdd29baa44f1d0cb22d1333b405a25e75', NULL, NULL, -1, NULL, NULL, NULL, NULL),
			--Svi obrisani korisnici sa rezervacijom--
			('obrisan_korisnik', '89104ddb8160b3c10c8e74600eb8ba1bcb91553aad4ae3ec66abcfd9d8c69c82', "Obrisani", "Korisnik", 0, NULL, NULL, NULL, NULL);


			
INSERT INTO Sala(id_sale, naziv, broj_redova, oznaka_mesta)
	VALUES	(1, "Sala 1", 4, "ABCDEF"),
			(2, "Sala 2", 2, "ABC"),
			(3, "Sala 3", 4, "123"),
			(4, "Sala 4", 3, "1234567"),
			(5, "Sala 5", 11, "AB"),
			(6, "Sala 6", 1, "KLMN");

INSERT INTO Vrste_treninga(id_vrste_treninga, naziv)
	VALUES	(1, "Sagorite masnoće: Trening za mršavljenje"),
			(2, "Izvajajte telo: Rutina za jačanje i definisanje mišića"),
			(4, "Aktivni i zdravi u zrelim godinama: Vežbe za starije osobe"),
			(5, "Nakon povrede do pobede: Rehabilitacija i povratak na teren"),
			(6, "Fitnes za buduće mame: Trening tokom trudnoće");

INSERT INTO Program(id_programa, naziv, id_vrste_treninga, trajanje, id_instruktora, potreban_paket, opis)
	VALUES  (1,"Mršavljenje uz Momira", 1, 90, "momir", 0,"Smršaćeš."),
			(2,"Izvajajte telo uz Ljubinku", 2, 60, "ljuba", 0, ""),
			(3,"Fontana Mladosti - Milovan", 4, 30, "milovan", 1, ""),
			(4,"Milica do pobede", 5, 45, "milica", 1, ""),
			(5,"Od mama za mame - Momir", 6, 45, "milica", 1, "");

INSERT INTO Trening(id_treninga, id_sale, vreme_pocetka, vreme_kraja, dani_nedelje, id_programa)
	VALUES  ("1111",3,"12:45","14:15","Pon,Uto,Sre,Čet,Pet,Sub,Ned",1),
			("1245",5,"08:00","08:30","Pon,Uto,Sre,Čet,Pet,Sub",3),
			("6421",6,"22:00","22:45","Pon,Uto,Sre,Čet,Pet,Sub,Ned",4),
			("9909",1,"09:00","10:00","Pon,Sre,Pet,Sub",2),
			("9435",2,"18:00","18:45","Uto,Čet,Sub",5),
			("1112",4,"18:00","19:30","Uto,Čet,Pet,Ned",1);

INSERT INTO Termin(id_termina, datum_odrzavanja, id_treninga)
	VALUES  ("1111AA",'2024-01-01',"1111"),
			("1112CZ",'2024-01-01',"1112"),
			("6421KM",'2024-01-01',"6421"),
			("9909PJ",'2024-02-01',"9909"),
			("1245MK",'2024-02-01',"1245"),
			("9435AA",'2024-12-21',"9435");

INSERT INTO Rezervacija(id_rezervacije, id_korisnika, id_termina, oznaka_reda_kolone, datum)
	VALUES  (1,'aqua',"1111AA",'22','2024-11-11'),
			(6,'aqua',"6421KM",'L1','2024-11-11'),
			(2,'rolex',"6421KM",'M1','2024-01-01'),
			(3,'dragan',"9909PJ",'A3','2024-01-09'),
			(4,'nekoime',"1245MK",'B6','2024-01-10'),
			(5,'gost',"1245MK",'B3','2020-01-10'),
			(7,'rolex',"9435AA",'C2','2024-02-15');

