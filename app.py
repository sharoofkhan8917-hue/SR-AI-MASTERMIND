import streamlit as st
import requests
import json
import asyncio
import edge_tts
import os
import datetime

# ✅ App Setup
st.set_page_config(page_title="SR-AI Intelligent", page_icon="🧬", layout="wide")

# 🔒 HIGH-SECURITY TIJORI
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets mein key nahi mili!")
    st.stop()

# 🎙️ FUNCTION: Diva Voice
async def generate_fast_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("reply.mp3")

# 📂 Chat Management
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
    first_id = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.all_chats[first_id] = []
    st.session_state.current_chat_id = first_id

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧠 UNSTOPPABLE AI")
    if st.button("➕ Fresh Session (Limit Reset)", use_container_width=True):
        new_id = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat_id = new_id
    st.divider()
    st.info("Tip: Agar AI ruke, toh naya session shuru karein.")

# --- MAIN AREA ---
st.title("✨ SR-AI Intelligent")

current_id = st.session_state.current_chat_id
current_messages = st.session_state.all_chats[current_id]

# Welcome Message
if not current_messages:
    welcome = "Hii, main SR-AI Intelligent hoon. Main taiyar hoon aapke har sawal ka jawab dene ke liye. ✨"
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

        # 🛡️ SUPER BYPASS (Instant replies for common stuff)
        if any(word in p_low for word in ["hi", "hello", "kaise ho"]):
            ai_reply = "Main ekdum mast hoon! Aap sunaiye, aaj kya dhamaal karna hai? ✨"
        elif any(word in p_low for word in ["kisne banaya", "maker", "owner"]):
            ai_reply = "Mujhe Babu (SR Comedy Gang) ne banaya hai. Wo hi mere asli Mastermind hain! 😎"
        
        if not ai_reply:
            # ⚡ LIGHT-WEIGHT API CALL (Only last 6 messages for speed)
            memory_window = current_messages[-6:] 
            api_contents = []
            for msg in memory_window:
                api_role = "user" if msg["role"] == "user" else "model"
                api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
            
            sys_msg = "Identity: SR-AI Intelligent. Creator: Babu. Tone: Wise Female. Use Hinglish."
            api_contents[-1]["parts"][0]["text"] = sys_msg + prompt
            
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
                # Added timeout to prevent long hangs
                response = requests.post(url, json={"contents": api_contents}, timeout=8)
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            except:
                ai_reply = "Babu, lagta hai traffic zyada hai! Ek baar 'Fresh Session' try kijiye ya dobara puchiye. ✨"

        # Final Display
        st.markdown(ai_reply)
        current_messages.append({"role": "assistant", "content": ai_reply})
        asyncio.run(generate_fast_voice(ai_reply))
        st.audio("reply.mp3", format='audio/mp3')
        
