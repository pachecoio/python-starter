import pytest
from services.user_service import create_user


@pytest.fixture
def existing_users(session_factory):
    return [
        create_user(
            session_factory=session_factory,
            name="Daenerys Targaryen",
            email="daenerys.targeryan.dragonstone.com"
        ),
        create_user(
            session_factory=session_factory,
            name="Tyrion Lannister",
            email="tyrion.lannister@casterly_rock.com"
        ),
    ]


@pytest.mark.usefixtures("existing_users")
def test_find_users_api(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json) == 2

    response = client.get("/api/users?page=1&per_page=1")
    assert response.status_code == 200
    assert len(response.json) == 1

    response = client.get("/api/users?page=2")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_create_user_api(client):
    data = {
        "name": "Jon Snow",
        "email": "jon.snow@winterfell.com",
    }
    response = client.post("/api/users", json=data)
    assert response.status_code == 201
    assert response.json["name"] == "Jon Snow"
    assert response.json["email"] == "jon.snow@winterfell.com"
