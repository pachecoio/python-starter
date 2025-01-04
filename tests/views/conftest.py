import pytest

@pytest.fixture(autouse=True)
def mock_session_factory(session_factory, mocker):
    return mocker.patch(
        "config.database.get_session",
        return_value=session_factory()
    )


@pytest.fixture
def test_app():
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client
