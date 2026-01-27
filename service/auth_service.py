from flask import current_app
from service.email_service import EmailService
from repository.user_repository import UsuarioRepositorio
from model.user_model import Usuario
from itsdangerous import SignatureExpired, BadTimeSignature
import os
from dotenv import load_dotenv

load_dotenv()
class AuthService:
    @staticmethod
    def senha_esquecida(email):
        usuario = UsuarioRepositorio.email_existente(email)

        if not usuario:
            return True # CASO FALHE, RETORNARÁ FALSO, PARA EVITAR VAZAR SE O EMAIL EXISTE NO BANCO DE DADOS
        
        # GERA O TOKEN DO EMAIL
        token = current_app.serializer.dumps(usuario["id"])

        # CRIA O LINK DE REDEFINIR SENHA
        base_url = os.getenv("BASE_URL", f"http://{current_app.config.get('SERVER_NAME', 'localhost:5000')}")
        reset_link = f"{base_url}/redefinir-senha?token={token}"

        # ENVIA O EMAIL
        return EmailService.enviar_email_recuperacao(email, reset_link)
    
    @staticmethod
    def validar_e_redefinir_senha(token, nova_senha):
        try:
            usuario_id = current_app.serializer.loads(
                token,
                max_age=current_app.token_expiry
            )
        except SignatureExpired:
            return {"status": "error", "message": "O link de expirou."}
        except BadTimeSignature:
            return {"status": "error", "message": "Link inválido"}
        
        if UsuarioRepositorio.alterar_senha(usuario_id, nova_senha):
            return {"status": "success", "message": "Senha redefinida com sucesso!"}
        return {"status": "error", "message": "Usuário não encontrado ou erro de DB."}