from pydantic import BaseModel


class AuthResponse(BaseModel):
    name: str
    email: str
    access_token: str
    refresh_token: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
