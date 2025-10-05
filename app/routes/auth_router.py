from fastapi import APIRouter, Request

# Import the Settings instance directly so attribute access works
from app.core.settings import settings
from app.services import auth_service

auth_router = APIRouter()


@auth_router.get("/login/google", name="login_google")
async def login_google(request: Request):
    return await auth_service.oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)
