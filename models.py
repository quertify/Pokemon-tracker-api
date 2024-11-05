from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

#  id , username
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

#  id name, favourite_count
class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    favorite_count = Column(Integer, default=0)

#  id , user_id, pokemon_id, timestamp
class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
    pokemon = relationship("Pokemon")
