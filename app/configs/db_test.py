from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)

TestingSessionLocal = sessionmaker(bind = engine)

# Dependency to get the database session in tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()