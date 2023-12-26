from pydantic import BaseModel


class SuccessApiToken(BaseModel):
    success: str
    api_token: str
