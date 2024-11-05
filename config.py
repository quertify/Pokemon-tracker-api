import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pokemon.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

#  We are using a cache and a DB