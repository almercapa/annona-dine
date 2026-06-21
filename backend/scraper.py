import requests
import datetime
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from database import engine, Base
from models import DiningHall, Item, Appearance

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def scrape_menu(hall, foodType):
    now = datetime.datetime.now()
    date = now.strftime("%Y/%m/%d")
    link = f"https://rutgers.api.nutrislice.com/menu/api/weeks/school/{hall}/menu-type/{foodType}/{date}"
    try:
         response = requests.get(link)
    except:
         print("API is down")
         return

    data = response.json()

    meals = []

    date = now.strftime("%Y-%m-%d")
    for day in data['days']:
         if day['date'] == date:
               for item in day['menu_items']:
                    if not item['is_station_header'] and item['food'] is not None:
                        meal = {
                            "name": item['food']['name'],
                            "calories": item['food']['rounded_nutrition_info']['calories'],
                            "protein": item['food']['rounded_nutrition_info']['g_protein'],
                            "fat": item['food']['rounded_nutrition_info']['g_fat'],
                            "carbs": item['food']['rounded_nutrition_info']['g_carbs'],
                        }
                        meals.append(meal)
    
    if not meals:
         print("No items available")
         return
    
    for meal in meals:
         itemID = db.execute(select(Item).where(Item.name == meal.get("name"))).scalars().first()
         if itemID is None:
              new_item = Item(name=meal.get("name"))
              db.add(new_item)
              db.commit()
              db.refresh(new_item)
              itemID = new_item

         hallID = db.execute(select(DiningHall).where(DiningHall.slug == hall)).scalars().first()
         
         new_appearance = Appearance(item_id=itemID.id, hall_id=hallID.id, date=date, food_type=foodType, calories=meal.get("calories"), protein=meal.get("protein"), fat=meal.get("fat"), carbs=meal.get("carbs"))
         db.add(new_appearance)
         db.commit()

         



halls = ["busch-dining-hall", "livingston-dining-commons", "neilson-dining-hall"]
types = ["breakfast", "lunch-test", "dinner", "knight-room-takeout"]

for hall in halls:
     for foodType in types:
          if foodType == "knight-room-takeout":
               if hall != "busch-dining-hall":
                    continue
          scrape_menu(hall, foodType)
          print(f"Done: {hall} {foodType}")

db.close()