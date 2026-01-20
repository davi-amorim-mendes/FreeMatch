import mysql.connector
from datetime import datetime
from model.database import SQL

class MatchRepository:
    @classmethod
    def validar_interesses(cls, interesses_user):
        conn = None
        cursor = None
        usuarios = False
        interesses_geral = []

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios_interesses")
            usuarios = cursor.fetchall()

            for interesse in interesses_user:
                for usuario in usuarios:
                    if interesse["interesse_id"] == usuario["interesse_id"] and interesse["usuario_id"] != usuario["usuario_id"]:
                        interesses_geral.append(usuario["usuario_id"])
            
            return list(set(interesses_geral)) # REMOVE IDS DUPLICADOS
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @classmethod
    def validar_usuarios(cls, usuario_info, interesses_geral):
        conn = None
        cursor = None
        usuarios_validados = []
        usuario_aux = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            for id in interesses_geral:
                cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
                usuario_aux = cursor.fetchone()

                # SE O USUÁRIO NÃO EXISTIR OU NÃO TIVER FOTO CONTINUA O LOOP
                if not usuario_aux or usuario_aux["foto"] is None:
                    continue
                
                # TESTE DE GÊNERO
                if usuario_info["generopref"] == "outro":
                    usuarios_validados.append(usuario_aux)
                elif usuario_info["generopref"] == usuario_aux["genero"]:
                    usuarios_validados.append(usuario_aux)
                        
                # TRATAMENTO DE DADOS
                for usuario in usuarios_validados:
                    usuario.pop("email", None)
                    usuario.pop("senha", None)
                    usuario.pop("generopref", None)
                    usuario.pop("nivel", None)

            return usuarios_validados
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def pegar_interesses_user(cls, usuario_id):
        conn = None
        cursor = None
        interesses_user = []

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios_interesses WHERE usuario_id=%s", (usuario_id,))

            interesses_user = cursor.fetchall()
            return interesses_user
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def salvar_like(cls, dados, id_usuario):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM likes WHERE id_usuario=%s AND id_curtido=%s", (id_usuario, dados["id_curtido"]))
            like_ex = cursor.fetchone()
            if like_ex:
                return resultado
            cursor.execute("INSERT INTO likes(id_usuario, id_curtido, data) values(%s,%s,%s)", (id_usuario, dados["id_curtido"], dados["datetime"]))

            conn.commit()
            resultado = True
            return resultado if resultado else False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def checar_match(cls, id_usuario, id_curtido):
        conn = None
        cursor = None
        resultado = False

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM matches WHERE usuario1=%s AND usuario2=%s", (id_curtido, id_usuario))
            match_ex1 = cursor.fetchone()
            if match_ex1:
                return False
            cursor.execute("SELECT * FROM matches WHERE usuario1=%s AND usuario2=%s", (id_usuario, id_curtido))
            match_ex2 = cursor.fetchone()
            if match_ex2:
                return False
            cursor.execute("SELECT * FROM likes WHERE id_usuario=%s AND id_curtido=%s", (id_usuario, id_curtido))
            like = cursor.fetchone()
            cursor.execute("SELECT * FROM likes WHERE id_usuario=%s AND id_curtido=%s", (id_curtido, id_usuario))
            match = cursor.fetchone()

            if like and match:
                resultado = cls.salvar_match(match)
             
            return resultado
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def salvar_match(cls, match):
        conn = None
        cursor = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute("INSERT INTO matches(usuario1, usuario2, data) values(%s,%s,%s)", (match["id_usuario"], match["id_curtido"], agora))

            match_id = cursor.lastrowid

            cursor.execute("INSERT INTO conversas(id_match) values(%s)", (match_id,))
            conn.commit()
            return True
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def pegar_matchs(cls, id):
        conn = None
        cursor = None
        matches = []
        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM matches WHERE usuario1=%s OR usuario2=%s", (id, id))
            matches = cursor.fetchall()

            for match in matches:
                if match["usuario1"] != id:
                    match["usuario_par"] = match["usuario1"]
                else:
                    match["usuario_par"] = match["usuario2"]

            return matches
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

