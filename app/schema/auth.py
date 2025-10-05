from pydantic import BaseModel


class AuthRegister(BaseModel):
    name: str
    email: str
