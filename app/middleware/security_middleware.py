from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.helpers.auth_user import decode_token, get_token_from_headers_or_cookies, get_current_user

from app.configs.logger import logger
from app.services.user_service import UserService


class SecurityMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)

        # Ignore public routes
        public_routes = ["/user/login", "/user/register", "/docs", "/openapi.json"]
        if any(request.url.path.startswith(route) for route in public_routes):
            await self.app(scope, receive, send)
            return

        try:
            token = get_token_from_headers_or_cookies(request)
            payload = decode_token(token)
            user = payload.get("user")
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token payload")

        except Exception as e:
            logger.error(f"Error validating token: {str(e)}")
            response = JSONResponse(status_code=401, content={"detail": str(e)})
            await response(scope, receive, send)
            return

        request.state.user = user
        logger.debug("Successfully setting user in request state")
        await self.app(scope, receive, send)