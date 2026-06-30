from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi import Response

from app.users.dependencies import CurrentUser, TokenPayload
from app.users.models.users import User
from app.users.schemes.users import (
    UserGetScheme,
    UserRegisterScheme,
    UserLoginScheme,
    UserPatchScheme,
    UserPasswordPatchScheme,
    UserPasswordForgot,
    UserPasswordReset,
)

from app.database.dependencies import SessionDep
from app.users.services import (
    create_user,
    auth_user,
    edit_user,
    remove_user,
    change_password,
    logout,
    forgot_password,
    reset_password,
)
from core.constants import JWT_EXPIRE_SECONDS
from core.schemes.common import StatusScheme
from core.helpers.limiter import limiter

user_routers = APIRouter()


@user_routers.post(
    path="/auth/register",
    tags=["Users"],
    response_model=UserGetScheme,
    status_code=201,
)
@limiter.limit("5/minute")
async def register_user(
    request: Request, data: UserRegisterScheme, db: SessionDep
) -> User:
    return await create_user(data=data, session=db)


@user_routers.post(
    path="/auth/login",
    tags=["Users"],
    response_model=StatusScheme,
)
@limiter.limit("10/minute")
async def login_user(
    response: Response, request: Request, data: UserLoginScheme, db: SessionDep
) -> dict:
    token = await auth_user(data=data, session=db)
    response.set_cookie(
        key="access_token",
        max_age=JWT_EXPIRE_SECONDS,
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
    )
    return {"status": "ok"}


@user_routers.post(
    path="/auth/logout",
    tags=["Users"],
    response_model=StatusScheme,
)
async def logout_user(
    response: Response, user: CurrentUser, payload: TokenPayload
) -> dict:
    response.delete_cookie(key="access_token", secure=True, samesite="none")
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
async def delete_user(
    response: Response, db: SessionDep, user: CurrentUser, payload: TokenPayload
) -> dict:
    response.delete_cookie(key="access_token", secure=True, samesite="none")
    jti = payload["jti"]
    ttl = payload["exp"] - int(datetime.now(timezone.utc).timestamp())
    return await remove_user(session=db, user=user, jti=jti, ttl=ttl)


@user_routers.post(
    path="/auth/forgot-password",
    tags=["Users"],
    response_model=StatusScheme,
)
@limiter.limit("1/minute")
async def forgot_password_handler(
    request: Request, data: UserPasswordForgot, db: SessionDep
) -> dict:
    return await forgot_password(data=data, session=db)


@user_routers.post(
    path="/auth/reset-password",
    tags=["Users"],
    response_model=StatusScheme,
)
@limiter.limit("1/minute")
async def reset_password_handler(
    request: Request, data: UserPasswordReset, db: SessionDep
) -> dict:
    return await reset_password(
        new_password=data.new_password, token=data.token, session=db
    )
