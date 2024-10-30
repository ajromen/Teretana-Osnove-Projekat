import sqlite3

connection=sqlite3.connect("baza.db")
cursor=connection.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS
               teretana(id INTEGER PRIMARY_KEY,
               imeTeretane TEXT)
               """)

cursor.execute("""
               INSERT INTO teretana(id,imeTeretane) 
                    VALUES(0,'TopForm'),
                          (1,'ClassicGym'),
                          (2,'Colosseum')
               """)

cursor.execute("SELECT * FROM teretana")
