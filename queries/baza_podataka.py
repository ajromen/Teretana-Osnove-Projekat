import sqlite3
import os
import helperFunctions

class BazaPodataka:
    connection = None
    cursor = None
    
    @classmethod
    def get_conn_curs(cls):
        cls.povezi_se()
        return cls.connection, cls.cursor

    @classmethod
    def povezi_se(cls):
        if cls.connection is None:
            cls.connection = sqlite3.connect("Teretana.db")
            cls.cursor = cls.connection.cursor()
    
    @classmethod
    def get_connection(cls):
        cls.povezi_se()
        return cls.connection
    
    @classmethod
    def get_cursor(cls):
        cls.povezi_se()
        return cls.cursor
    
    @classmethod
    def zatvori(cls):
        if cls.connection:
            cls.connection.close()
            cls.connection = None
            cls.cursor = None

    @classmethod
    def izvrsi_skripte_iz_fajla(cls, fajl):
        conn, cur = cls.get_conn_curs()
        with open(fajl, 'r', encoding='utf-8') as file:
            sql_fajl = file.read()
            
        sqlKomande = sql_fajl.split(';')

        for i in range(0,len(sqlKomande)):
            try:
                cur.execute(sqlKomande[i])
            except sqlite3.OperationalError as msg:
                print("Command skipped: ", msg,", Redni broj komande :"+str(i))
        conn.commit()

    @classmethod
    def restart(cls):
        cls.zatvori()
        if os.path.exists("Teretana.db"):
            os.remove("Teretana.db")
        
        cls.povezi_se()
        cls.izvrsi_skripte_iz_fajla("src/sql/Teretana.sql")
        cls.izvrsi_skripte_iz_fajla("src/sql/TeretanaUnosPodataka.sql")
        print("Baza uspešno resetovana")

    @classmethod
    def commit(cls):
        cls.povezi_se()
        cls.connection.commit()
        
