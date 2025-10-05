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
    refresh_token = create_refresh_token(data={"sub": str(existing_user.id), "email": existing_user.email})

    return AuthResponse(
        name=existing_user.name,
        email=existing_user.email,
        access_token=access_token,
        refresh_token=refresh_token,
    )


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=app_settings.JWT_TOKEN_EXPIRE)):
    to_encode = data.copy()
    # mark this as an access token
    to_encode.update({"token_type": "access"})
    expired_time = datetime.now() + expires_delta
    to_encode.update({"exp": expired_time})
    encoded_jwt = jwt.encode(to_encode, app_settings.JWT_SECRET, algorithm=app_settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=app_settings.JWT_REFRESH_TOKEN_EXPIRE)
):
    """Create a refresh token with a longer expiry.

    This mirrors create_access_token but uses the refresh expiry setting.
    """
    to_encode = data.copy()
    # mark this as a refresh token
    to_encode.update({"token_type": "refresh"})
    expired_time = datetime.now() + expires_delta
    to_encode.update({"exp": expired_time})
    encoded_jwt = jwt.encode(to_encode, app_settings.JWT_SECRET, algorithm=app_settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> dict:
    """Verify and decode a refresh token. Returns payload if valid, raises jwt exceptions otherwise."""
    payload = jwt.decode(token, app_settings.JWT_SECRET, algorithms=[app_settings.JWT_ALGORITHM])
    # ensure token type
    if payload.get("token_type") != "refresh":
        raise jwt.InvalidTokenError("Not a refresh token")
    return payload


def refresh_access_token(refresh_token: str, rotate: bool = False) -> tuple[str, str | None]:
    """Given a refresh token, validate it and return (access_token, refresh_token_or_none).

    If rotate is True, return a new refresh token as well. Otherwise return None for refresh token.
    """
    payload = verify_refresh_token(refresh_token)
    user_data = {"sub": payload.get("sub"), "email": payload.get("email")}
    new_access = create_access_token(data=user_data)
    new_refresh = None
    if rotate:
        new_refresh = create_refresh_token(data=user_data)
    return new_access, new_refresh
