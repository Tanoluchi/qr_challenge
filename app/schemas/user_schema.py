from pydantic import BaseModel, EmailStr, Field

class CreateUserSchema(BaseModel):
    email: EmailStr = Field(examples=['example@example.com'])
    password_hash: str = Field(examples=['password'])

class LoginUserSchema(BaseModel):
    email: EmailStr = Field(examples=['example@example.com'])
    password: str = Field(examples=['password'])

class UserSchema(BaseModel):
    email: EmailStr

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")
    user: UserSchema