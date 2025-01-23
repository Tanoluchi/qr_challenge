from fastapi import FastAPI
from app.configs.db import Base, engine

app = FastAPI(title="API - QR")

Base.metadata.create_all(bind=engine)
