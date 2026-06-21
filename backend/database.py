from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

load_dotenv() # Pulls all global environment data from env file
database_url = os.getenv("DATABASE_URL") # Attaches database url from env file to a variable
engine = create_engine(database_url) # Creates connection to Neon using database url
Base = declarative_base() # Blueprint for all SQLAlchemy models

try: # Testing connection
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

