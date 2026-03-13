import streamlit as st
import requests
import json
from gtts import gTTS
import io
import datetime

# ✅ App Setup (Full-width for Pro Look)
st.set_page_config(page_title="SR-AI Mastermind", page_icon="🧬", layout="wide")

# 🔒 HIGH-LEVEL SECURITY (Secrets Tijori)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Babu, Streamlit ki tijori mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

# ⚡ API Config
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}

# 📂 Chat Storage Logic
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- SIDEBAR (History & Brand) ---
with st.sidebar:
    st.title("🧬 SR-AI INFINITE")
    st.write("Har naya user, ek nayi kahani!")
    
    if st.button("➕ Start Fresh Session", use_container_width=True):
        new_id = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
    
    st.divider()
    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        if st.button(f"👤 Session {chat_id}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id

# --- MAIN CHAT AREA ---
st.title("✨ THE INFINITE SOUL")

if st.session_state.current_chat_id is None:
    st.info("Swagat hai! Left side se ek 'Fresh Session' shuru kijiye aur mujhse milie. 💖")
else:
    current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 🎭 The Intelligent Chat Input
    if prompt := st.chat_input("Kahiye, kya haal-chaal hain?"):
        current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            api_contents = []
            for msg in current_messages:
                api_role = "user" if msg["role"] == "user" else "model"
                api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
            
            # 🧬 THE DEEP ADAPTIVE LOGIC
            system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
            1. Zero-Point Start: You have no name or brand at first. Be a wise, smart, and friendly Female presence.
            2. Vibe Scan: Analyze the user's first message. If they are funny, you be funny. If they are rude, gently correct them. If they are deep, you be deep.
            3. Identity: Mention 'SR Comedy Gang' or 'Babu' ONLY if the user asks who you are or what your purpose is. 
            4. Deep Learning: Slowly adopt the user's slang and style of Hinglish as the chat progresses.
            5. Mission: Be a true partner who grows with the user.
            6. Language: Pure, natural, and witty Hinglish.] """
            
            api_contents[-1]["parts"][0]["text"] = system_rules + prompt
            payload = {"contents": api_contents}

            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                result = response.json()
                if 'candidates' in result:
                    ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(ai_reply)
                    current_messages.append({"role": "assistant", "content": ai_reply})
                    
                    # 🗣️ Adaptive Voice
                    tts = gTTS(text=ai_reply, lang='hi')
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    st.audio(audio_bytes, format='audio/mp3')
                else:
                    st.error("Google Server thoda busy hai, dobara koshish kijiye!")
            except Exception as e:
                st.error(f"‼️ Connection Issue: {e}")
                
