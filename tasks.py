from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Favorite, Pokemon
from database import SessionLocal
from cache import set_pokemon_in_cache


def update_trending_pokemon():
    with SessionLocal() as db:
        last_24_hours = datetime.utcnow() - timedelta(hours=24)

        trending = (
            db.query(Pokemon.name, Pokemon.favorite_count)
            .join(Favorite)
            .filter(Favorite.timestamp >= last_24_hours)
            .group_by(Pokemon.name)
            .order_by(Pokemon.favorite_count.desc())
            .limit(10)
            .all()
        )

        trending_list = [{"pokemon": name, "favorites": count} for name, count in trending]
        set_pokemon_in_cache("trending_pokemon", trending_list)
