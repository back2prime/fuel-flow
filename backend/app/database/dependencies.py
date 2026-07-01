from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.helpers.db_helper import db_helper

SessionDep = Annotated[AsyncSession, Depends(db_helper.get_async_session)]
