from pydantic import BaseModel, EmailStr, Field

class CreateUserSchema(BaseModel):
    email: EmailStr
    password_hash: str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    email: EmailStr

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")
    user: UserSchema