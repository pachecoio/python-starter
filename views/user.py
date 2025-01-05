from flask import Blueprint, request
from config.database import get_session
from services import user_service

bp = Blueprint('user', __name__)

@bp.route("/api/users", methods=["GET"])
def find_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    users = user_service.find_users(
        get_session,
        page=page,
        per_page=per_page
    )

    return users


@bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = user_service.create_user(
        get_session,
        **data
    )

    return {
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }, 201



