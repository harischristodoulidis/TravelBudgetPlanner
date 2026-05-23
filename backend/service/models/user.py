from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    userId: str
    username: str
    passwordHash: str
    firstName: str
    lastName: str
    friendIds: list[str]
    createdAt: datetime
