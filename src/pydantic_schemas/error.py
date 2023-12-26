from pydantic import BaseModel

from src.pydantic_schemas.warning import OCWarning


class Store(BaseModel):
    store: str


class Error(BaseModel):
    error: Store | OCWarning
