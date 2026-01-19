import streamlit as st
from main import make_plan
import json
with st.popover("Info about yourself"):
    st.markdown("Write any relevant information that could aid in creating a meal plan for you.")
    user_info = st.text_input("Information")
##def save_history(user_info: str, ai_response: str):
    ##with open("ai_history.txt", "r") as file:
        ##history = json.load(file) if file else []
    ##with open("ai_history.txt", "w") as file:
        ##history.append({"user_info": user_info, "ai_response": ai_response})

if user_info:
    ai_response = make_plan(user_info)
    st.markdown(ai_response)