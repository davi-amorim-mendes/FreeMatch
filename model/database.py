import mysql.connector

class SQL:
    @staticmethod
    def conexao():
        return mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="DaviSQL2005@",
                                       database="freematch")