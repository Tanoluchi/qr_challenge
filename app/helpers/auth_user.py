import jwt
import os

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Response, Request, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from dotenv import load_dotenv

from app.services.user_service import UserService

from app.configs.logger import logger

load_dotenv()

# Confi hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ouath2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')

# Conf JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

# Generate Token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        logger.debug(f"Creating Access Token with data: {data} and expires_delta: {expires_delta}")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        if "user" not in to_encode:
            logger.warning("The user field is missing in the token data.")
            raise ValueError("The 'user' field is missing in the token data.")
        logger.debug("Successfully returning access token")
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Error creating token: {e}")
        raise ValueError(f"Error generating token: {e}")

# Decode and validate token JWT
def decode_token(token: str):
    try:
        logger.debug(f"Trying to decoding token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("The token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except Exception as e:
        raise ValueError(f"Error decoding the token: {e}")

def get_current_user(
        payload: dict,
        user_service: UserService = Depends()
):
    try:
        email = payload.get("user")
        if email is None:
            logger.warning("Email not found in payload data")
            raise Exception("Could not authenticated user")

        user = user_service.get(email)
        if not user:
            logger.warning("User not found in the database")
            raise Exception("User not found in the database")

        logger.debug("Successfully returning current user")
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=401, detail=str(e))

def set_token_in_cookie(response: Response, access_token: str):
    logger.debug(f"Setting access token in cookie with access_token: {access_token}")
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=timedelta(minutes=30),
        httponly=True,
        secure=False,
        samesite="Strict",
    )

def get_token_from_headers_or_cookies(request: Request) -> str:
    logger.debug(f"Trying to get token from headers or cookies with request: {request}")
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    else:
        token = request.cookies.get("access_token")
        if not token:
            logger.warning("Token not found in headers or cookies")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found",
            )
        elif token.startswith("Bearer "):
            token = token[7:]

    logger.debug("Successfully returning token")
    return token