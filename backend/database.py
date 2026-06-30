import os # used to read variables/files
from dotenv import load_dotenv # used to load env files
from sqlalchemy import create_engine # used to create engine
from sqlalchemy.orm import declarative_base, sessionmaker # used to create blueprint and database templates

load_dotenv() # Pulls all global environment data from env file
database_url = os.getenv("DATABASE_URL") # Attaches database url from env file to a variable
engine = create_engine(database_url, pool_pre_ping=True) # Creates connection to Neon using database url, use for database interactions, pool_pre_ping tests connection before using it
Base = declarative_base() # Blueprint for all SQLAlchemy models

try: # Testing connection
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Creates a template for database sessions

def get_db(): # Opens session for route
    db = SessionLocal()
    try:
        yield db # Keeps database open while route is using it
    finally: 
        db.close() # Closes once route is completed

