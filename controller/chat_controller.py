from flask_socketio import Namespace, emit, disconnect, join_room
from flask import request, g
from flask_jwt_extended import decode_token
from repository.msg_repository import MsgRepository

class ChatNamespace(Namespace):
    def on_connect(self):
        token = request.cookies.get("access_token_cookie")
        if not token:
            disconnect()
            return

        try:
            payload = decode_token(token)
            g.usuario_id = payload["sub"]

            print(f"USUÁRIO {g.usuario_id} CONECTADO AO CHAT")
        except:
            disconnect()

    def on_disconnect(self):
        print("CLIENTE DESCONECTADO DO CHAT")

    def on_entrar_conversa(self, data):
        join_room(str(data["id_conversa"]))

    def on_enviar_mensagem(self, data):
        id_usuario = g.usuario_id
        id_conversa = data["id_conversa"]
        texto = data["texto"]

        MsgRepository.salvar_mensagem(id_conversa, id_usuario, texto)

        emit(
            "receive_message",
            {
                "id_remetente": id_usuario,
                "texto": texto
            },
            room=str(id_conversa)
        )