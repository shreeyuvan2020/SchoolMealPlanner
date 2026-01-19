import requests
from datetime import date
import os
import json

def make_plan(user_info="A student athlete (baseball) who trains after school."):
    today = date.today()
    food = requests.get(f"https://srvusd.api.nutrislice.com/menu/api/weeks/school/pine-valley-middle/menu-type/lunch/{today.year}/{today.month}/{today.day}/?format=json").json()
    api_key = os.getenv("API_KEY")
    print(api_key)
    all_food = []
    for day in food.get("days", []):
        items = day.get("menu_items", [])
        if not items:
            continue
        else:
            for item in items:
                food_items = item.get("food", {})
                if not food_items:
                    continue
                food_data = {
                    "date": day.get("date"),
                    "name": food_items.get("name"),
                    "category": food_items.get('food_category'),
                    "nutrition": food_items.get('rounded_nutrition_info'),
                    "allergens": [i.get('name') for i in food_items.get('icons', {}).get('food_icons', [])]
                }
                all_food.append(food_data)
    prompt = json.dumps(all_food, indent=2) + f"""
You are a nutritionist. This is the info the customer has given you: {user_info}.
Based on the menu provided above, please create a meal plan for the week.
For each day, choose one entree, one optional beverage, and either a fruit or a vegetable that would be suitable for the customer.
Present the plan with the days of the week as titles (e.g., Monday, Tuesday).
ONLY USE THE FOOD ITEMS AVAILABLE.
"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-3-flash-preview",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(
        "https://ai.hackclub.com/proxy/v1/chat/completions",
        headers=headers,
        json=data
    )
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(make_plan())