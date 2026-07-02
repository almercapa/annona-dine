import datetime # used to find the date
from fastapi import FastAPI, Depends, HTTPException, status # used to initialize FastAPI and dependencies
from sqlalchemy.orm import Session # used for type hinting
from sqlalchemy import select, func, and_ # used in queries
from typing import Annotated # used as database parameter
# all pulling objects/functions from other classes
from database import Base, engine, get_db
from models import DiningHall, Item, Appearance, User, Rating, Pin
from schemas import HallResponse, ItemDetailResponse, MenuResponse, SearchItemResponse, UserResponse, RatingRequest, RatingResponse, PinResponse
from auth import router, get_current_user

app = FastAPI() # Creates app instance
app.include_router(router) # Informs FastAPI of the routes in auth.py
Base.metadata.create_all(bind=engine) # Creates all tables on startup

def get_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

#  Retrieving menu from database, response_model represents a list of rows in the database
@app.get("/menu", response_model=list[MenuResponse])
def get_menu(hall: str, food_type: str, db: Annotated[Session, Depends(get_db)]):
    date = get_date() # Finds the current date!
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

@app.get("/users/me", response_model=UserResponse) # Gets your profile
def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user


@app.get("/items/{id}/rating", response_model=RatingResponse) 
def get_rating(id: int, db: Annotated[Session, Depends(get_db)]):
    query = ( 
        select(func.avg(Rating.score), func.count(Rating.score)) # Queries an average and total score using the Rating object
        .where(Rating.item_id==id) # Filters by ID
    )
    res = db.execute(query).first()
    return {"score": res[0], "count": res[1]} # Returns as dictionary

@app.get("/items/{id}", response_model=list[ItemDetailResponse])
def get_item(id: int, db: Annotated[Session, Depends(get_db)]):
    date = get_date()
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

@app.post("/items/{id}/rate")
def rate_item(id: int, rating: RatingRequest, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    query = ( # Queries Rating object by item and user ID
        select(Rating)
        .where(Rating.item_id==id)
        .where(Rating.user_id==user.id)
    )
    rate_check = db.execute(query).scalars().first() # Grabs the first row that matches

    if not rate_check: # If no row exists add it to database
        new_rating = Rating(user_id=user.id, item_id=id, score=rating.score)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return {"message": "Rating submitted successfully"}
    else:
        update_check = (datetime.datetime.now() - rate_check.updated_at) # Check when the last update was
        if update_check.days >= 120:
            rate_check.score = rating.score # Update score if matches
            db.commit()
            return {"message": "Rating updated successfully"}
        else:
            raise HTTPException( # Raise error if not
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Must wait at least 4 months before rerating"
            )

@app.get("/users/me/pins", response_model=list[PinResponse])
def get_pin(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    date = get_date()
    query = (
        select(Pin.item_id, Item.name, Item.rarity, Item.last_seen, Appearance.hall_id, DiningHall.name.label("hall_name"))
        .select_from(Pin)
        .join(Item, Item.id == Pin.item_id)
        .outerjoin(Appearance, and_(Appearance.item_id == Item.id, Appearance.date == date))
        .outerjoin(DiningHall, DiningHall.id == Appearance.hall_id)
        .where(Pin.user_id == user.id)
    )
    pins = db.execute(query).all()
    pinList = {}
    for pin in pins:
        if pin.item_id not in pinList:
            pinList[pin.item_id] = {
                "item_id": pin.item_id,
                "name": pin.name,
                "rarity": pin.rarity,
                "last_seen": pin.last_seen,
                "available_today": []
            }
        if pin.hall_id is not None:
            pinList[pin.item_id]["available_today"].append(pin.hall_name)

    return pinList.values()

@app.post("/items/{id}/pin")
def pin_item(id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    query = (
        select(func.count(Pin.item_id))
        .where(Pin.user_id==user.id)
    )
    count = db.execute(query).scalar()

    if count > 3:
        raise HTTPException( # Raise error if not
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Maximum pins reached"
        )
    
    query = ( # Queries Rating object by item and user ID
        select(Pin)
        .where(Pin.item_id==id)
        .where(Pin.user_id==user.id)
    )
    pin_check = db.execute(query).scalars().first() # Grabs the first row that matches

    if not pin_check: # If no row exists add it to database
        new_pin = Pin(user_id=user.id, item_id=id)
        db.add(new_pin)
        db.commit()
        db.refresh(new_pin)
        return {"message": "Item pinned successfully"}
    else:
        raise HTTPException( # Raise error if not
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Item already pinned"
        )
    
@app.delete("/items/{id}/pin")
def delete_pin(id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    query = ( # Queries Rating object by item and user ID
        select(Pin)
        .where(Pin.item_id==id)
        .where(Pin.user_id==user.id)
    )
    pin_check = db.execute(query).scalars().first() # Grabs the first row that matches

    if pin_check: # If no row exists add it to database
        db.delete(pin_check)
        db.commit()
        return {"message": "Item removed successfully"}
    else:
        raise HTTPException( # Raise error if not
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Item not currently pinned"
        )