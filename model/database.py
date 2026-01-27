import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")

url = urlparse(DATABASE_URL)
class SQL:
    @staticmethod
    def conexao():
        return psycopg2.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],
            port=url.port
        )
