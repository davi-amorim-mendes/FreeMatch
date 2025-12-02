from model.user_model import Usuario
from repository.user_repository import UsuarioRepositorio

class UsuarioService:
    @staticmethod
    def cadastro(dados):
        usuario = Usuario(**dados)
        if UsuarioRepositorio.email_existente(usuario):
            return "EMAIL EXISTE"
        if UsuarioRepositorio.adicionar(usuario):
            return "CADASTRADO"
        
    @staticmethod
    def login(dados):
        usuario = Usuario(**dados)
        if UsuarioRepositorio.email_existente(usuario):
            usuario_autenticado = UsuarioRepositorio.usuario_existente(dados["email"], dados["senha"])
            if usuario_autenticado:
                return usuario_autenticado
        return "USUARIO NAO EXISTE"