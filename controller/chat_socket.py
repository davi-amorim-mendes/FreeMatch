from flask_socketio import join_room, emit
from extensions.socketio import socketio
from service.chat_service import ChatService

@socketio.on("entrar_conversa")
def entrar_conversa(data):
    join_room(str(data["id_conversa"]))

@socketio.on("enviar_mensagem")
def enviar_mensagem(data):
    ok = ChatService.enviar_mensagem(data["id_conversa"], data["id_remetente"], data["texto"])

    if not ok:
        return
    
    emit("nova_mensagem", {
        "id_remetente": data["id_remetente"],
        "texto": data["texto"]
    }, room=str(data["id_conversa"]))