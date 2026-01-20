from repository.msg_repository import MsgRepository
from repository.match_repository import MatchRepository
from service.match_service import MatchService

class ChatService:
    @staticmethod
    def enviar_mensagem(id_conversa, id_remetente, texto):
        if not texto.strip():
            return False
        
        MsgRepository.salvar_mensagem(id_conversa, id_remetente, texto)
        return True
    
    @staticmethod
    def carregar_conversas(id_usuario):
        matches_id = MatchRepository.pegar_matchs(id_usuario)
        conversas = MsgRepository.listar_conversas(matches_id)
        matches = MatchService.pegar_usuarios_matchs(id_usuario)

        return [matches, conversas]