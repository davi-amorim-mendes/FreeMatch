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

# ============= CONFIGURAÇÃO OTIMIZADA DO SOCKETIO =============
print("🔧 Configurando SocketIO...")
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",  # Permite todas as origens
    async_mode='threading',     # Modo assíncrono compatível com Render
    logger=True,                # Ativa logs para debug
    engineio_logger=True,       # Ativa logs do engine.io
    ping_timeout=120,           # Aumenta timeout para 120s (era 60)
    ping_interval=25,           # Intervalo de ping
    max_http_buffer_size=1e8,   # Buffer maior
    transports=['polling', 'websocket'],  # Polling primeiro
    # Configurações adicionais para evitar timeout
    allow_upgrades=True,        # Permite upgrade de polling para websocket
    http_compression=True,      # Compressão HTTP
    compression_threshold=1024, # Limite de compressão
    cookie=False,               # Desabilita cookie do Socket.IO (usamos JWT)
    manage_session=False        # Não gerencia sessão automaticamente
)
print("✅ SocketIO configurado!")

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

# Inicializa eventos do Socket.IO
print("🔌 Inicializando eventos do SocketIO...")
from controller.chat_socket import init_socketio
init_socketio(socketio)
print("✅ Eventos registrados!")

# Registra blueprints
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(match_bp)

app.serializer = serializer
app.token_expiry = TOKEN_EXPIRY_SECONDS

# Rota de health check para o Render
@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Iniciando servidor na porta {port}...")
    print(f"🌍 Ambiente: {'PRODUÇÃO' if IS_PRODUCTION else 'DESENVOLVIMENTO'}")
    print(f"🔗 CORS permitido: {ALLOWED_ORIGINS}")
    
    # Configuração adequada para Render
    socketio.run(
        app, 
        debug=False, 
        host='0.0.0.0', 
        port=port,
        allow_unsafe_werkzeug=True,  # Necessário para algumas versões
        log_output=True              # Exibe logs
    )