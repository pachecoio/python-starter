from collections.abc import Callable
import os

from sqlalchemy import Engine, create_engine, orm


def get_database_uri() -> str:
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = 5432
    username = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    db_name = os.environ.get("POSTGRES_DB", "postgres")
    return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"


DEFAULT_ENGINE = create_engine(get_database_uri())

get_session = orm.sessionmaker(bind=DEFAULT_ENGINE)

reg = orm.registry()

type SessionFactory = Callable[[], orm.Session]

def create_all(engine: Engine) -> None:
    reg.metadata.create_all(engine)

def drop_all(engine: Engine) -> None:
    reg.metadata.drop_all(engine)
