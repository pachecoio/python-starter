import pytest
from services.user_service import create_user


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


def test_get_user_api(client):
    response = client.post("/api/users", json={
        "name": "Jorah Mormont",
        "email": "jorah.mormont@bear_island.com",
    })
    assert response.status_code == 201

    id = response.json["id"]
    response = client.get(f"/api/users/{id}")
    assert response.status_code == 200
    assert response.json["name"] == "Jorah Mormont"
    assert response.json["email"] == "jorah.mormont@bear_island.com"

    response = client.get("/api/users/999")
    assert response.status_code == 404

def test_update_user_api(client):
    response = client.post("/api/users", json={
        "name": "Samwell Tarly",
        "email": "samwell.tarly@castle_black.com",
    })
    assert response.status_code == 201

    id = response.json["id"]
    response = client.put(f"/api/users/{id}", json={
        "name": "Daenerys Stormborn",
    })
    assert response.status_code == 200
    assert response.json["name"] == "Daenerys Stormborn"

    response = client.put("/api/users/999", json={
        "name": "Tyrion Lannister",
    })
    assert response.status_code == 404

def test_delete_user_api(client):
    response = client.post("/api/users", json={
        "name": "Bran Stark",
        "email": "bran.start@winterfell.com",
    })
    id = response.json["id"]

    response = client.delete(f"/api/users/{id}")
    assert response.status_code == 204

    response = client.get(f"/api/users/{id}")
    assert response.status_code == 404
