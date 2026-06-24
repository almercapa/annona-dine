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
    date = now.strftime("%Y-%m-%d") # Finds the current date!
    hallID = db.execute(select(DiningHall).where(DiningHall.slug == hall)).scalars().first() # Took a while to figure out, but essentially queries the first dining hall in database that matches our hall variable
    appearance = db.execute(select(Appearance.item_id, Appearance.calories, Appearance.fat, Appearance.carbs, Appearance.food_type, Item.name).join(Item).where(Appearance.hall_id==hallID.id).where(Appearance.date == date).where(Appearance.food_type == food_type)).all()
    # ^^ Queries the whole hall, pulling all rows that match the hall ID, date, and meal type. Joins the Item obj with the Appearance obj to pull data from both
    return [dict(row._mapping) for row in appearance]
    # Returns a list of dictionaries of every queried row in appearance

@app.get("/halls")
def get_halls(db: Annotated[Session, Depends(get_db)]):
    return db.execute(select(DiningHall)).scalars().all()

@app.get("/items/search")
def get_search(name: str, db: Annotated[Session, Depends(get_db)]):
    item = db.execute(select(Item.name, Appearance.calories, Appearance.fat, Appearance.carbs, Appearance.protein).select_from(Appearance).join(Item).where(Item.name.ilike(f"%{name}%")).distinct()).all()
    return [dict(row._mapping) for row in item]

@app.get("/items/{id}")
def get_item(id: int, db: Annotated[Session, Depends(get_db)]):
    now = datetime.datetime.now() 
    date = now.strftime("%Y-%m-%d") # Finds the current date!
    item = db.execute(select(Item.name, Item.rarity, Item.last_seen, Appearance.calories, Appearance.fat, Appearance.carbs, Appearance.protein, DiningHall.name).select_from(Appearance).join(Item, Item.id == Appearance.item_id).join(DiningHall, DiningHall.id == Appearance.hall_id).where(Appearance.item_id==id).where(Appearance.date==date)).all()
    return [dict(row._mapping) for row in item]