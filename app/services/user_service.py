from fastapi import Depends

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserSchema


class UserService:
    userRepository = UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.userRepository = user_repository

    def create(self, user_body: CreateUserSchema) -> User:
        "Create a new user in the database"
        return self.userRepository.create(User(**user_body.dict()))

    def get(self, email: str) -> User:
        "Get a user by email in the database"
        return self.userRepository.get(email)