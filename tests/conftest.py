import pytest
from sqlalchemy import orm
from sqlalchemy import create_engine

from config import database


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    session_factory = orm.sessionmaker(bind=engine, expire_on_commit=False)
    database.create_all(engine)
    yield session_factory
