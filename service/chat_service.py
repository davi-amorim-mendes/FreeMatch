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

        for i, conversa in enumerate(conversas):
            if conversa:
                ultima_msg = MsgRepository.obter_ultima_mensagem(conversa['id_conversa'])
                conversas[i]['ultima_mensagem'] = ultima_msg

        return [matches, conversas]
    
    @staticmethod
    def carregar_mensagens(id_conversa):
        return MsgRepository.listar_mensagens(id_conversa)
    
    @staticmethod
    def qtd_msg(id_usuario):
        matches = MatchRepository.pegar_matchs(id_usuario)
        conversas = MsgRepository.listar_conversas(matches)
        mensagens = MsgRepository.qtd_msg(conversas)
        qtd_msg = 0

        for mensagem in mensagens:
            qtd_msg += mensagem["total"]

        return qtd_msg

