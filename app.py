from flask import Flask, redirect, url_for
from controller.user_controller import user_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("SESSION_KEY")
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_SAMESITE"] = "None"
serializer = URLSafeTimedSerializer(os.getenv("RESET_PASSWORD_KEY"))

CORS(app, supports_credentials=True, allow_headers=["Authorization", "Content-Type"])
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


app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.serializer = serializer
    with app.app_context():
        app.run(debug=True)