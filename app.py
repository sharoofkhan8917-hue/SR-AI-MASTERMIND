import streamlit as st
import requests
import json
import asyncio
import edge_tts
import os
import datetime

# ✅ App Setup
st.set_page_config(page_title="SR-AI Intelligent", page_icon="✨", layout="wide")

# 🔒 HIGH-SECURITY TIJORI
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets mein key nahi mili!")
    st.stop()

# 🎙️ FUNCTION: Fast Diva Voice (No Autoplay)
async def generate_fast_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("reply.mp3")

# 📂 Chat Management
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
    first_id = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.all_chats[first_id] = []
    st.session_state.current_chat_id = first_id

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]

# --- SIDEBAR ---
with st.sidebar:
    st.title("✨ SR-AI HQ")
    if st.button("➕ New Session / Clear", use_container_width=True):
        new_id = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
    st.divider()
    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        label = "Active 👤" if chat_id == st.session_state.current_chat_id else f"Session {chat_id}"
        if st.button(label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id

# --- MAIN AREA ---
st.title("✨ SR-AI Intelligent")

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

# Initial Welcome
if not current_messages:
    welcome = "Hii, main SR-AI Intelligent hoon. Bataiye main aapki kaise madad kar sakti hoon? ✨"
    with st.chat_message("assistant"):
        st.markdown(welcome)
    asyncio.run(generate_fast_voice(welcome))
    st.audio("reply.mp3", format='audio/mp3')

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✍️ TEXT INPUT
if prompt := st.chat_input("Yahan type kijiye..."):
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 🛡️ SMART BYPASS: Creator sawal ka turant jawab
        creator_keywords = ["kisne banaya", "who created", "maker", "owner", "banane wala"]
        if any(word in prompt.lower() for word in creator_keywords):
            ai_reply = "Mujhe Babu (SR Comedy Gang ke Mastermind) ne banaya hai! Main unki official intelligent assistant hoon. 😎"
        else:
            # Normal API Call
            api_contents = []
            for msg in current_messages:
                api_role = "user" if msg["role"] == "user" else "model"
                api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
            
            system_rules = "Identity: You are SR-AI Intelligent. Creator: Babu (SR Comedy Gang). Tone: Smart, Witty, Wise Female. Language: Hinglish."
            api_contents[-1]["parts"][0]["text"] = system_rules + prompt
            
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
                response = requests.post(url, json={"contents": api_contents})
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            except:
                ai_reply = "Babu, main thodi gehri soch mein hoon... bas ek baar aur koshish kijiye! ✨"

        # Final Display & Audio
        st.markdown(ai_reply)
        current_messages.append({"role": "assistant", "content": ai_reply})
        asyncio.run(generate_fast_voice(ai_reply))
        st.audio("reply.mp3", format='audio/mp3')
                
