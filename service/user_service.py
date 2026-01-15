from model.user_model import Usuario
from repository.user_repository import UsuarioRepositorio
from repository.match_repository import MatchRepository
from datetime import date, datetime
class UsuarioService:
    @staticmethod
    def cadastro(dados):
        interesses = dados["interesses"]
        usuario = Usuario(**dados)
        if UsuarioRepositorio.email_existente_class(usuario):
            return "EMAIL EXISTE"
        if UsuarioRepositorio.adicionar(interesses, usuario):
            return "CADASTRADO"
        
    @staticmethod
    def login(dados):
        usuario = UsuarioRepositorio.email_existente(dados["email"])
        if usuario != False:
            usuario_autenticado = UsuarioRepositorio.usuario_existente(dados["email"], dados["senha"])
            if usuario_autenticado:
                return usuario_autenticado
        return "USUARIO NAO EXISTE"
    
    @staticmethod
    def atualizar_foto(foto, usuario_id):
        url = UsuarioRepositorio.salvar_foto_local(foto)
        UsuarioRepositorio.salvar_foto_db(url, usuario_id)
        return url
    
    @staticmethod
    def usuario_info(id):
        usuario = UsuarioRepositorio.buscar_usuario(id)
        # if usuario == False:
        #     return False
        usuario.pop("email", None)
        usuario.pop("senha", None)
        usuario.pop("id", None)
        idade = UsuarioService.calcular_idade(usuario["data"])
        usuario["data"] = idade
        interesses = MatchRepository.pegar_interesses_user(id)
        nome_interesses = {1: "Música", 2: "Viagem", 3: "Fotografia", 4: "Cinema", 5: "Leitura", 6: "Esportes", 7: "Arte", 8: "Games", 9: "Natureza", 10: "Vinho"}

        for interesse in interesses:
            id_atual = interesse["interesse_id"]

            interesse["interesse_id"] = nome_interesses.get(id_atual, id_atual)
            # print(interesse["interesse_id"])

        return [usuario, interesses]
        
    @staticmethod
    def calcular_idade(data):
        data = datetime.strptime(data, "%Y-%m-%d")
        hoje = date.today()
        idade = hoje.year - data.year

        aniversario = (hoje.month, hoje.day) < (data.month, data.day)

        if aniversario:
            idade -= 1

        return idade
    
    @staticmethod
    def alterar_dados(tipo, dado, id):
        if tipo == "SOBRE":
            UsuarioRepositorio.editar_sobre(dado, id)

        return