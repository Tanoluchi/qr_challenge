from fastapi import Depends
from sqlalchemy.orm import Session

from app.configs.db import (
    get_db,
)
from app.models.user_model import User

class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        self.db_user = user
        self.db.add(self.db_user)
        self.db.commit()
        self.db.refresh(self.db_user)
        return self.db_user
