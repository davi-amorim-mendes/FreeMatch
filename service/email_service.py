import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    def enviar_email_recuperacao(usuario_email, link_redefinir):
        smtp_server = "smtp.gmail.com" # SMTP COM GMAIL
        smtp_port = 587
        sender_email = os.getenv("SMTP_EMAIL")
        sender_password = os.getenv("SMTP_PASSWORD")

        if not sender_email or not sender_password:
            print("Erro: credenciais SMTP ausentes no .env")
            return False
        
        msg_body = f"""
                    Olá,
                    Você solicitou uma redefinição de senha. Clique no link abaixo para continuar:
                    {link_redefinir}

                    O link irá expirar em 1 hora.

                    Se você não solicitou isso, ignore este e-mail.
                    """
        msg = MIMEText(msg_body, 'plain', 'utf-8')
        msg['Subject'] = "Link de Redefinição de Senha"
        msg['From'] = sender_email
        msg['To'] = usuario_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, usuario_email, msg.as_string())
            return True
        except Exception as e:
            print(f"Erro ao enviar o e-mail para {usuario_email}: {e}")
            return False