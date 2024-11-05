import pytest
from services import fetch_pokemon, mark_as_favorite
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import User, Pokemon

# Create an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    session = TestingSessionLocal()
    yield session
    session.close()

@patch("services.requests.get")
def test_fetch_pokemon(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "name": "pikachu",
        "id": 25,
        "height": 4,
        "weight": 60,
        "types": [{"type": {"name": "electric"}}]
    }
    pokemon = fetch_pokemon("pikachu")
    assert pokemon["name"] == "pikachu"
    assert pokemon["id"] == 25
    assert "electric" in pokemon["types"]

def test_mark_as_favorite(db):
    username = "ash_ketchum"
    pokemon_name = "pikachu"
    
    mark_as_favorite(db, username, pokemon_name)

    user = db.query(User).filter(User.username == username).first()
    assert user is not None
    assert user.username == username

    pokemon = db.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
    assert pokemon is not None
    assert pokemon.name == pokemon_name
