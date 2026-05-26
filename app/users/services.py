from sqlalchemy import select, Result, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemes import RegistrationScheme

from fastapi import HTTPException, status


async def check_email_and_login(login: str, email: str, session: AsyncSession) -> None:
    query = select(User.login, User.email).where(
        or_(User.login == login, User.email == email)
    )
    result = await session.execute(query)
    rows = result.all()

    taken_logins = {row.login for row in rows}
    taken_emails = {row.email for row in rows}

    if login in taken_logins and email in taken_emails:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This login and email are already taken")
    if login in taken_logins:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This login is already taken")
    if email in taken_emails:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already taken")


async def create_user(data: RegistrationScheme, session: AsyncSession) -> User:
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
