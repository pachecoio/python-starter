from flask import Blueprint, request
from werkzeug.exceptions import NotFound
from config.database import get_session
from schemas.user_schema import CreateUserSchema, UpdateUserSchema, UserSchema
from services import user_service
from utils.request_utils import marshal_with

bp = Blueprint("user", __name__)


@bp.route("/api/users", methods=["GET"])
def find_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    users = user_service.find_users(get_session, page=page, per_page=per_page)

    serialized_users = [UserSchema.model_validate(user).model_dump() for user in users]
    return serialized_users, 200


@bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user(get_session, user_id)
    if user is None:
        return {"message": "User not found"}, 404
    serialized_user = UserSchema.model_validate(user)
    return serialized_user.model_dump(), 200


@bp.route("/api/users", methods=["POST"])
@marshal_with(CreateUserSchema)
def create_user(entity: CreateUserSchema):
    user = user_service.create_user(get_session, **entity.model_dump())

    serialized_user = UserSchema.model_validate(user)
    return serialized_user.model_dump(), 201


@bp.route("/api/users/<int:user_id>", methods=["PUT"])
@marshal_with(UpdateUserSchema)
def update_user(entity: UpdateUserSchema, user_id: int):
    try:
        user = user_service.update_user(get_session, user_id, name=entity.name)
    except NotFound:
        return {"message": "User not found"}, 404
    except Exception as e:
        return {"message": str(e)}, 500
    serialized_user = UserSchema.model_validate(user)
    return serialized_user.model_dump(), 200


@bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user_service.delete_user(get_session, user_id)
    except NotFound:
        return {"message": "User not found"}, 404
    except Exception as e:
        return {"message": str(e)}, 500
    return {}, 204

