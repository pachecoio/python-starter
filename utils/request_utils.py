from functools import wraps
from typing import Any, Type
from flask import request
from pydantic import BaseModel


def _marshal(request: dict, model: Type[BaseModel], handler):
    """Marshal a request json data into a pydantic model.

    Attempts to parse a request.json into a pydantic model
    and returns the model instance.
    If it fails, it returns a 400 error with a message.
    """

    try:
        entity = model(**request)
        return handler(entity)
    except Exception as e:
        return {"message": str(e)}, 400


def marshal_with(model: Type[BaseModel]):
    def inner(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return _marshal(
                request.get_json(),
                model,
                lambda entity: f(entity, *args, **kwargs)
            )
        return decorated_function
    return inner


def _serialize(response: Any, model: Type[BaseModel]):
    """Serialize a response dict into a pydantic model.

    Attempts to parse a response dict into a pydantic model
    and returns the model instance.
    If it fails, it returns a 500 error with a message.
    """

    try:
        return model.model_validate(response).model_dump()
    except Exception as e:
        return {"message": str(e)}, 500

def serialize_with(model: Type[BaseModel]):
    def inner(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response, status = f(*args, **kwargs)
            return _serialize(response, model), status
        return decorated_function
    return inner
