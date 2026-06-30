from sqlalchemy.orm import sessionmaker # used to configure sessions
# importing objects and functions from other files
from database import engine
from models import DiningHall

SessionLocal = sessionmaker(bind=engine) # runs as a standalone script, NOT through FastAPI
db = SessionLocal() # establishes database session

buschdh = DiningHall(name="Busch Dining Hall", slug="busch-dining-hall") 
lividh = DiningHall(name="Livingston Dining Hall", slug="livingston-dining-commons")
neilsondh = DiningHall(name="Neilson Dining Hall", slug="neilson-dining-hall")
db.add(buschdh)
db.add(lividh)
db.add(neilsondh)
db.commit() # adds each dining hall to its own dining hall database

db.close() # closes database session