from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from service.user_service import UsuarioService
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies, create_refresh_token, set_refresh_cookies
from service.match_service import MatchService
import os
import uuid

user_bp = Blueprint('user', __name__)

@user_bp.route("/")
def landing_page():
    return render_template("landing-page.html")

@user_bp.route("/explorer")
@jwt_required()
def home():
    # ADICIONAR O CÓDIGO DA RECOMENDAÇÃO POR INTERESSES
    # PEGA O ID DO USUÁRIO DO TOKEN
    usuario_id = get_jwt_identity()
    usuarios_compativeis = MatchService.filtrar_interesses(usuario_id)
    return render_template("explorer.html", usuarios=usuarios_compativeis)

@user_bp.route("/matches")
@jwt_required()
def matches():
    usuario_id = get_jwt_identity()
    usuarios_matches = MatchService.pegar_usuarios_matchs(usuario_id)
    return render_template("matches.html", usuarios=usuarios_matches)

@user_bp.route("/chat")
@jwt_required()
def chat():
    return render_template("chat.html")

@user_bp.route("/perfil")
@jwt_required()
def perfil():
    usuario_id = get_jwt_identity()
    # print(usuario["usuario_foto"])
    usuario = UsuarioService.usuario_info(usuario_id)
    return render_template("perfil.html", usuario=usuario)

@user_bp.route("/chat-user")
@jwt_required()
def chat_user():
    return render_template("chat-user.html")

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

    token = create_access_token(
        identity=login["id"],
    )

    refresh_token = create_refresh_token(
        identity=login["id"]
    )

    response = jsonify({"mensagem": "Login realizado com sucesso!", "redirect": True})

    set_access_cookies(response, token)
    set_refresh_cookies(response, refresh_token)

    return response

@user_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"mensagem": "Logout realizado com sucesso!"})
    unset_jwt_cookies(response)
    return response

@user_bp.route("/senha-esquecida")
def senha_esquecida_get():
    return render_template("senha-esquecida.html")

@user_bp.route("/foto-perfil", methods=["POST"])
@jwt_required()
def foto_perfil():
    foto = request.files.get("foto-perfil")

    if not foto or foto.filename == "":
        return jsonify({"mensagem": "Nenhuma imagem enviada"}), 400
    
    if not foto.content_type.startswith('image/'):
        return jsonify({"mensagem": "Arquivo inválido"}), 400
    
    usuario_id = get_jwt_identity()
    url = UsuarioService.atualizar_foto(foto, usuario_id)
    # url = f'/static/img/img_perfil/{nome_foto}'

    return jsonify({"mensagem": "Foto atualizada com sucesso!",
                    "url": url}), 200


@user_bp.route("/editar-sobre", methods=["POST"])
@jwt_required()
def editar_sobre():
    novo_sobre = request.get_json()
    usuario_id = get_jwt_identity()
    UsuarioService.alterar_dados("SOBRE", novo_sobre, usuario_id)
    return jsonify({"mensagem": "Bio alterada com sucesso!!"}), 200

@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    id = get_jwt_identity()

    token = create_access_token(identity=id)

    response = jsonify({"mensagem": "Token renovado"})
    set_access_cookies(response, token)

    return response