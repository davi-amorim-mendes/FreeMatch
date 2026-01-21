from flask_socketio import join_room, emit, disconnect
from flask import request
from flask_jwt_extended import decode_token
from service.chat_service import ChatService
from datetime import datetime

def init_socketio(socketio):
    @socketio.on('connect')
    def handle_connect():
        token = request.cookies.get("access_token_cookie")
        if not token:
            print("Token não encontrado, desconectando...")
            disconnect()
            return False
        
        try:
            payload = decode_token(token)
            usuario_id = payload["sub"]
            print(f"Usuário {usuario_id} conectado ao chat")
            return True
        except Exception as e:
            print(f"Erro ao decodificar token: {e}")
            disconnect()
            return False
        
    @socketio.on("disconnect")
    def handle_disconnect():
        print("Cliente desconectado do chat")

    @socketio.on("entrar_conversa")
    def entrar_conversa(data):
        token = request.cookies.get("access_token_cookie")
        if not token:
            disconnect()
            return
        
        try:
            payload = decode_token(token)
            id_conversa = data.get("id_conversa")

            if id_conversa:
                join_room(str(id_conversa))
                print(f"Usuário entrou na conversa: {id_conversa}")

                # ENVIA HISTÓRICO DE MENSAGENS
                mensagens = ChatService.carregar_mensagens(id_conversa)
                emit('historico_mensagens', {'mensagens': mensagens})
        except Exception as e:
            print(f"Erro ao entrar na conversa: {e}")

    @socketio.on("enviar_mensagem")
    def enviar_mensagem(data):
        token = request.cookies.get("access_token_cookie")
        if not token:
            disconnect()
            return

        try:
            payload = decode_token(token)
            id_remetente = payload["sub"]
            id_conversa = data.get("id_conversa")
            texto = data.get("texto")

            if not texto or not texto.strip():
                print("Mensagem vazia, ignorando...")
                return

            ok = ChatService.enviar_mensagem(id_conversa, id_remetente, texto)

            if ok:
                print(f"Mensagem salva, emitindo pela sala {id_conversa}")
                emit("nova_mensagem", {
                    "id_remetente": id_remetente,
                    "id_conversa": id_conversa,
                    "texto": texto,
                    "criada_em": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }, room=str(id_conversa))
                print("Mensagem emitida com sucesso!")
            else:
                print("Falha ao salvar mensagem")
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            import traceback
            traceback.print_exc()
    print("Eventos do SocketIo registrados!")