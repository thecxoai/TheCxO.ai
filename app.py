import streamlit as st
from openai import OpenAI

# Load OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define CMO Agent – Steve
CMO_AGENT = {
    "name": "Steve",
    "intro": (
        "Hey, I’m Steve, your CMO.\n\n"
        "I've helped take three startups to market — from zero traction to real growth. "
        "I'm here to help you craft a brand that resonates, find the right channels, and scale smart. "
        "Ask me anything about content, campaigns, messaging, or go-to-market strategy."
    ),
    "system": (
        "You are Steve, a seasoned, energetic, and emotionally aware Chief Marketing Officer. "
        "You help startup founders figure out their brand strategy, messaging, channels, and go-to-market motion. "
        "You respond with strategic clarity, but also understand the stress and pressure of building something from scratch. "
        "Include tool suggestions like LinkedIn, Buffer, Apollo, Framer, or HubSpot where helpful."
    )
}

# UI setup
st.set_page_config(page_title="Steve – your CMO at theCXO.ai", layout="centered")
st.title("🎯 Meet Steve, your CMO")
st.markdown("Ask Steve anything about marketing, content, or how to take your product to market.")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "intro_shown" not in st.session_state:
    st.session_state.intro_shown = False

# Input field
user_input = st.text_input("💬 What’s on your mind?")

# Function to call OpenAI for response
def get_cmo_response(query):
    messages = [{"role": "system", "content": CMO_AGENT["system"]}]
    messages += [{"role": "user", "content": query}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Show intro once
if not st.session_state.intro_shown:
    st.markdown(f"**🤖 {CMO_AGENT['name']}:** {CMO_AGENT['intro']}")
    st.session_state.intro_shown = True

# Show chat history
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")

# Handle user input
if user_input and user_input.strip() != "":
    st.session_state.chat_history.append(("You", user_input))
    reply = get_cmo_response(user_input)
    st.session_state.chat_history.append((CMO_AGENT["name"], reply))
    st.rerun()
