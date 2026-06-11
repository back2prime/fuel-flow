from datetime import datetime, timezone

from fastapi import APIRouter

from app.users.dependencies import CurrentUser, TokenPayload
from app.users.models.users import User
from app.users.schemes.users import (
    UserGetScheme,
    UserRegisterScheme,
    UserLoginScheme,
    UserPatchScheme,
    UserPasswordPatchScheme,
)

from app.database.dependencies import SessionDep
from app.users.services import (
    create_user,
    auth_user,
    edit_user,
    remove_user,
    change_password,
    logout,
)
from core.schemes.common import TokenScheme, StatusScheme

user_routers = APIRouter()


@user_routers.post(
    path="/auth/register",
    tags=["Users"],
    response_model=UserGetScheme,
    status_code=201,
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


@user_routers.post(
    path="/auth/logout",
    tags=["Users"],
    response_model=StatusScheme,
)
async def logout_user(user: CurrentUser, payload: TokenPayload) -> dict:
    jti = payload["jti"]
    ttl = payload["exp"] - int(datetime.now(timezone.utc).timestamp())
    return await logout(user=user, jti=jti, ttl=ttl)


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


@user_routers.patch(
    path="/users/me/password",
    tags=["Users"],
    response_model=StatusScheme,
)
async def patch_user_password(
    data: UserPasswordPatchScheme, db: SessionDep, user: CurrentUser
) -> dict:
    return await change_password(data=data, session=db, user=user)


@user_routers.delete(
    path="/users/me",
    tags=["Users"],
    response_model=StatusScheme,
)
async def delete_user(db: SessionDep, user: CurrentUser, payload: TokenPayload) -> dict:
    jti = payload["jti"]
    ttl = payload["exp"] - int(datetime.now(timezone.utc).timestamp())
    return await remove_user(session=db, user=user, jti=jti, ttl=ttl)
