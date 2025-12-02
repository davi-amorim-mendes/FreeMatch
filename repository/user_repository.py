import os
from model.user_model import Usuario
import mysql.connector
import bcrypt

def conexao():
    return mysql.connector.connect(host="localhost", user="root", password="DaviSQL2005@", database="freematch")

class UsuarioRepositorio:
    @classmethod
    def adicionar(cls, usuario:Usuario):
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios(id, nome, email, senha, data, genero, generopref, relacionamento, interesses, sobre, foto, nivel) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (usuario.id, usuario.nome, usuario.email, usuario.senha, usuario.data, usuario.genero, usuario.generoPref,
             usuario.relacionamento, usuario.interesses, usuario.sobre, usuario.foto, usuario.nivel)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return True

    @classmethod
    def email_existente(cls, usuario:Usuario):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (usuario.email,))
            cursor.fetchone()

            if cursor.rowcount > 0:
                resultado = True
            return resultado
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def usuario_existente(cls, email, senha):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            usuario = cursor.fetchone()
            if bcrypt.checkpw(senha.encode("utf-8"), usuario["senha"].encode("utf-8")):
                resultado = usuario
            return resultado
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


