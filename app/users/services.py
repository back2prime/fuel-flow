from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemes import RegistrationScheme, UserGetSchemes

from fastapi import HTTPException, status


async def check_email_and_login(login: str, email: str, session: AsyncSession) -> None:
    login_query = select(User.login).where(User.login == login)
    login_query_result: Result = await session.execute(login_query)
    login_result = login_query_result.scalar_one_or_none()

    email_query = select(User.email).where(User.email == email)
    email_query_result: Result = await session.execute(email_query)
    email_result = email_query_result.scalar_one_or_none()

    if login_result and email_result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This login and email is already taken",
        )
    elif login_result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This login is already taken"
        )
    elif email_result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is already taken"
        )


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
