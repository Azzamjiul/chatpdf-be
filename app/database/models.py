from sqlmodel import Field

from app.core.models import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    # Inherit `id` from BaseModel so the default_factory (generate_id)
    # is applied and a string primary key is generated in Python prior to flush.
    name: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, max_length=255)
