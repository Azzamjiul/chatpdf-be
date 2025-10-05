from pydantic import BaseModel


class AuthResponse(BaseModel):
    name: str
    email: str
    access_token: str
    refresh_token: str | None = None
