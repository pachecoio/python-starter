from flask import Blueprint, request
from config.database import get_session
from schemas.user_schema import CreateUserSchema, UserSchema
from services import user_service
from utils.request_utils import marshal_with

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
@marshal_with(CreateUserSchema)
def create_user(entity: CreateUserSchema):
    user = user_service.create_user(
        get_session,
        **entity.model_dump()
    )

    serialized = UserSchema.model_validate(user)
    return serialized.model_dump(), 201



