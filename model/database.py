import psycopg2

class SQL:
    @staticmethod
    def conexao():
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="DaviSQL2005@",
            database="freematch",
            port=5432
        )
