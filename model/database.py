import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
url = urlparse(DATABASE_URL)
class SQL:
    @staticmethod
    def conexao():
        return psycopg2.connect(
            host=url.path[1:],
            user=url.username,
            password=url.password,
            database=url.hostname,
            port=url.port
        )
