from flask_socketio import join_room, emit, disconnect
from flask import request
from flask_jwt_extended import decode_token
from service.chat_service import ChatService
from datetime import datetime

def init_socketio(socketio):
    @socketio.on('connect')
    def handle_connect():
        """
        Conexão inicial - NÃO deve fazer operações pesadas aqui
        """
        try:
            print("🔌 Nova tentativa de conexão")
            
            # Verificação básica do token (não bloqueia)
            token = request.cookies.get("access_token_cookie")
            
            if not token:
                print("⚠️ Token não encontrado, mas permitindo conexão temporária")
                # IMPORTANTE: Retornar True para permitir conexão
                # A verificação real será feita nos eventos específicos
                return True
            
            try:
                payload = decode_token(token)
                usuario_id = payload.get("sub")
                print(f"✅ Usuário {usuario_id} conectado ao chat")
                return True
            except Exception as e:
                print(f"⚠️ Erro ao decodificar token (permitindo conexão): {e}")
                # Mesmo com erro no token, permite conectar
                # O erro será tratado nos eventos específicos
                return True
                
        except Exception as e:
            print(f"❌ Erro crítico na conexão: {e}")
            import traceback
            traceback.print_exc()
            # Mesmo com erro, tenta permitir conexão
            return True
        
    @socketio.on("disconnect")
    def handle_disconnect():
        print("🔴 Cliente desconectado do chat")

    @socketio.on("entrar_conversa")
    def entrar_conversa(data):
        """
        Evento para entrar em uma conversa específica
        """
        try:
            print(f"📥 Recebido evento 'entrar_conversa': {data}")
            
            token = request.cookies.get("access_token_cookie")
            if not token:
                print("❌ Token não encontrado em 'entrar_conversa'")
                emit('erro', {'mensagem': 'Não autenticado'})
                return
            
            # Decodifica token
            try:
                payload = decode_token(token)
                usuario_id = payload.get("sub")
            except Exception as e:
                print(f"❌ Erro ao decodificar token: {e}")
                emit('erro', {'mensagem': 'Token inválido'})
                return
            
            # Pega ID da conversa
            id_conversa = data.get("id_conversa")
            
            if not id_conversa:
                print("❌ ID da conversa não fornecido")
                emit('erro', {'mensagem': 'ID da conversa inválido'})
                return

            # Entra na sala
            join_room(str(id_conversa))
            print(f"✅ Usuário {usuario_id} entrou na conversa: {id_conversa}")

            # Carrega e envia histórico de mensagens
            try:
                print(f"📜 Carregando histórico da conversa {id_conversa}...")
                mensagens = ChatService.carregar_mensagens(id_conversa)
                print(f"✅ {len(mensagens) if mensagens else 0} mensagens carregadas")
                
                emit('historico_mensagens', {
                    'mensagens': mensagens if mensagens else []
                })
                print("✅ Histórico enviado com sucesso")
                
            except Exception as e:
                print(f"❌ Erro ao carregar mensagens: {e}")
                import traceback
                traceback.print_exc()
                # Envia histórico vazio em caso de erro
                emit('historico_mensagens', {'mensagens': []})
                
        except Exception as e:
            print(f"❌ Erro geral em 'entrar_conversa': {e}")
            import traceback
            traceback.print_exc()
            emit('erro', {'mensagem': 'Erro ao entrar na conversa'})

    @socketio.on("enviar_mensagem")
    def enviar_mensagem(data):
        """
        Evento para enviar uma nova mensagem
        """
        try:
            print(f"📤 Recebido evento 'enviar_mensagem': {data}")
            
            token = request.cookies.get("access_token_cookie")
            if not token:
                print("❌ Token não encontrado em 'enviar_mensagem'")
                emit('erro', {'mensagem': 'Não autenticado'})
                return

            # Decodifica token
            try:
                payload = decode_token(token)
                id_remetente = payload.get("sub")
            except Exception as e:
                print(f"❌ Erro ao decodificar token: {e}")
                emit('erro', {'mensagem': 'Token inválido'})
                return
            
            # Valida dados
            id_conversa = data.get("id_conversa")
            texto = data.get("texto")

            if not texto or not texto.strip():
                print("⚠️ Mensagem vazia, ignorando...")
                return
            
            if not id_conversa:
                print("❌ ID da conversa não fornecido")
                return

            # Salva mensagem no banco
            try:
                print(f"💾 Salvando mensagem na conversa {id_conversa}...")
                ok = ChatService.enviar_mensagem(id_conversa, id_remetente, texto)

                if ok:
                    print(f"✅ Mensagem salva, emitindo para sala {id_conversa}")
                    
                    # Emite para todos na sala
                    emit("nova_mensagem", {
                        "id_remetente": id_remetente,
                        "id_conversa": id_conversa,
                        "texto": texto,
                        "criada_em": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }, room=str(id_conversa))
                    
                    print("✅ Mensagem emitida com sucesso!")
                else:
                    print("❌ Falha ao salvar mensagem no banco")
                    emit('erro', {'mensagem': 'Erro ao salvar mensagem'})
                    
            except Exception as e:
                print(f"❌ Erro ao salvar mensagem: {e}")
                import traceback
                traceback.print_exc()
                emit('erro', {'mensagem': 'Erro ao processar mensagem'})
                
        except Exception as e:
            print(f"❌ Erro geral em 'enviar_mensagem': {e}")
            import traceback
            traceback.print_exc()
            emit('erro', {'mensagem': 'Erro ao enviar mensagem'})
    
    print("✅ Eventos do SocketIO registrados com sucesso!")