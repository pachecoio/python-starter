import pytest
from services.user_service import (
    create_user,
    delete_user,
    find_users,
    get_user,
    update_user,
)


def test_create_user(session_factory):
    user = create_user(
        session_factory=session_factory,
        name="Jon Snow",
        email="jon.snow@winterfell.com",
    )
    assert user.id is not None

    user = get_user(session_factory=session_factory, user_id=user.id)
    assert user
    assert user.name == "Jon Snow"


def test_cannot_create_duplicated_user(session_factory):
    params = {"name": "Arya Stark", "email": "arya.start@winterfell.com"}
    create_user(session_factory=session_factory, **params)

    with pytest.raises(Exception):
        create_user(session_factory=session_factory, **params)


def test_update_user(session_factory):
    user = create_user(
        session_factory=session_factory,
        name="Jorah Mormont",
        email="jorah.mormont@bearisland.com",
    )
    assert user.name == "Jorah Mormont"

    updated_user = update_user(
        session_factory=session_factory, user_id=user.id, name="Ser Jorah Mormont"
    )
    assert updated_user.name == "Ser Jorah Mormont"
    assert updated_user.id == user.id
    assert updated_user.created_at == user.created_at
    assert updated_user.updated_at > user.updated_at


@pytest.fixture
def existing_users(session_factory):
    return [
        create_user(
            session_factory=session_factory,
            name="Daenerys Targaryen",
            email="daenerys.targeryan.dragonstone.com",
        ),
        create_user(
            session_factory=session_factory,
            name="Tyrion Lannister",
            email="tyrion.lannister@casterly_rock.com",
        ),
    ]


@pytest.mark.usefixtures("existing_users")
def test_list_users(session_factory):
    users = find_users(session_factory=session_factory)
    assert len(users) == 2

    users_limited_page_1 = find_users(
        session_factory=session_factory, page=1, per_page=1
    )
    assert len(users_limited_page_1) == 1


def test_delete_user(session_factory):
    user = create_user(
        session_factory=session_factory,
        name="Brienne of Tarth",
        email="brienne@tarth.com",
    )
    assert user.deleted_at is None
    delete_user(session_factory=session_factory, user_id=user.id)
    users = find_users(session_factory=session_factory)
    assert len(users) == 0
