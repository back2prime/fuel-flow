from fastapi import APIRouter

from app.users.dependencies import CurrentUser
from app.users.models.users import User
from app.users.schemes.users import (
    UserGetScheme,
    UserRegisterScheme,
    UserLoginScheme,
    UserPatchScheme,
)

from app.database.dependencies import SessionDep
from app.users.services import create_user, auth_user, edit_user, remove_user
from core.schemes.common import TokenScheme, StatusScheme

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


@user_routers.patch(
    path="/users/me",
    tags=["Users"],
    response_model=UserGetScheme,
)
async def patch_user(data: UserPatchScheme, db: SessionDep, user: CurrentUser) -> User:
    return await edit_user(user=user, data=data, session=db)


@user_routers.delete(
    path="/users/me",
    tags=["Users"],
    response_model=StatusScheme,
)
async def delete_user(db: SessionDep, user: CurrentUser) -> dict:
    return await remove_user(user=user, session=db)
