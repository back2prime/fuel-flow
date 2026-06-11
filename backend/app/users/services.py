from sqlalchemy import select, Result, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models.users import User
from app.users.schemes.users import (
    UserRegisterScheme,
    UserLoginScheme,
    UserPatchScheme,
    UserPasswordPatchScheme,
)

from fastapi import HTTPException, status

import datetime
from datetime import timezone

from core.constants import JWT_EXPIRE_SECONDS
from core.helpers.jwt_helper import jwt_helper


async def check_email_and_login(
    login: str | None, email: str | None, session: AsyncSession, exclude_user_id=None
) -> None:
    conditions = []
    if login:
        conditions.append(User.login == login)
    if email:
        conditions.append(User.email == email)
    if not conditions:
        return

    query = select(User.login, User.email).where(or_(*conditions))
    if exclude_user_id:
        query = query.where(User.id != exclude_user_id)
    result: Result = await session.execute(query)
    rows = result.all()

    taken_logins = {row.login for row in rows}
    taken_emails = {row.email for row in rows}

    if login in taken_logins and email in taken_emails:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This login and email are already taken",
        )
    if login in taken_logins:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This login is already taken"
        )
    if email in taken_emails:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is already taken"
        )


async def create_user(data: UserRegisterScheme, session: AsyncSession) -> User:
    await check_email_and_login(login=data.login, email=data.email, session=session)
    new_user = User(
        login=data.login,
        email=data.email,
        name=data.name,
        surname=data.surname,
        birth_date=data.birth_date,
    )
    new_user.set_password(password=data.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def auth_user(data: UserLoginScheme, session: AsyncSession) -> str:
    query = select(User).where(User.login == data.login)
    result = await session.execute(query)
    response = result.scalar_one_or_none()
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if not response.check_password(password=data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is wrong"
        )
    payload = {
        "sub": str(response.id),
        "exp": datetime.datetime.now(tz=timezone.utc)
        + datetime.timedelta(seconds=JWT_EXPIRE_SECONDS),
    }

    return jwt_helper.encode(payload=payload)


async def edit_user(user: User, data: UserPatchScheme, session: AsyncSession) -> User:
    result = data.model_dump(exclude_unset=True)
    login = result.get("login")
    email = result.get("email")
    if login or email:
        await check_email_and_login(
            login=login, email=email, session=session, exclude_user_id=user.id
        )
    for k, v in result.items():
        setattr(user, k, v)

    await session.commit()
    await session.refresh(user)
    return user


async def remove_user(user: User, session: AsyncSession) -> dict:
    await session.delete(user)
    await session.commit()
    return {"status": "ok"}


async def change_password(
    user: User, data: UserPasswordPatchScheme, session: AsyncSession
) -> dict:
    if user.check_password(data.old_password):
        user.set_password(data.new_password)
        await session.commit()
        await session.refresh(user)
        return {"status": "ok"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is wrong"
    )


async def logout(user: User) -> dict:
    return {"status": "ok"}
