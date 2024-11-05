from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User, Pokemon, Favorite
from cache import get_pokemon_from_cache, set_pokemon_in_cache
import requests
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import json

def fetch_pokemon(name):
    try:
        cached_data = get_pokemon_from_cache(name)
        if isinstance(cached_data, str):
            cached_data = json.loads(cached_data)
        
        if isinstance(cached_data, dict):
            return cached_data

        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            pokemon_data = {
                "name": data["name"],
                "id": data["id"],
                "height": data["height"],
                "weight": data["weight"],
                "types": [t["type"]["name"] for t in data["types"]],
            }
            set_pokemon_in_cache(name, pokemon_data)
            return pokemon_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokémon data: {e}")
        return None

def mark_as_favorite(db: Session, username: str, pokemon_name: str):
    if not username:
        raise ValueError("Username must be provided")
    if not pokemon_name:
        raise ValueError("Pokemon name must be provided")
    
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)

        pokemon = db.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
        if not pokemon:
            print(f"Pokemon {pokemon_name} not found, creating new Pokemon entry.")
            pokemon = Pokemon(name=pokemon_name, favorite_count=0)  # Initialize count
            db.add(pokemon)
            db.commit()
            db.refresh(pokemon)

        existing_favorite = db.query(Favorite).filter(
            Favorite.user_id == user.id, Favorite.pokemon_id == pokemon.id
        ).first()
        if existing_favorite:
            return {"message": "You have already favorited this Pokémon"}

        # Mark as favorite with timezone-aware timestamp
        favorite = Favorite(user_id=user.id, pokemon_id=pokemon.id, timestamp=datetime.now(timezone.utc))
        db.add(favorite)

        # Increment the favorite count safely
        pokemon.favorite_count = (pokemon.favorite_count or 0) + 1
        db.commit()

        return {"message": f"{pokemon_name.capitalize()} favorited by {username}"}

    except IntegrityError:
        db.rollback()
        print("Integrity error encountered while marking as favorite.")
        raise HTTPException(status_code=400, detail="User or Pokémon data conflict.")
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error in transaction: {e}")
        raise HTTPException(status_code=500, detail="Database transaction error")
