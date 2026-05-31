from pydantic import BaseModel


class FrozenModelType(BaseModel):
    """
    Base Pydantic model with immutable fields.
    """

    model_config = {"frozen": True}
