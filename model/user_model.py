import uuid
import bcrypt

class Usuario:
    def __init__(self, nome=None, email=None, senha=None, data=None, genero=None, generoPref=None, relacionamento=None, interesses=None, sobre=None, foto=None, id=None, nivel=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.data = data
        self.genero = genero
        self.generoPref = generoPref
        self.relacionamento = relacionamento
        self.sobre = sobre
        self.interesses = ",".join(interesses) if isinstance(interesses, list) else interesses # TRANSFORMA LISTA EM STRING
        self.foto = foto
        self.nivel = nivel

    def dicionario(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "data": self.data,
            "genero": self.genero,
            "generoPref": self.generoPref,
            "relacionamento": self.relacionamento,
            "sobre": self.sobre,
            "interesses": self.interesses,
            "foto": self.foto,
            "nivel": self.nivel
        }