import os
from model.user_model import Usuario
import bcrypt
import uuid
from model.database import SQL

PASTA_FOTOS = "static/img/img_perfil"

class UsuarioRepositorio:
    @classmethod
    def adicionar(cls, interesses, usuario:Usuario):
        conn = SQL.conexao()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios(id, nome, email, senha, data, genero, generopref, relacionamento, sobre, foto, nivel) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (usuario.id, usuario.nome, usuario.email, usuario.senha, usuario.data, usuario.genero, usuario.generoPref,
             usuario.relacionamento, usuario.sobre, usuario.foto, usuario.nivel)
        )

        for interesse in interesses:
            cursor.execute("INSERT INTO usuarios_interesses(usuario_id, interesse_id) values(%s, %s)", (usuario.id, interesse))

        conn.commit()
        cursor.close()
        conn.close()

        return True

    @classmethod
    def email_existente_class(cls, usuario:Usuario):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (usuario.email,))

            resultado = cursor.fetchone()
            return resultado if resultado else False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def email_existente(cls, email):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))

            resultado = cursor.fetchone()
            return resultado if resultado else False
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
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            usuario = cursor.fetchone()

            if not usuario:
                return resultado

            if bcrypt.checkpw(senha.encode("utf-8"), usuario["senha"].encode("utf-8")):
                resultado = usuario
            return resultado
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def buscar_usuario(cls, id):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
            usuario = cursor.fetchone()
            if not usuario:
                return resultado
            
            return usuario
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def alterar_senha(cls, usuario_id, nova_senha):
        nova_senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = SQL.conexao()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET senha=%s WHERE id=%s", (nova_senha_hash, usuario_id))
        conn.commit()
        cursor.close()
        conn.close()

        return True

    @classmethod
    def salvar_foto_local(cls, foto):
            ext = os.path.splitext(foto.filename)[1] # EXTENSÃO DO ARQUIVO
            nome_foto = f"{uuid.uuid4()}{ext}"


            caminho = os.path.join(PASTA_FOTOS, nome_foto)

            foto.save(caminho)

            url = f'/static/img/img_perfil/{nome_foto}'

            return url
    
    @classmethod
    def salvar_foto_db(cls, url, usuario_id):
        conn = SQL.conexao()
        cursor = conn.cursor()

        cursor.execute("SELECT foto FROM usuarios WHERE id=%s", (usuario_id,))

        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            foto_antiga = resultado[0].lstrip("/")

            if os.path.exists(foto_antiga):
                os.remove(foto_antiga)

        cursor.execute("UPDATE usuarios SET foto=%s WHERE id=%s", (url, usuario_id))

        conn.commit()
        cursor.close()
        conn.close()

        return

    @classmethod
    def editar_sobre(cls, sobre, id):
        conn = None
        cursor = None
        
        conn = SQL.conexao()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET sobre=%s WHERE id=%s", (sobre, id))
        conn.commit()
        cursor.close()
        conn.close()

        return
    
    @classmethod
    def excluir_interesse(cls, id_usuario):
        conn = None
        cursor = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM usuarios_interesses WHERE usuario_id=%s", (id_usuario,))
            conn.commit()
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @classmethod
    def excluir_usuario(cls, id_usuario):
        conn = None
        cursor = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM usuarios WHERE id=%s", (id_usuario,))
            conn.commit()
            return True
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()