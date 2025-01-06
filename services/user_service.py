from datetime import datetime
from config.types import SessionFactory
from models.user import User
from werkzeug.exceptions import NotFound


def get_user(
    session_factory: SessionFactory,
    user_id: int,
):
    with session_factory() as session:
        return session.query(User).filter(
            User.id == user_id,
            User.deleted_at == None
        ).one_or_none()


def create_user(
    session_factory: SessionFactory,
    name: str,
    email: str,
):
    with session_factory() as session:
        user = User(
            name=name,
            email=email,
        )
        session.add(user)
        session.commit()
        return user


def update_user(
    session_factory: SessionFactory,
    user_id: int,
    name: str,
):
    with session_factory() as session:
        user = session.query(User).get(user_id)
        if user is None:
            raise NotFound(f"User with id {user_id} not found")
        user.name = name
        session.commit()
        return user


def find_users(
    session_factory: SessionFactory,
    page: int = 1,
    per_page: int = 10,
):
    with session_factory() as session:
        return (
            session.query(User)
            .filter(User.deleted_at == None)
            .limit(per_page)
            .offset((page - 1) * per_page)
            .all()
        )


def delete_user(
    session_factory: SessionFactory,
    user_id: int,
):
    with session_factory() as session:
        user = session.query(User).get(user_id)
        if user is None:
            raise NotFound(f"User with id {user_id} not found")
        user.deleted_at = datetime.now()
        session.commit()
        return user
