from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    access_token: str
