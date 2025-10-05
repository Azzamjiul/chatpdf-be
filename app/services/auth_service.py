from datetime import datetime, timedelta
from typing import Optional

import jwt
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.extended_settings import app_settings
from app.core.settings import settings
from app.database.models import User
from app.schema.auth import AuthResponse

oauth = OAuth()
oauth.register(
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
    name="google",
)


async def authorize(request: Request, db: Session) -> Optional[AuthResponse]:
    """Handle Google OIDC authorization and create or return a User.

    Notes:
    - `oauth.google.authorize_access_token` is async and must be awaited.
    - The DB session is a synchronous SQLModel/SQLAlchemy Session, so do not await
      its methods. Use them directly.
    """
    data = await oauth.google.authorize_access_token(request)
    userinfo = dict(data.get("userinfo", {}))

    # Try to find existing user (synchronous session API)
    existing_user = db.query(User).filter(User.email == userinfo.get("email")).first()

    if not existing_user:
        new_user = User(
            name=userinfo.get("name") or "",
            email=userinfo.get("email") or "",
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        existing_user = new_user

    # generate jwt token here
    access_token = create_access_token(data={"sub": str(existing_user.id), "email": existing_user.email})

    return AuthResponse(
        name=existing_user.name,
        email=existing_user.email,
        access_token=access_token,
    )


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=app_settings.JWT_TOKEN_EXPIRE)):
    to_encode = data.copy()
    expired_time = datetime.now() + expires_delta
    to_encode.update({"exp": expired_time})
    encoded_jwt = jwt.encode(to_encode, app_settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt
