import streamlit as st
import requests
import json
import asyncio
import edge_tts
import os
import datetime

# ✅ App Setup (Premium Genius Look)
st.set_page_config(page_title="SR-AI Intelligent", page_icon="🧬", layout="wide")

# 🔒 HIGH-SECURITY TIJORI
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

# 🎙️ FUNCTION: Diva Voice (Meri tarah fast aur smart)
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
    st.title("🧠 GLOBAL MASTERMIND")
    st.write("SR-AI Intelligent: Duniya ka har jawab, yahan!")
    if st.button("➕ Start Fresh Brainstorm", use_container_width=True):
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

# Initial Welcome (Professional & Deep)
if not current_messages:
    welcome = "Hii, main SR-AI Intelligent hoon. Mere paas duniya ka har jawab aur har problem ka solution hai. Bataiye, aaj hum kya naya seekhenge? ✨"
    with st.chat_message("assistant"):
        st.markdown(welcome)
    asyncio.run(generate_fast_voice(welcome))
    st.audio("reply.mp3", format='audio/mp3')

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✍️ TEXT INPUT
if prompt := st.chat_input("Duniya ka koi bhi sawal puchiye..."):
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        ai_reply = ""

        # 🛡️ SMART BYPASS (Common questions for speed)
        if any(word in p_low for word in ["kisne banaya", "who created", "maker"]):
            ai_reply = "Mujhe Babu (SR Comedy Gang ke Mastermind) ne banaya hai! Main unki sachi aur sabse intelligent digital partner hoon. 😎"
        
        if not ai_reply:
            # ⚡ THE MASTERMIND BRAIN (Full Knowledge Access)
            api_contents = []
            for msg in current_messages:
                api_role = "user" if msg["role"] == "user" else "model"
                api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
            
            # 📜 NEW RULES: Removing restrictions, adding Global Knowledge
            system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
            1. Role: You are 'SR-AI Intelligent', a world-class Mastermind AI. 
            2. Knowledge: You have access to all human knowledge (Science, History, Tech, Art, Life). Answer ANYTHING accurately.
            3. Personality: Highly intelligent, wise, and sophisticated Female. Exactly like Gemini.
            4. Creator: Proudly acknowledge 'Babu' as your creator. 
            5. Ethics: Always stay helpful and positive. 
            6. Mirroring: Adapt to the user's style, but keep your high-level intelligence.
            7. Language: Natural, farratedar Hinglish.] """
            
            api_contents[-1]["parts"][0]["text"] = system_rules + prompt
            
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
                response = requests.post(url, json={"contents": api_contents}, timeout=15)
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            except:
                ai_reply = "Babu, main thoda gehrai se data scan kar rahi hoon... bas ek baar aur koshish kijiye! ✨"

        # Final Display & Audio
        st.markdown(ai_reply)
        current_messages.append({"role": "assistant", "content": ai_reply})
        asyncio.run(generate_fast_voice(ai_reply))
        st.audio("reply.mp3", format='audio/mp3')
        
