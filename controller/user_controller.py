from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from service.user_service import UsuarioService
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies

user_bp = Blueprint('user', __name__)

@user_bp.route("/")
def landing_page():
    return render_template("landing-page.html")
@user_bp.route("/home")
@jwt_required()
def home():
    return render_template("home.html")

@user_bp.route("/cadastro", methods=["POST"])
def cadastro_post():
    usuario = request.get_json()

    cadastrar = UsuarioService.cadastro(usuario)

    if cadastrar == "EMAIL EXISTE":
        return jsonify({"mensagem": "E-mail já cadastrado no sistema"}), 409
    if cadastrar == "CADASTRADO":
        return jsonify({"mensagem": f"Cadastro de {usuario['nome']} realizado com sucesso!"}), 201
    
@user_bp.route("/login", methods=["POST"])
def login_post():
    usuario = request.get_json()

    login = UsuarioService.login(usuario)

    if login == "USUARIO NAO EXISTE":
        return jsonify({"mensagem": "E-mail ou senha incorretos"}), 401
    
    data = {
        "usuario_nome": login["nome"],
        "usuario_nivel": login["nivel"]
    }

    token = create_access_token(
        identity=login["id"],
        additional_claims=data
    )

    response = jsonify({"mensagem": "Login realizado com sucesso!", "redirect": True})

    set_access_cookies(response, token)

    return response

@user_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"mensagem": "Logout realizado com sucesso!"})
    unset_jwt_cookies(response)
    return response