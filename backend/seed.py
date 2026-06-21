from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from database import engine, Base
from models import DiningHall

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

buschdh = DiningHall(name="Busch Dining Hall", slug="busch-dining-hall")
lividh = DiningHall(name="Livingston Dining Hall", slug="livingston-dining-commons")
neilsondh = DiningHall(name="Neilson Dining Hall", slug="neilson-dining-hall")
db.add(buschdh)
db.add(lividh)
db.add(neilsondh)
db.commit()

db.close()