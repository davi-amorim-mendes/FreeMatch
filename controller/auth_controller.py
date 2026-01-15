from flask import Blueprint, request, jsonify, url_for, render_template, current_app
from service.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/senha-esquecida", methods=["POST"])
def senha_esquecida():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"mensagem": "E-mail obrigatório"}), 400
    
    AuthService.senha_esquecida(email)

    return jsonify({"mensagem": "Se a conta existir, um e-mail de redefinição foi enviado."}), 200

# ROTA PARA O FORMULÁRIO
@auth_bp.route("/redefinir-senha", methods=["GET"])
def redefinir_senha_get():
    token = request.args.get('token')
    if not token:
        return jsonify({"mensagem": "Token não encontrado na URL."}), 400
    
    try:
        current_app.serializer.loads(token, max_age=current_app.token_expiry)
        return render_template("redefinir-senha.html")
    except Exception:
        return jsonify({"message": "Link de redefinição inválido ou expirado."}), 400

# ROTA PARA O ENVIO DO FORMULÁRIO
@auth_bp.route("/redefinir-senha", methods=["POST"])
def redefinir_senha_post():
    token = request.args.get('token')
    if not token:
        return jsonify({"mensagem": "Token não encontrado na URL."}), 400
    
    data = request.get_json()
    nova_senha = data.get("nova_senha")

    resultado = AuthService.validar_e_redefinir_senha(token, nova_senha)

    if resultado["status"] == "success":
        return jsonify({"mensagem": resultado["message"]}), 200
    return jsonify({"mensagem": resultado["message"]}), 400
    
