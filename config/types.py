from collections.abc import Callable
from sqlalchemy import orm


type SessionFactory = Callable[[], orm.Session]
