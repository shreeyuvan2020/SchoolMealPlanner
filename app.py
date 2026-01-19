from openrouter import OpenRouter
import streamlit as st
from main import make_plan, respond
import json
api_key = st.secrets["API_KEY"]
with st.popover("Info about yourself"):
    st.markdown("Write any relevant information that could aid in creating a meal plan for you.")
    user_info = st.text_input("Information")
##def save_history(user_info: str, ai_response: str):
    ##with open("ai_history.txt", "r") as file:
        ##history = json.load(file) if file else []
    ##with open("ai_history.txt", "w") as file:
        ##history.append({"user_info": user_info, "ai_response": ai_response})
counter = 0
client = OpenRouter(
    api_key=api_key,
    server_url="https://ai.hackclub.com/proxy/v1",
)
if user_info:
    st.chat_message("user").markdown(f"Create a meal plan for: {user_info}")
    ai_response = make_plan(user_info, client)
    st.chat_message("assistant").markdown(ai_response)
    first_chat = st.chat_input("Modify your info above to get a new plan or talk about the current one!", key="initial_chat_input")
    if first_chat:
        st.chat_message("user").markdown(first_chat)
        st.chat_message("assistant").markdown(respond(first_chat, client))