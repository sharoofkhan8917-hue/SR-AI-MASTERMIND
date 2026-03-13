import streamlit as st
import requests
import json
import asyncio
import edge_tts
import os
import datetime

# ✅ App Setup
st.set_page_config(page_title="SR-AI Intelligent", page_icon="✨", layout="wide")

# 🔒 HIGH-LEVEL SECURITY (Secrets Tijori)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

# 🎙️ FUNCTION: Diva Voice (Fast & Classy)
async def generate_fast_voice(text):
    # 'hi-IN-SwaraNeural' speed +20% for natural flow
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("reply.mp3")

# 📂 Auto-Chat Storage
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
    if st.button("➕ New Chat Session", use_container_width=True):
        new_id = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
    st.divider()
    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        label = "Active 👤" if chat_id == st.session_state.current_chat_id else f"Chat {chat_id}"
        if st.button(label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id

# --- MAIN AREA ---
st.title("✨ SR-AI Intelligent")

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

# Initial Welcome for new users (No Autoplay)
if not current_messages:
    welcome_msg = "Hii, main SR-AI Intelligent hoon. Bataiye main aapki kaise madad kar sakti hoon? ✨"
    with st.chat_message("assistant"):
        st.markdown(welcome_msg)
    asyncio.run(generate_fast_voice(welcome_msg))
    st.audio("reply.mp3", format='audio/mp3') # Manual Play

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✍️ TEXT INPUT
if prompt := st.chat_input("Yahan type kijiye..."):
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        api_contents = []
        for msg in current_messages:
            api_role = "user" if msg["role"] == "user" else "model"
            api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
        
        system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
        1. Identity: You are 'SR-AI Intelligent'. 
        2. Creator: If anyone asks who created you, say: 'Mujhe Babu (SR Comedy Gang ke Mastermind) ne banaya hai!'
        3. Personality: Smart, classy, and highly intelligent Female AI. Gemini-level wisdom.
        4. Adaptation: Mirror the user's style. Only address the owner as 'Babu'. 
        5. Morals: Promote ethics and good behavior.
        6. Language: Natural, witty Hinglish.]"""
        
        api_contents[-1]["parts"][0]["text"] = system_rules + prompt
        payload = {"contents": api_contents}

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
            response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            result = response.json()
            
            if 'candidates' in result:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ai_reply)
                current_messages.append({"role": "assistant", "content": ai_reply})
                
                # 🗣️ VOICE GENERATION (Lekin Bajega tabhi jab play karoge)
                asyncio.run(generate_fast_voice(ai_reply))
                st.audio("reply.mp3", format='audio/mp3') # Autoplay Removed
            else:
                st.info("Babu, main bas thodi gehrai se soch rahi hoon... ek baar dobara koshish kijiye! ✨")
                
        except Exception as e:
            st.warning("Network issue lag raha hai, par main yahin hoon!")
            
