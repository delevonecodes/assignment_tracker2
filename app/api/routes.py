from flask import Blueprint, request, jsonify
from functools import wraps
import os
from app import db
from app.models import User, LinkCode
 
api = Blueprint('api', __name__)

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != os.environ.get("BOT_API_KEY"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

@api.route("/link/start", methods=["POST"])
@require_api_key
def link_start():
    data = request.get_json(silent=True) or {}
    discord_id = data.get("discord_id")
    if not discord_id:
        return jsonify({"error": "discord_id is required"}), 400
    discord_id = str(discord_id)
 
    existing_user = User.query.filter_by(discord_id=discord_id).first()
    if existing_user:
        return jsonify({"error": "already_linked", "username": existing_user.username}), 409
 
    LinkCode.query.filter_by(discord_id=discord_id).delete()
 
    code = LinkCode.generate_code()
    while LinkCode.query.filter_by(code=code).first():
        code = LinkCode.generate_code()
 
    link_code = LinkCode(code=code, discord_id=discord_id, expires_at=LinkCode.new_expiry())
    db.session.add(link_code)
    db.session.commit()
 
    return jsonify({"code": code, "expires_in": 600}), 200
 
 
@api.route("/unlink", methods=["POST"])
@require_api_key
def unlink():
    data = request.get_json(silent=True) or {}
    discord_id = data.get("discord_id")
    if not discord_id:
        return jsonify({"error": "discord_id is required"}), 400
 
    user = User.query.filter_by(discord_id=str(discord_id)).first()
    if not user:
        return jsonify({"error": "not_linked"}), 404
 
    user.discord_id = None
    db.session.commit()
    return jsonify({"unlinked": True}), 200
 
 
@api.route("/link/status", methods=["GET"])
@require_api_key
def link_status():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return jsonify({"error": "discord_id is required"}), 400
 
    user = User.query.filter_by(discord_id=str(discord_id)).first()
    if user:
        return jsonify({"linked": True, "username": user.username}), 200
    return jsonify({"linked": False}), 200