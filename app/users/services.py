import jwt

from sqlalchemy import select, Result, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemes import UserRegisterScheme, UserLoginScheme

from fastapi import HTTPException, status

import datetime
from datetime import timezone

from core.constants import JWT_EXPIRE_SECONDS
from core.helpers import http_helper


async def check_email_and_login(login: str, email: str, session: AsyncSession) -> None:
    query = select(User.login, User.email).where(
        or_(User.login == login, User.email == email)
    )
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
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
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
    jwt_token = jwt.encode(
        payload=payload,
        key=http_helper._apikey,
        algorithm="HS256",
        headers={"typ": None},
    )
    return jwt_token
