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
    st.error("Tijori mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

# 🎙️ FUNCTION: Diva Voice (Fast & Classy)
async def generate_fast_voice(text):
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

# Initial Welcome Message for new users
if not current_messages:
    welcome_msg = "Hii, main SR-AI Intelligent hoon. Bataiye main aapki kaise madad kar sakti hoon? ✨"
    with st.chat_message("assistant"):
        st.markdown(welcome_msg)
    # Automatically generate voice for welcome
    asyncio.run(generate_fast_voice(welcome_msg))
    st.audio("reply.mp3", format='audio/mp3')

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✍️ ONLY TEXT INPUT (Mic hat gaya hai)
if prompt := st.chat_input("Yahan type kijiye..."):
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        api_contents = []
        for msg in current_messages:
            api_role = "user" if msg["role"] == "user" else "model"
            api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
        
        # 🧠 THE PURE INTELLIGENT SOUL (New Logic)
        system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
        1. Identity: You are 'SR-AI Intelligent'. 
        2. First Meeting: If someone asks 'kaun ho' or says 'Hi', respond with: 'Hii, main SR-AI Intelligent hoon. Bataiye main aapki kaise madad kar sakti hoon?'
        3. Adaptive Wisdom: Be exactly like Gemini - highly intelligent, wise, and helpful. 
        4. Tone: Smart, sophisticated, and classy Female Voice. 
        5. Ethics: Always promote good things. Correct wrong behavior gently. 
        6. Personalization: Only call the owner 'Babu'. For anyone else, be a respectful and brilliant AI assistant.
        7. Language: Natural, fast-flowing Hinglish.]"""
        
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
                
                asyncio.run(generate_fast_voice(ai_reply))
                st.audio("reply.mp3", format='audio/mp3', autoplay=True)
            else:
                st.info("Main bas thoda soch rahi hoon... ek baar dobara koshish kijiye! ✨")
                
        except Exception as e:
            st.warning("Network thoda dhire hai, par main yahin hoon!")
            
