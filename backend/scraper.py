import requests, datetime # uses HTTP library, used to find current date
from sqlalchemy.orm import sessionmaker # used to configure sessions
from sqlalchemy import select # used in queries
# importing models and objects from files
from database import engine
from models import DiningHall, Item, Appearance

SessionLocal = sessionmaker(bind=engine) # runs as a standalone script, NOT through FastAPI
db = SessionLocal() # establishes database session

def scrape_menu(hall, foodType):
    now = datetime.datetime.now()
    date = now.strftime("%Y/%m/%d") # finds current date
    link = f"https://rutgers.api.nutrislice.com/menu/api/weeks/school/{hall}/menu-type/{foodType}/{date}" # Takes the Nutrislice API link and makes it updatable through hall name, meal type, and date
    try: # Checks to see if API is available, returns error message if not
         response = requests.get(link) 
    except:
         print("API is down")
         return 

    data = response.json() # Stores all API data in a Python dictionary

    meals = [] # Empty array for each meal
    date = now.strftime("%Y-%m-%d")
    for day in data['days']: # Runs through each day of the week
         if day['date'] == date: # Checks if the date is today
               for item in day['menu_items']: # Runs through every possible item in the menu
                    if not item['is_station_header'] and item['food'] is not None: # Checks if item isn't the generic category name (i.e. Salad Bar, Rotisserie, Asian Station)
                        meal = {
                            "name": item['food']['name'],
                            "calories": item['food']['rounded_nutrition_info']['calories'],
                            "protein": item['food']['rounded_nutrition_info']['g_protein'],
                            "fat": item['food']['rounded_nutrition_info']['g_fat'],
                            "carbs": item['food']['rounded_nutrition_info']['g_carbs'],
                        }
                        meals.append(meal)
               # adds all food details to an object meal and then appends to array
    
    if not meals: # if no output print error message
         print("No items available")
         return
    
    for meal in meals:
         if meal.get("calories") is None: # skips item if it has no calories
              continue
         
         itemID = db.execute(select(Item).where(Item.name == meal.get("name"))).scalars().first() # retrieves the first row in database with the same name
         if itemID is None: # adds to database if it does not exist in database
              new_item = Item(name=meal.get("name"))
              db.add(new_item)
              db.commit()
              db.refresh(new_item)
              itemID = new_item

         hallID = db.execute(select(DiningHall).where(DiningHall.slug == hall)).scalars().first() # retrieves the first instance of the specific hall being scraped from

         existing = db.execute(select(Appearance).where(Appearance.item_id == itemID.id,Appearance.hall_id == hallID.id,Appearance.date == date,Appearance.food_type == foodType)).scalars().first() # checks if there is any duplicate entries in database
         if existing: # skips if duplicate exists; scraper was run more than once
              continue
         
         new_appearance = Appearance(item_id=itemID.id, hall_id=hallID.id, date=date, food_type=foodType, calories=meal.get("calories"), protein=meal.get("protein"), fat=meal.get("fat"), carbs=meal.get("carbs")) # adds new appearance to database otherwise
         db.add(new_appearance)
         db.commit()

         



halls = ["busch-dining-hall", "livingston-dining-commons", "neilson-dining-hall"] # arrays of all the current dining halls and meal types
types = ["breakfast", "lunch-test", "dinner", "knight-room-takeout"]

for hall in halls: 
     for foodType in types:
          if foodType == "knight-room-takeout": # skips takeout menu if it is not from Busch -- takeout is Busch specific
               if hall != "busch-dining-hall":
                    continue
          scrape_menu(hall, foodType) # scrapes the current menu and meal type in arrays
          print(f"Done: {hall} {foodType}") # confirmation

db.close() # closes database session