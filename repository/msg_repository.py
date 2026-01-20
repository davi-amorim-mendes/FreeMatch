from model.database import SQL

class MsgRepository:
    @classmethod
    def salvar_mensagem(cls, id_conversa, id_remetente, texto):
        conn = SQL.conexao()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensagens(id_conversa, id_remetente, texto) values(%s,%s,%s)", (id_conversa, id_remetente, texto))
        conn.commit()

        return
    
    @classmethod
    def listar_mensagens(cls, id_conversa):
        conn = SQL.conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_remetente, texto, criada_em FROM mensagens WHERE id_conversa=%s ORDER BY criada_em", (id_conversa,))
        mensagens = cursor.fetchall()

    @classmethod
    def listar_conversas(cls, matches):
        conn = None
        cursor = None
        conversas = []

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(dictionary=True)

            for match in matches:
                cursor.execute("SELECT * FROM conversas WHERE id_match=%s", (match["id_match"],))
                conversas.append(cursor.fetchone())

            return conversas
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
