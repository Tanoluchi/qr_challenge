from fastapi import FastAPI

from app.configs.db import create_tables
from app.routers.qr_router import QRCodeRouter
from app.routers.user_router import UserRouter

# Create tables in database when the application starts up.
create_tables()

app = FastAPI(title="API - QR Codes")

app.include_router(QRCodeRouter)
app.include_router(UserRouter)

