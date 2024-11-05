from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User, Pokemon, Favorite
from services import fetch_pokemon, mark_as_favorite
import json
from cache import redis_client
from tasks import update_trending_pokemon

app = FastAPI()

# Initialize the database tables
Base.metadata.create_all(bind=engine)

@app.get("/pokemon/search")
async def search_pokemon(name: str):
    pokemon = fetch_pokemon(name)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@app.post("/pokemon/{pokemon_name}/favorite", status_code=200)
async def favorite_pokemon(pokemon_name: str, background_tasks: BackgroundTasks, username: str, db: Session = Depends(get_db)):
    try:
        result = mark_as_favorite(db, username, pokemon_name)
        
        if "message" in result:
            print("we are here")
            return result  # Return
        background_tasks.add_task(update_trending_pokemon)

        return {"message": f"{pokemon_name} favorited by {username}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pokemon/trending")
async def trending_pokemon():
    trending = redis_client.get("trending_pokemon")
    if trending:
        return json.loads(trending)
    else:
        # Run the update synchronously if no data is found
        update_trending_pokemon()
        trending = redis_client.get("trending_pokemon")
        return json.loads(trending) if trending else {"message": "No trending data available."}
