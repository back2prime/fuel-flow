from fastapi import APIRouter

from app.users import User
from app.users.schemes import UserGetSchemes, RegistrationScheme

from app.database.dependencies import SessionDep
from app.users.services import create_user

user_routers = APIRouter()


@user_routers.post(
    path="/users",
    tags=["Users"],
    summary="Registration new user",
    response_model=UserGetSchemes,
)
async def registration(data: RegistrationScheme, db: SessionDep) -> User:
    result = await create_user(data=data, session=db)
    return result
