import streamlit as st
from xmlrpc import client
from openrouter import OpenRouter
import requests
from datetime import date
import os
import json
def respond(prompt: str, client: OpenRouter, history):
    history = st.session_state.history
    old_prompt = prompt
    prompt = prompt + f"Here is the history of what has been asked before and what has been responded: {history}"
    response = client.chat.send(
    model="google/gemini-3-flash-preview",
    messages=[
        {"role": "user", "content": prompt}
    ],
    stream=False,
)
    st.session_state.history = history + [{
            "prompt": old_prompt,
            "response": response.choices[0].message.content
        }]
    return response.choices[0].message.content
def make_plan(user_info="A student athlete (baseball) who trains after school.", client=None):
    today = date.today()
    food = requests.get(f"https://srvusd.api.nutrislice.com/menu/api/weeks/school/pine-valley-middle/menu-type/lunch/{today.year}/{today.month}/{today.day}/?format=json").json()
    api_key = os.getenv("API_KEY")
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
    

    response = client.chat.send(
    model="google/gemini-3-flash-preview",
    messages=[
        {"role": "user", "content": prompt}
    ],
    stream=False,
)
    st.session_state.history = [{
            "prompt": prompt,
            "plan": response.choices[0].message.content
        }]
    return response.choices[0].message.content