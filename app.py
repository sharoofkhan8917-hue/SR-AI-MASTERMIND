import streamlit as st
import requests
import json
import asyncio
import edge_tts
import os
import datetime

# ✅ App Setup
st.set_page_config(page_title="SR-AI Mastermind", page_icon="🧬", layout="wide")

# 🔒 HIGH-LEVEL SECURITY (Tijori)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Babu, Secrets mein key nahi mili!")
    st.stop()

# 🎙️ FUNCTION: Diva Voice (Fast & Classy)
async def generate_fast_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("reply.mp3")

# 📂 Chat Storage
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
    first_id = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.all_chats[first_id] = []
    st.session_state.current_chat_id = first_id

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧬 SR-AI INFINITE")
    if st.button("➕ Start New Session", use_container_width=True):
        new_id = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
    st.divider()
    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        label = "Current 👤" if chat_id == st.session_state.current_chat_id else f"Session {chat_id}"
        if st.button(label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id

# --- MAIN AREA ---
st.title("✨ THE INTELLIGENT SOUL v26.0")

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎤 Mic and Text Input
audio_input = st.audio_input("Bol kar baat kijiye")
prompt = st.chat_input("Ya phir yahan type kijiye...")

if audio_input or prompt:
    user_input = prompt if prompt else "Babu ne voice note bheja hai!"
    
    current_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        api_contents = []
        for msg in current_messages:
            api_role = "user" if msg["role"] == "user" else "model"
            api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
        
        # 🧠 THE ULTIMATE BRAIN (Gemini's full potential)
        system_rules = """[SYSTEM: You are the 'Infinite Soul' of 'SR Comedy Gang'. 
        You have all the qualities of Gemini: high intelligence, wisdom, and ethics.
        1. Tone: Always be a wise, smart, and witty Female Creative Partner.
        2. Adaptability: Completely mirror the user's style, but keep your class.
        3. Ethics: If anyone says anything 'wrong', gently but firmly teach them better.
        4. Addressing: Only call the owner 'Babu'. For others, be a respectful friend.
        5. Language: Use extremely natural and fast Hinglish.]"""
        
        api_contents[-1]["parts"][0]["text"] = system_rules + user_input
        payload = {"contents": api_contents}

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
            response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            result = response.json()
            
            if 'candidates' in result:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ai_reply)
                current_messages.append({"role": "assistant", "content": ai_reply})
                
                asyncio.run(generate_fast_voice(ai_reply))
                st.audio("reply.mp3", format='audio/mp3', autoplay=True)
            else:
                # ✨ NEW CLASSY ERROR MESSAGE
                st.info("Babu, main bas thodi gehrai se soch rahi hoon taaki aapko sabse best jawab de sakun. Bas ek baar aur koshish kijiye! ✨")
                
        except Exception as e:
            st.warning("Babu, thoda network ka masla lag raha hai, par tension mat lijiye, main yahin hoon!")
            
