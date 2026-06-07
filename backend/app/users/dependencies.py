from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from starlette import status

from app.database.dependencies import SessionDep
from app.users.models.users import User

from core.helpers.jwt_helper import jwt_helper

security = HTTPBearer()


async def get_current_user(
    session: SessionDep, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    try:
        result = jwt_helper.decode(token=credentials.credentials)

    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token was expired"
        )
    else:
        user_id = result["sub"]
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        response = result.scalar_one_or_none()
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return response


CurrentUser = Annotated[User, Depends(get_current_user)]
