# tests/conftest.py
import pytest
from httpx import AsyncClient
from main import app
from database import Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database URL (use in-memory SQLite for isolated tests)
TEST_DATABASE_URL = "sqlite:///./test_pokemon.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override dependency for test database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[override_get_db] = override_get_db

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create tables for tests and clean up afterward
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
