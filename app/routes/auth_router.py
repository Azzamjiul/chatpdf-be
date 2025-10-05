from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database.engine import db_session
from app.services import auth_service

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/google/login", name="login_google")
async def login_google(request: Request):
    return await auth_service.oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@auth_router.get("/google/callback", name="auth_google_callback")
async def auth_google_callback(request: Request, db: Session = Depends(db_session)):
    return await auth_service.authorize(request, db)
