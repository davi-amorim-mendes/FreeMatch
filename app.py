from flask import Flask, redirect, url_for
from controller.user_controller import user_bp
from controller.auth_controller import auth_bp
from controller.match_controller import match_bp
from controller.chat_controller import ChatNamespace
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta
from flask_socketio import SocketIO

load_dotenv()

RESET_PASSWORD_KEY = os.getenv("RESET_PASSWORD_KEY")
if not RESET_PASSWORD_KEY:
    raise ValueError("A variável 'RESET_PASSWORD_KEY' não está definida")

serializer = URLSafeTimedSerializer(os.getenv("RESET_PASSWORD_KEY"))
TOKEN_EXPIRY_SECONDS = 3600 # O TOKEN EXPIRA EM 1 HORA PARA REDEFINIR SENHA

app = Flask(__name__)

# DETECTAR AMBIENTE
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.config["JWT_SECRET_KEY"] = os.getenv("SESSION_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=17)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_SECURE"] = IS_PRODUCTION
app.config["JWT_COOKIE_SAMESITE"] = "None" if IS_PRODUCTION else "Lax"
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"

socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS, cookie=True, transports=['websocket', 'polling'], async_mode='threading', logger=True, engineio_logger=True, ping_interval=25, ping_timeout=60)

CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True, allow_headers=["Authorization", "Content-Type"])
jwt = JWTManager(app)

@jwt.unauthorized_loader
def sem_token(error):
    return redirect(url_for("user.landing_page"))

@jwt.invalid_token_loader
def token_invalido(error):
    return redirect(url_for("user.landing_page"))

@jwt.expired_token_loader
def token_expirado(jwt_header, jwt_payload):
    return redirect(url_for("user.landing_page"))

from controller.chat_socket import init_socketio
init_socketio(socketio)

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(match_bp)

app.serializer = serializer
app.token_expiry = TOKEN_EXPIRY_SECONDS

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, debug=False, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)