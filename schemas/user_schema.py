from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """
    The `model_config` attribute allows you to parse this schema
    from an arbitrary class by simply using Schema.model_validate(obj)

    Example:
    ```
    serialized_user = UserSchema.model_validate(user)
    ```
    """

    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class CreateUserSchema(BaseModel):
    name: str
    email: str
