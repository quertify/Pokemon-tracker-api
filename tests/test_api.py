import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
from database import Base, engine, SessionLocal
from models import User, Pokemon, Favorite

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(User).delete()
        db.query(Pokemon).delete()
        db.query(Favorite).delete()
        db.commit()
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@patch("services.requests.get")
def test_search_pokemon(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "name": "pikachu",
        "id": 25,
        "height": 4,
        "weight": 60,
        "types": [{"type": {"name": "electric"}}]
    }
    response = client.get("/pokemon/search?name=pikachu")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "pikachu"
    assert "electric" in data["types"]

@patch("services.fetch_pokemon")
def test_favorite_pokemon(mock_fetch_pokemon):
    mock_fetch_pokemon.return_value = {
        "name": "pikachu",
        "id": 25,
        "height": 4,
        "weight": 60,
        "types": ["electric"]
    }

    response = client.post("/pokemon/pikachu/favorite?username=pizzam")
    print("First request response:", response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Pikachu favorited by pizzam"

@patch("services.fetch_pokemon")
def test_trending_pokemon(mock_fetch_pokemon):
    mock_fetch_pokemon.side_effect = [
        {"name": "pikachu", "id": 25, "height": 4, "weight": 60, "types": ["electric"]},
        {"name": "charizard", "id": 6, "height": 17, "weight": 905, "types": ["fire", "flying"]}
    ]

    client.post("/pokemon/pikachu/favorite?username=trendy_user1")
    client.post("/pokemon/charizard/favorite?username=trendy_user2")

    response = client.get("/pokemon/trending")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list), "Expected list response for trending Pokémon"
    for entry in data:
        assert "pokemon" in entry, "Each entry in trending data should contain a 'name' key"
    assert any(p["pokemon"] == "pikachu" for p in data)
    assert any(p["pokemon"] == "charizard" for p in data)
