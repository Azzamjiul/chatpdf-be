from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/login/google")
def login_google():
    return {"message": "Login with Google"}
