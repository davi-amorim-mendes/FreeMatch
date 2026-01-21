from repository.match_repository import MatchRepository
from repository.user_repository import UsuarioRepositorio
from service.user_service import UsuarioService

class MatchService:
    @staticmethod
    def filtrar_interesses(usuario_id):
        usuario_info = UsuarioRepositorio.buscar_usuario(usuario_id)
        interesses_user = MatchRepository.pegar_interesses_user(usuario_id)
        interesses_geral = MatchRepository.validar_interesses(interesses_user)
        usuarios_compativeis = MatchRepository.validar_usuarios(usuario_info, interesses_geral)
        for usuario in usuarios_compativeis:
            usuario["data"] = UsuarioService.calcular_idade(usuario["data"])
            usuario["interesses"] = MatchRepository.pegar_interesses_user(usuario["id"])
            nome_interesses = {1: "Música", 2: "Viagem", 3: "Fotografia", 4: "Cinema", 5: "Leitura", 6: "Esportes", 7: "Arte", 8: "Games", 9: "Natureza", 10: "Vinho"}
            for interesse in usuario["interesses"]:
                id_atual = interesse["interesse_id"]

                interesse["interesse_id"] = nome_interesses.get(id_atual, id_atual)
                print(interesse["interesse_id"])
        return usuarios_compativeis
    
    @staticmethod
    def like(dados, id_usuario):
        resposta = MatchRepository.salvar_like(dados, id_usuario)
        match = MatchRepository.checar_match(id_usuario, dados["id_curtido"])
        if match:
            return "MATCH"
        return "LIKE"
    
    @staticmethod
    def pegar_usuarios_matchs(id):
        matches = MatchRepository.pegar_matchs(id)
        usuarios = []
        for match in matches:
            usuario = UsuarioRepositorio.buscar_usuario(match["usuario_par"])
            usuario.pop("email", None)
            usuario.pop("senha", None)
            idade = UsuarioService.calcular_idade(usuario["data"])
            usuario["data"] = idade
            usuario["datamatch"] = match["data"]
            usuarios.append(usuario)

        return usuarios
        
    @staticmethod
    def qtd_likes(id_usuario):
        qtd_likes = MatchRepository.pegar_likes(id_usuario)
        return qtd_likes
