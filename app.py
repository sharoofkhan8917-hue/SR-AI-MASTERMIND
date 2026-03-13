import streamlit as st
import requests
import json
import asyncio
import edge_tts
import random
import re
import datetime

# ✅ 1. App Setup & Premium Branding
st.set_page_config(page_title="SR-AI Intelligent", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1 { color: #FFD700 !important; text-align: center; font-family: 'Poppins'; text-shadow: 2px 2px 10px rgba(255,215,0,0.2); }
    .stChatMessage.user { background-color: #1E293B !important; border-radius: 15px; border: 1px solid #334155; }
    .stChatMessage.assistant { background-color: #0F172A !important; border-radius: 15px; border: 1px solid #FFD700; box-shadow: 0px 0px 15px rgba(255,215,0,0.1); }
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 2px solid #FFD700; }
    .stButton>button { border-radius: 20px !important; background-color: #FFD700 !important; color: black !important; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); background-color: #FACC15 !important; }
    </style>
    """, unsafe_allow_html=True)

# 🔒 2. Privacy Guard (Data Leak Protection)
def privacy_guard(text):
    # Phone numbers, Emails aur sensitive patterns mask karega
    text = re.sub(r'\d{10}', '[HIDDEN_NUMBER]', text)
    text = re.sub(r'\S+@\S+', '[HIDDEN_EMAIL]', text)
    return text

# 🔑 3. Dynamic Key Loading (Support for 36+ Keys)
def get_all_keys(prefix):
    return [st.secrets[k] for k in st.secrets if k.startswith(prefix)]

g_keys = get_all_keys("KEY")        # Google
gr_keys = get_all_keys("GROQ_KEY")   # Groq
c_keys = get_all_keys("CEREBRAS_KEY") # Cerebras (Warp Speed)
t_keys = get_all_keys("TOGETHER_KEY") # Together
o_keys = get_all_keys("OPENAI_KEY")   # OpenAI

# 🎙️ 4. Voice Engine (Diva Speed)
async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("reply.mp3")

# --- SIDEBAR (Triple Mode Selection) ---
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>🏴 SR-AI GLOBAL</h2>", unsafe_allow_html=True)
    st.write("### 🔥 SR Comedy Gang")
    
    # Membership Check
    if "is_pro" not in st.session_state: st.session_state.is_pro = False
    m_key = st.text_input("🔑 Membership Key:", type="password", help="Enter key for Pro Mode")
    if m_key == "SR_GANG_2026": # Aapka Secret Code
        st.session_state.is_pro = True
        st.success("👑 Pro Membership Active!")
    
    st.divider()
    
    # 🧬 Engine Selection (Aapki Photo Jaisa Setup)
    st.write("### Choose Your Engine")
    mode = st.radio(
        "Select Mindset:",
        ["⚡ फ़ास्ट (Fast)", "🧠 सूझ-बूझ वाला (Smart)", "💎 Pro (Mastermind)"],
        index=0
    )
    
    if "Pro" in mode and not st.session_state.is_pro:
        st.error("Babu, Pro Mode locked hai! 🔒")
        st.info("Pay ₹99 to UPI: babu@upi & get Key")
        mode = "⚡ फ़ास्ट (Fast)" # Force back to free

    st.divider()
    if st.button("➕ Fresh Brainstorm"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT AREA ---
st.markdown("<h1>✨ SR-AI INTELLIGENT</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

# Show Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ✍️ Input Logic
if prompt := st.chat_input("Babu, aaj kya kamaal karna hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # Clean the data before sending to any API
    safe_prompt = privacy_guard(prompt)

    with st.chat_message("assistant"):
        ai_reply = ""
        
        # --- ENGINE LOGIC ---
        # 1. FAST MODE (Groq or Cerebras)
        if "फ़ास्ट" in mode:
            all_fast = gr_keys + c_keys
            if all_fast:
                try:
                    k = random.choice(all_fast)
                    # Simple API call to Groq/Cerebras (OpenAI compatible)
                    resp = requests.post("https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {k}"},
                        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": safe_prompt}]}, timeout=5)
                    ai_reply = resp.json()['choices'][0]['message']['content']
                except: pass

        # 2. SMART MODE (Gemini Flash or Together)
        elif "सूझ-बूझ" in mode:
            if g_keys:
                try:
                    k = random.choice(g_keys)
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k}"
                    resp = requests.post(url, json={"contents": [{"parts": [{"text": safe_prompt}]}]}, timeout=10)
                    ai_reply = resp.json()['candidates'][0]['content']['parts'][0]['text']
                except: pass

        # 3. PRO MODE (Gemini Pro or OpenAI)
        elif "Pro" in mode:
            premium_keys = g_keys + o_keys
            if premium_keys:
                try:
                    k = random.choice(premium_keys)
                    # Using Gemini 1.5 Pro for Mastermind tasks
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={k}"
                    resp = requests.post(url, json={"contents": [{"parts": [{"text": safe_prompt}]}]}, timeout=15)
                    ai_reply = resp.json()['candidates'][0]['content']['parts'][0]['text']
                except: pass

        if not ai_reply: ai_reply = "Babu, lagta hai network jam hai! Ek baar phir try karein. ✨"

        st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        asyncio.run(generate_voice(ai_reply))
        st.audio("reply.mp3")
        
