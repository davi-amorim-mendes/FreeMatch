from psycopg2.extras import RealDictCursor
from model.database import SQL

class MsgRepository:
    @classmethod
    def salvar_mensagem(cls, id_conversa, id_remetente, texto):
        conn = None
        cursor = None
        try:
            conn = SQL.conexao()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mensagens(id_conversa, id_remetente, texto) values(%s,%s,%s)", (id_conversa, id_remetente, texto))
            conn.commit()
            return True
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @classmethod
    def listar_mensagens(cls, id_conversa):
        conn = None
        cursor = None
        try:
            conn = SQL.conexao()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id_remetente, texto, criada_em FROM mensagens WHERE id_conversa=%s ORDER BY criada_em", (id_conversa,))
            mensagens = cursor.fetchall()

            if mensagens:
                for msg in mensagens:
                    if msg.get('criada_em'):
                        msg['criada_em'] = msg['criada_em'].strftime('%Y-%m-%d %H:%M:%S')
                        
            return mensagens
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def listar_conversas(cls, matches):
        conn = None
        cursor = None
        conversas = []

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            for match in matches:
                cursor.execute("SELECT * FROM conversas WHERE id_match=%s", (match["id_match"],))
                conversas.append(cursor.fetchone())

            return conversas
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def obter_ultima_mensagem(cls, id_conversa):
        conn = None
        cursor = None
        try:
            conn = SQL.conexao()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT texto, criada_em FROM mensagens WHERE id_conversa=%s ORDER BY criada_em DESC LIMIT 1", 
                (id_conversa,)
            )
            mensagem = cursor.fetchone()
            return mensagem
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def qtd_msg(cls, conversas):
        conn = None
        cursor = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            mensagens = []
            for conversa in conversas:
                cursor.execute("SELECT COUNT(*) AS total FROM mensagens WHERE id_conversa=%s", (conversa["id_conversa"],))
                mensagem = cursor.fetchone()
                mensagens.append(mensagem)

            return mensagens
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def excluir_msg(cls, id_conversa):
        conn = None
        cursor = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM mensagens WHERE id_conversa=%s", (id_conversa,))
            conn.commit()
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def excluir_conversa(cls, id_conversa):
        conn = None
        cursor = None

        try:
            conn = SQL.conexao()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM conversas WHERE id_conversa=%s", (id_conversa,))
            conn.commit()
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()