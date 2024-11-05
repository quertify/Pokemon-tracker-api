import redis
import json
from config import REDIS_URL

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

def get_pokemon_from_cache(name):
    data = redis_client.get(f"pokemon:{name}")
    return json.loads(data) if data else None

def set_pokemon_in_cache(name, data):
    try:

        expiration = 3600 if name == "trending_pokemon" else 600
        

        cache_key = f"pokemon:{name}" if name != "trending_pokemon" else name
        

        redis_client.setex(cache_key, expiration, json.dumps(data))

    except (TypeError, ValueError) as e:
        print(f"Error serializing data for cache: {e}")
    except Exception as e:
        print(f"Error setting data in cache: {e}")
