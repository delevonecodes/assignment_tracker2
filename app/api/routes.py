from flask import Blueprint, request, jsonify
from functools import wraps
from datetime import datetime
import os
from app import db
from app.models import User, LinkCode, Assignment
 
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

@api.route("/add-assignment", methods=["POST"])
@require_api_key
def add_assignment():
    data = request.get_json(silent=True) or {}
    discord_id = data.get("discord_id")
    if not discord_id:
        return jsonify({"error": "discord_id is required"}), 400
    user = User.query.filter_by(discord_id=str(discord_id)).first()
    if not user:
        return jsonify({"error": "not_linked"}), 404

    name = data.get("assignment_name")
    course = data.get("course")
    priority = data.get("priority")
    due_date = data.get("due_date")
    notes = data.get("description")

    if not name or not course or not due_date:
        return jsonify({"error": "missing_fields"}), 400

    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"error": "invalid_due_date"}), 400

    try:
        assignment = Assignment(
            name=name,
            course=course,
            priority=priority,
            due_date=due_date_obj,
            notes=notes,
            student=user.id
        )
        db.session.add(assignment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating assignment via API: {e}")
        return jsonify({"error": "server_error"}), 500

    return jsonify({
        "id": assignment.id,
        "name": assignment.name,
        "course": assignment.course,
        "priority": assignment.priority,
        "due_date": assignment.due_date.isoformat()
    }), 201