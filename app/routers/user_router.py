from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder

from app.schemas.user_schema import (
    CreateUserSchema,
    UserSchema,
    LoginUserSchema,
    TokenSchema
)
from app.helpers.auth_user import (
    create_access_token,
    verify_password,
    hash_password,
    set_token_in_cookie,
    get_current_user
)
from app.services.user_service import UserService

UserRouter = APIRouter(
    prefix="/user",
    tags=["user"],
)

@UserRouter.get("/", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def user(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UserSchema(**jsonable_encoder(user))

@UserRouter.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(
        user: CreateUserSchema,
        user_service: UserService = Depends()
):
    if user_service.get(user.email):
        raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists")

    user.password_hash = hash_password(user.password_hash)
    created_user = user_service.create(user)
    return UserSchema(**jsonable_encoder(created_user))


@UserRouter.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def authenticate_user(
        user: LoginUserSchema,
        response: Response,
        user_service: UserService = Depends()
):
    try:
        exist_user = user_service.get(user.email)
        if not exist_user:
            raise HTTPException(status_code=400, detail=f"Sorry, there was a problem, the login failed")

        if not verify_password(user.password, exist_user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Sorry, there was a problem, the login failed",
            )
        access_token = create_access_token({"user": user.email})
        set_token_in_cookie(response, access_token)

        return TokenSchema(
            access_token=access_token,
            user=UserSchema(email=exist_user.email)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))