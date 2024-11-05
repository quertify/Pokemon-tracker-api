
# Pokémon Tracker API

This project is a **Pokémon Tracker API** built with **FastAPI**. It allows users to:

- Search for Pokémon details.
- Mark a Pokémon as a favorite.
- Retrieve trending Pokémon based on favorite counts.

## Features

- **Search Pokémon**: Retrieve details for a specific Pokémon.
- **Favorite Pokémon**: Mark a Pokémon as a favorite for a specific user.
- **Trending Pokémon**: Retrieve a list of trending Pokémon based on the number of favorites.

## Getting Started

### Prerequisites

- **Python 3.x** (ensure Python is installed)
- **Database**: SQLite is used by default, but any SQLAlchemy-supported database can be configured.
- **Docker**: We would need to maintain local cache (redis) in docker desktop

### Installation

1. **Clone the repository**:

   ```bash
   git clone 
   cd Pokemon-Tracker-API
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Setup Redis**
   ```bash
   docker run -d -p 6379:6379 redis
   ```


### Running the API

To start the API server, run:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.
The Swagger UI  will be available at `http://127.0.0.1:8000/docs`.
## API Endpoints

### 1. Search Pokémon
   - **GET** `/pokemon/search?name={pokemon_name}`
   - **Description**: Retrieves details about the specified Pokémon.
   - **Response**:
     ```json
     {
       "name": "pikachu",
       "id": 25,
       "height": 4,
       "weight": 60,
       "types": ["electric"]
     }
     ```

### 2. Favorite a Pokémon
   - **POST** `/pokemon/{pokemon_name}/favorite?username={username}`
   - **Description**: Marks the specified Pokémon as a favorite for the given user.
   - **Response**:
     ```json
     {
       "message": "pikachu favorited by pizzaman"
     }
     ```

### 3. Trending Pokémon
   - **GET** `/pokemon/trending`
   - **Description**: Retrieves a list of the most favorited Pokémon.
   - **Response**:
     ```json
     [
       {"name": "pikachu", "favorites": 10},
       {"name": "charizard", "favorites": 8}
     ]
     ```

## Testing

Tests are located in the `tests` folder.

1. **Run all tests**:

   ```bash
   pytest
   ```

2. **Test Individual Files**:

   ```bash
   pytest tests/test_api.py
   ```

### Key Test Files

- `test_api.py`: Tests for API endpoints.
- `test_services.py`: Tests for core service functions.
- `test_cache.py`: Tests for caching logic.

## Project Structure
- `config.py`: Setup general configurations.
- `main.py`: Application entry point with endpoint definitions.
- `models.py`: Database models for `User`, `Pokemon`, and `Favorite`.
- `services.py`: Core logic for fetching Pokémon data, marking favorites, and trending calculations.
- `cache.py`: Cache management functions.
- `database.py`: Database connection.
- `task.py`: Save data in cache for most frequently liked pokemon.
- `tests/`: Folder containing unit and integration tests.



## Configuration

Database and other configurations can be updated in `config.py`. By default, the app uses an SQLite database (`sqlite:///./pokemon.db`).

## Limitations and extentions

- Add Authentication: Use JWT or OAuth for secure user access.
- Enhanced Trending Logic: Use time-based metrics for popularity trends.
- Improved Caching: Add cache invalidation for fresher data.
- Database Upgrade: Switch to PostgreSQL for scalability.
- Rate Limiting: Prevent abuse and manage traffic.
- Comprehensive Logging: Expand error handling and logs.
- User Interface: Build a web or mobile frontend.