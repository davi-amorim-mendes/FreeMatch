from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from service.user_service import UsuarioService
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, get_jwt
from service.match_service import MatchService

match_bp = Blueprint('match', __name__)

@match_bp.route("/like", methods=["POST"])
def like():
    print("LIKE")
    return jsonify({"mensagem": "asfasfa"})