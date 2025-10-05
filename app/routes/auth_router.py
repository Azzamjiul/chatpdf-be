from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database.engine import db_session
from app.schema.auth import RefreshRequest, RefreshResponse
from app.services import auth_service

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/google/login", name="login_google")
async def login_google(request: Request):
    return await auth_service.oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@auth_router.get("/google/callback", name="auth_google_callback")
async def auth_google_callback(request: Request, db: Session = Depends(db_session)):
    return await auth_service.authorize(request, db)


@auth_router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(req: RefreshRequest):
    """Exchange a refresh token for a new access token.

    By default we don't rotate refresh tokens here. Set rotate=True in the
    service call if you want refresh rotation.
    """
    access, new_refresh = auth_service.refresh_access_token(req.refresh_token, rotate=False)
    return RefreshResponse(access_token=access, refresh_token=new_refresh)
