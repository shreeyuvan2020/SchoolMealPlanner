from openrouter import OpenRouter
import streamlit as st
from main import make_plan, respond
import json
api_key = st.secrets["API_KEY"]
with st.popover("Info about yourself"):
    st.markdown("Write any relevant information that could aid in creating a meal plan for you.")
    user_info = st.text_input("Information")
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
        response = respond(first_chat, client, st.session_state.history)
        history = st.session_state.history
        st.chat_message("assistant").markdown(response)