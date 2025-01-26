from fastapi import FastAPI

from app.configs.db import create_tables
from app.middleware.security_middleware import SecurityMiddleware
from app.routers.qr_router import QRCodeRouter
from app.routers.user_router import UserRouter
from app.routers.scan_router import ScanerRouter
from app.routers.statistics_router import StatisticsRouter
from app.services.user_service import UserService

# Create tables in database when the application starts up.
create_tables()

app = FastAPI(title="API - QR Codes")

app.include_router(QRCodeRouter)
app.include_router(UserRouter)
app.include_router(ScanerRouter)
app.include_router(StatisticsRouter)

user_service = UserService()

# Add security middleware
app.add_middleware(SecurityMiddleware)
