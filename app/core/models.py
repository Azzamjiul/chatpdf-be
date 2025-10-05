from datetime import datetime

from sqlmodel import Field, SQLModel

from app.utils.generate_ids import generate_id


class BaseModel(SQLModel):
    # Use a generated string id (24 chars). This ensures the id is
    # available on the Python side before flush so SQLAlchemy won't
    # complain about a NULL identity key.
    id: str = Field(default_factory=generate_id, primary_key=True, max_length=24)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)
