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

    return {"users": users}


