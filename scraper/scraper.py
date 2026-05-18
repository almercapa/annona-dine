import requests
import json
import datetime

def scrape_menu(hall, type):
    now = datetime.datetime.now()
    date = now.strftime("%Y/%m/%d")
    link = f"https://rutgers.api.nutrislice.com/menu/api/weeks/school/{hall}/menu-type/{type}/{date}"
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
                            "protein": item['food']['rounded_nutrition_info']['g_protein']
                        }
                        meals.append(meal)
    
    if not meals:
         print("No items available")
         return
    
    with open(f"{hall}_{type}.json", "w") as f:
            json.dump(meals, f, indent=2) 