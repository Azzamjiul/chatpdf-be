from sqlmodel import Field

from app.core.models import BaseModel


class User(BaseModel, table=True):
    id: str = Field(primary_key=True, index=True, nullable=False, max_length=24)
    name: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, max_length=255)
