from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

# сделать так чтобы работало с классом db_helper

# SessionDep = Annotated[AsyncSession,Depends(get_session)]
