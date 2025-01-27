import uuid
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from app.src.main import app
from app.configs.db_test import override_get_db
from app.configs.db import get_db
from app.services.user_service import UserService
from app.services.qr_service import QRCodeService
from app.helpers.auth_user import hash_password
from app.models.user_model import User

@pytest.fixture
def test_client():
    """
    Create a test client to make requests to the application.
    """
    return TestClient(app)

@pytest.fixture
def mock_user_service():
    """
    Mock of the user service for testing.
    """
    class MockUserService:
        def __init__(self):
            self.users = {}

        def get(self, email):
            return self.users.get(email)

        def create(self, user):
            self.users[user.email] = user
            return user

    return MockUserService()


@pytest.fixture
def mock_qr_code_service():
    """
    Mock de QRCodeService para probar sin una base de datos real.
    """

    class MockQRCodeService:
        def __init__(self):
            self.users = {}

        def get_all(self, user_uuid):
            # Simula que devuelve una lista de QR codes para un usuario
            return [
                {
                    "uuid": str(uuid4()),
                    "url": "https://example.com",
                    "color": "#000000",
                    "size": 300,
                    "created_at": "2025-01-27 02:55:36.485692",
                    "updated_at": "2025-01-27 02:55:36.485692"
                },
                {
                    "uuid": str(uuid4()),
                    "url": "https://example.com",
                    "color": "#000000",
                    "size": 300,
                    "created_at": "2025-01-25 02:55:36.485692",
                    "updated_at": "2025-01-25 02:55:36.485692"
                }
            ]

        def get(self, qr_uuid):
            # Simula que un QR Code con un uuid válido
            if qr_uuid:
                return MagicMock(uuid=str(qr_uuid), url="https://example.com", color="#000000", size=300)
            return None

        def create(self, qr_code, user_uuid):
            # Simula la creación de un QR code en la base de datos
            return MagicMock(uuid="b9d9a2bf-a0c9-4642-b3d6-6587baad1e6d", user_uuid=user_uuid, url=qr_code.url, color=qr_code.color, size=qr_code.size)

        def update(self, qr_uuid, qr_code_data):
            # Simula la actualización de un QR code
            return MagicMock(uuid=str(qr_uuid), url=qr_code_data.url, color=qr_code_data.color, size=qr_code_data.size)

    return MockQRCodeService()


@pytest.fixture(autouse=True)
def override_services(mock_user_service, mock_qr_code_service):
    """
    Overwrite the Services with a mock.
    """
    app.dependency_overrides[UserService] = lambda: mock_user_service
    app.dependency_overrides[QRCodeService] = lambda: mock_qr_code_service
    yield
    app.dependency_overrides = {}

@pytest.fixture(autouse=True)
def override_db():
    app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_user(mock_user_service):
    """
    Create a test user in the mock service.
    """
    user_email = "testuser@example.com"
    plain_password = "securepassword"
    password_hash = hash_password(plain_password)

    # Create user in the mock service
    mock_user_service.create(
        User(
            uuid="795d6d2d-d54c-4779-9f6b-0c14c2d5c3f2",
            email=user_email,
            password_hash=password_hash
        )
    )

    # Return user and password data in plain text
    return {
        "user_uuid":"795d6d2d-d54c-4779-9f6b-0c14c2d5c3f2",
        "user_email": user_email,
        "plain_password": plain_password,
        "hashed_password": password_hash,
    }


@pytest.fixture
def auth_headers(test_client, test_user):
    """
    Provides the authentication headers required for testing.
    """
    # Login to obtain the token
    login_data = {
        "email": test_user["user_email"],
        "password": test_user["plain_password"],
    }
    response = test_client.post("/user/login", json=login_data)
    assert response.status_code == 200  # Make sure the login was successful
    token = response.json()["access_token"]

    # Return the headers with the token
    return {"Authorization": f"Bearer {token}"}


