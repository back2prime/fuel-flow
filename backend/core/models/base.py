import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy ORM models.

    Auto-generates __tablename__ as lowercase class name + 's'.
    Provides a UUID primary key for every model.
    """
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
