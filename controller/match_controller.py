from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from service.user_service import UsuarioService
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, get_jwt
from service.match_service import MatchService

match_bp = Blueprint('match', __name__)

@match_bp.route("/like", methods=["POST"])
@jwt_required()
def like():
    dados = request.get_json()
    id_usuario = get_jwt_identity()
    resposta = MatchService.like(dados, id_usuario)
    print(resposta)
    if resposta == "MATCH":
        return jsonify({"mensagem": "MATCH!"}), 200
    else:
        return jsonify({"mensagem": "LIKE"}), 200