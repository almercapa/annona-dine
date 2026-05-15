import requests
import json

response = requests.get("https://rutgers.api.nutrislice.com/menu/api/weeks/school/livingston-dining-commons/menu-type/dinner/2026/04/28/")

data = response.json()

meals = []

for item in data['days'][0]['menu_items']:
    if not item['is_station_header'] and item['food'] is not None:
        meal = {
            "name": item['food']['name'],
            "calories": item['food']['rounded_nutrition_info']['calories'],
            "protein": item['food']['rounded_nutrition_info']['g_protein']
        }
        meals.append(meal)
    with open("menu_clean.json", "w") as f:
        json.dump(meals, f, indent=2) 