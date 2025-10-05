from fastapi import APIRouter, Request

# Import the Settings instance directly so attribute access works
from app.core.settings import settings
from app.services import auth_service

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/login/google", name="login_google")
async def login_google(request: Request):
    return await auth_service.oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@auth_router.get("/google/callback", name="auth_google_callback")
async def auth_google_callback(request: Request):
    token = await auth_service.oauth.google.authorize_access_token(request)
    return token
