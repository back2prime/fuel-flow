from fastapi import APIRouter

from app.users.dependencies import CurrentUser
from app.users.models.users import User
from app.users.schemes.users import UserGetScheme, UserRegisterScheme, UserLoginScheme

from app.database.dependencies import SessionDep
from app.users.services import create_user, auth_user
from core.schemes.jwt_token_scheme import TokenScheme

user_routers = APIRouter()


@user_routers.post(
    path="/auth/register",
    tags=["Users"],
    response_model=UserGetScheme,
)
async def register_user(data: UserRegisterScheme, db: SessionDep) -> User:
    return await create_user(data=data, session=db)


@user_routers.post(
    path="/auth/login",
    tags=["Users"],
    response_model=TokenScheme,
)
async def login_user(data: UserLoginScheme, db: SessionDep) -> dict:
    return {
        "access_token": await auth_user(data=data, session=db),
        "token_type": "bearer",
    }


@user_routers.get(
    path="/users/me",
    tags=["Users"],
    response_model=UserGetScheme,
)
async def get_user(user: CurrentUser) -> User:
    return user
