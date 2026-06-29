import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv() # Pulls all global environment data from env file
database_url = os.getenv("DATABASE_URL") # Attaches database url from env file to a variable
engine = create_engine(database_url, pool_pre_ping=True) # Creates connection to Neon using database url
Base = declarative_base() # Blueprint for all SQLAlchemy models

try: # Testing connection
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

