import requests, datetime

# EDIT THESE to match the exact null row you looked up in menu_appearances
hall = "busch-dining-hall"       # <- set to the hall_id's actual slug from dining_halls
foodType = "breakfast"           # <- set to the food_type on the null row

now = datetime.datetime.now()
date_slash = now.strftime("%Y/%m/%d")
date_dash = now.strftime("%Y-%m-%d")

link = f"https://rutgers.api.nutrislice.com/menu/api/weeks/school/{hall}/menu-type/{foodType}/{date_slash}"
response = requests.get(link)
data = response.json()

for day in data['days']:
    if day['date'] == date_dash:
        station_name = None
        for item in day['menu_items']:
            if item['is_station_header']:
                station_name = item['text']
                print(f"[{item['position']}] HEADER -> station_name set to: {station_name!r}")
            else:
                if item['food'] is not None:
                    print(f"[{item['position']}] item: {item['food']['name']!r:40} | station_name currently: {station_name!r}")
                else:
                    print(f"[{item['position']}] skipped (food is None)")