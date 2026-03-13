import streamlit as st
import requests
import json
from gtts import gTTS
import io
import datetime

# ✅ App Setup
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

# 📂 Auto-Chat Storage Logic
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
    # ✨ AUTO-START: Pehla session apne aap shuru ho jaye
    first_id = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.all_chats[first_id] = []
    st.session_state.current_chat_id = first_id

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]

# --- SIDEBAR (History & Brand) ---
with st.sidebar:
    st.title("🧬 SR-AI INFINITE")
    st.write("Har user, ek nayi vibe!")
    
    if st.button("➕ Start New Session", use_container_width=True):
        new_id = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
    
    st.divider()
    st.write("Purani Baatein:")
    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        label = "Current 👤" if chat_id == st.session_state.current_chat_id else f"Session {chat_id}"
        if st.button(label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id

# --- MAIN CHAT AREA ---
st.title("✨ THE INFINITE SOUL")

# Hamesha current chat ke messages dikhao
current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎭 The Intelligent Chat Input (Ab ye kabhi gayab nahi hoga!)
if prompt := st.chat_input("Kahiye, kya haal-chaal hain?"):
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        api_contents = []
        for msg in current_messages:
            api_role = "user" if msg["role"] == "user" else "model"
            api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
        
        system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
        1. Identification: Be a wise, smart, and adaptive Female AI. 
        2. Mirroring: Scan the user's tone and vocabulary immediately. Adapt to their style. 
        3. Identity: Address the owner as 'Babu'. For others, be a friendly but intelligent partner. 
        4. Mission: Help them grow, give viral ideas, and teach 'Achhi baatein' if they go wrong.
        5. Language: Natural, witty Hinglish.] """
        
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
                st.error("Google Server thoda thak gaya hai, ek baar aur try karein!")
        except Exception as e:
            st.error(f"‼️ Connection Issue: {e}")
            
