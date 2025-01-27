from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.schemas.user_schema import (
    CreateUserSchema,
    UserSchema,
    TokenSchema,
    LoginUserSchema
)
from app.helpers.auth_user import (
    create_access_token,
    verify_password,
    hash_password,
    set_token_in_cookie,
)
from app.services.user_service import UserService

UserRouter = APIRouter(
    prefix="/user",
    tags=["Users"],
)

@UserRouter.get("/", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def user(request: Request, user_service: UserService = Depends()):
    """
    Get the current authenticated user.

        **Args**:
            request (Request): The FastAPI request object

        **Returns**:
            UserSchema: Contains the authenticated user information

        **Raises**:
            HTTPException: If the user is not authenticated
    """
    user = user_service.get(request.state.user)
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User is authenticated"})

@UserRouter.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(
        user: CreateUserSchema,
        user_service: UserService = Depends()
):
    """
    Create a new user with the provided data.

        **Request Body**:

        - **email**: Required (string)
        - **password**: Required (string)

        **Args**:
            user (CreateUserSchema): The user to be created

        **Returns**:
            UserSchema: Contains the created user information

        **Raises**:
            HTTPException: If the user already exists
    """
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
    """
        Authenticate a user and return an access token.

        **Request Body**:

        - **email**: Required (string)
        - **password**: Required (string)

        **Args**:
            user (LoginUserSchema): The user to be authenticated

        **Returns**:
            TokenSchema: Contains the access token and user information

        **Raises**:
            HTTPException: If the user does not exist or the password is incorrect
    """
    try:
        exist_user = user_service.get(user.email)
        if not exist_user or not verify_password(user.password, exist_user.password_hash):
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