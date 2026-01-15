import mysql.connector

def conexao():
    return mysql.connector.connect(host="localhost", user="root", password="DaviSQL2005@", database="freematch")

class MatchRepository:
    @classmethod
    def validar_interesses(cls, interesses_user):
        conn = None
        cursor = None
        usuarios = False
        interesses_geral = []

        try:
            conn = conexao()
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
            conn = conexao()
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
            conn = conexao()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios_interesses WHERE usuario_id=%s", (usuario_id,))

            interesses_user = cursor.fetchall()
            return interesses_user
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


