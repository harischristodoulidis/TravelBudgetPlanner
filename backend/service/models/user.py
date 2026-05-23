from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
    userId: str = Field(..., description="Unique user identifier", examples=["u1"])
    username: str = Field(..., description="Login handle", examples=["jdoe"])
    passwordHash: str = Field(..., description="Bcrypt-hashed password (not returned in production)", examples=["hashed"])
    firstName: str = Field(..., description="User's first name", examples=["John"])
    lastName: str = Field(..., description="User's last name", examples=["Doe"])
    friendIds: list[str] = Field(..., description="List of friend user IDs", examples=[["u2"]])
    createdAt: datetime = Field(..., description="Account creation timestamp (ISO-8601)", examples=["2024-01-01T00:00:00"])
