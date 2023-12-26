from pydantic import BaseModel


class OCWarning(BaseModel):
    warning: str
