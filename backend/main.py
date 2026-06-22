from database import Base, engine
from fastapi import FastAPI, Depends
from models import DiningHall, Item, Appearance
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from typing import Annotated
import datetime


app = FastAPI() # Creates app instance
Base.metadata.create_all(bind=engine) # Creates all tables on startup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/menu")
def get_menu(hall: str, food_type: str, db: Annotated[Session, Depends(get_db)]):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    hallID = db.execute(select(DiningHall).where(DiningHall.slug == hall)).scalars().first()
    appearance = db.execute(select(Appearance.item_id, Appearance.calories, Appearance.fat, Appearance.carbs, Appearance.food_type, Item.name).join(Item).where(Appearance.hall_id==hallID.id).where(Appearance.date == date).where(Appearance.food_type == food_type)).all()
    return [dict(row._mapping) for row in appearance]