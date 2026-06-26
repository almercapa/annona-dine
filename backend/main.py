from database import Base, engine
from fastapi import FastAPI, Depends
from models import DiningHall, Item, Appearance
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from typing import Annotated
from schemas import HallResponse, ItemDetailResponse, MenuResponse, SearchItemResponse
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

@app.get("/menu", response_model=list[MenuResponse])
def get_menu(hall: str, food_type: str, db: Annotated[Session, Depends(get_db)]):
    now = datetime.datetime.now() 
    date = now.strftime("%Y-%m-%d") # Finds the current date!
    hallID = db.execute(select(DiningHall).where(DiningHall.slug == hall)).scalars().first() # Took a while to figure out, but essentially queries the first dining hall in database that matches our hall variable
    query = (
        select(Appearance.item_id, Appearance.calories, Appearance.protein, Appearance.fat, Appearance.carbs, Appearance.food_type, Item.name)
        .join(Item)
        .where(Appearance.hall_id==hallID.id)
        .where(Appearance.date == date)
        .where(Appearance.food_type == food_type)
    )
    appearance = db.execute(query).all()
    # ^^ Queries the whole hall, pulling all rows that match the hall ID, date, and meal type. Joins the Item obj with the Appearance obj to pull data from both
    return appearance
    # Returns a list of dictionaries of every queried row in appearance

@app.get("/halls", response_model=list[HallResponse])
def get_halls(db: Annotated[Session, Depends(get_db)]):
    # Simply returns every dining hall
    return db.execute(select(DiningHall)).scalars().all()

@app.get("/items/search", response_model=list[SearchItemResponse])
def get_search(name: str, db: Annotated[Session, Depends(get_db)]):
    # Queries all DISTINCT items in the Appearance database that match the name specified, not case-sensitive
    query = (
        select(Item.name, Appearance.calories, Appearance.protein, Appearance.fat, Appearance.carbs)
        .select_from(Appearance)
        .join(Item)
        .where(Item.name.ilike(f"%{name}%"))
        .distinct()
    )
    item = db.execute(query).all()
    return item
    # Future addition: Add all available dining halls to item ("Available in Busch Dining Hall, Livingston Dining Hall, ...")

@app.get("/items/{id}", response_model=list[ItemDetailResponse])
def get_item(id: int, db: Annotated[Session, Depends(get_db)]):
    now = datetime.datetime.now() 
    date = now.strftime("%Y-%m-%d") # Finds the current date!
    # Finds all items in Appearance database that match the ID provided and current date
    query = (
        select(Item.name, Item.rarity, Item.last_seen, Appearance.calories, Appearance.fat, Appearance.carbs, Appearance.protein, DiningHall.name.label("hall_name"))
        .select_from(Appearance)
        .join(Item, Item.id == Appearance.item_id)
        .join(DiningHall, DiningHall.id == Appearance.hall_id)
        .where(Appearance.item_id==id)
        .where(Appearance.date==date)
    )
    item = db.execute(query).all()
    return item