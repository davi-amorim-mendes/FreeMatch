from model.user_model import Usuario
from repository.user_repository import UsuarioRepositorio
from repository.match_repository import MatchRepository
from repository.msg_repository import MsgRepository
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
    
    @staticmethod
    def excluir_conta(id_usuario):
        try:
            # Busca os matches do usuário
            matches = MatchRepository.pegar_matchs(id_usuario)
            
            # Se houver matches, exclui conversas e mensagens
            if matches:
                conversas = MsgRepository.listar_conversas(matches)
                
                if conversas:
                    for conversa in conversas:
                        # Verifica se a conversa existe antes de tentar excluir
                        if conversa and conversa.get("id_conversa"):
                            MsgRepository.excluir_msg(conversa["id_conversa"])
                            MsgRepository.excluir_conversa(conversa["id_conversa"])
            
            # Exclui matches e likes
            MatchRepository.excluir_match(id_usuario)
            MatchRepository.excluir_like(id_usuario)
            
            # Exclui interesses
            UsuarioRepositorio.excluir_interesse(id_usuario)
            
            # IMPORTANTE: Exclui o usuário por último
            UsuarioRepositorio.excluir_usuario(id_usuario)
            
            return True
            
        except Exception as e:
            print(f"Erro ao excluir conta: {e}")
            return False
