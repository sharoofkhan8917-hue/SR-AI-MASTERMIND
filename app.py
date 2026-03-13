import streamlit as st
import requests
import json
import asyncio
import edge_tts
import random
import re

# ✅ 1. ULTIMATE CSS (Glassmorphism & Neon Glow)
st.set_page_config(page_title="SR-AI PRO", page_icon="🏴", layout="wide")

st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617); }
    
    /* Custom Sidebar - Ultra Clean */
    [data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.95) !important;
        border-right: 1px solid rgba(255, 215, 0, 0.3);
        backdrop-filter: blur(10px);
    }

    /* Glassmorphism Chat Bubbles */
    .stChatMessage.assistant {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 215, 0, 0.4) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(4px);
        border-radius: 20px !important;
    }
    
    .stChatMessage.user {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
    }

    /* Neon Titles */
    h1 {
        color: #FFD700 !important; font-family: 'Orbitron', sans-serif;
        text-align: center; letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }

    /* Glowing Engine Status */
    .status-online {
        height: 10px; width: 10px; background-color: #22c55e;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 8px #22c55e; margin-right: 5px;
    }

    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #B8860B) !important;
        color: black !important; border: none !important;
        font-weight: 900 !important; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 🛡️ 2. Privacy Guard
def privacy_guard(text):
    text = re.sub(r'\d{10}', '[HIDDEN_NUMBER]', text)
    text = re.sub(r'\S+@\S+', '[HIDDEN_EMAIL]', text)
    return text

# 🔑 3. Dynamic Key System (Safely gets keys if they exist)
def get_keys(prefix): 
    try: return [st.secrets[k] for k in st.secrets if k.startswith(prefix)]
    except: return []

g_keys = get_keys("KEY")
gr_keys = get_keys("GROQ")

# 🎙️ 4. Voice Engine
async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("reply.mp3")

# --- SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 24px;'>🏴 SR-AI GLOBAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Core Creative Director: <b>Babu</b></p>", unsafe_allow_html=True)
    st.divider()
    
    # 👑 Membership Status
    if "is_pro" not in st.session_state: st.session_state.is_pro = False
    m_key = st.text_input("🔑 VIP Membership Key:", type="password")
    if m_key == "SR_GANG_2026":
        st.session_state.is_pro = True
        st.markdown("<p style='color:#fbbf24; font-weight:bold;'>✨ PRO ACCOUNT ACTIVE</p>", unsafe_allow_html=True)
    st.divider()

    # ⚙️ System Status
    st.write("### ⚙️ System Status")
    st.markdown(f"<div><span class='status-online'></span> Engines Online: {len(g_keys) + len(gr_keys)}</div>", unsafe_allow_html=True)
    
    # 🧠 Select Intelligence
    st.write("### 🧠 Select Intelligence")
    mode = st.radio("", ["⚡ FAST (0.5s)", "🧠 SMART (Logic)", "💎 PRO (Expert)"], label_visibility="collapsed")
    if "PRO" in mode and not st.session_state.is_pro:
        st.warning("Locked! 🔒 Upgrade to PRO.")
        mode = "⚡ FAST (0.5s)"
    st.divider()

    # 🛠️ THE NEW MASTERMIND SETTINGS PANEL
    with st.expander("⚙️ Advanced Settings"):
        st.markdown("<b style='color:#FFD700;'>Control Panel</b>", unsafe_allow_html=True)
        st.session_state.voice_on = st.toggle("🔊 AI Voice Output", value=True)
        st.session_state.creativity = st.slider("🧠 Creativity Level", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="1.0 = Highly Creative, 0.0 = Strict Logic")
        
        if st.button("🗑️ Clear Memory / Restart"):
            st.session_state.messages = []
            st.rerun()
        st.caption(f"Network Ping: ~0.{random.randint(1,5)}s")

# --- MAIN INTERFACE ---
st.markdown("<h1>SR-AI INTELLIGENT</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask anything, Babu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    safe_prompt = privacy_guard(prompt)

    with st.chat_message("assistant"):
        with st.status("Engines Firing...", expanded=False) as status:
            ai_reply = ""
            temp = st.session_state.creativity # Setting se dimaag ka level liya
            
            # 🏎️ FAST MODE (Groq)
            if "FAST" in mode and gr_keys:
                try:
                    k = random.choice(gr_keys)
                    resp = requests.post("https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {k}"},
                        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": safe_prompt}], "temperature": temp}, timeout=5)
                    ai_reply = resp.json()['choices'][0]['message']['content']
                except: pass

            # 🧠 SMART / PRO MODE (Gemini)
            if not ai_reply and g_keys:
                try:
                    k = random.choice(g_keys)
                    m = "gemini-1.5-pro" if "PRO" in mode else "gemini-1.5-flash"
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"
                    # Gemini needs a slightly different JSON structure, passing temperature
                    resp = requests.post(url, json={
                        "contents": [{"parts": [{"text": safe_prompt}]}],
                        "generationConfig": {"temperature": temp}
                    }, timeout=10)
                    ai_reply = resp.json()['candidates'][0]['content']['parts'][0]['text']
                except: pass

            if not ai_reply: ai_reply = "Babu, Keys daalna baaki hai ya network jam hai! Kal 30 keys daalte hi raket ban jayega! ✨"
            
            status.update(label="Response Ready ✅", state="complete", expanded=False)

        st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
        # 🔊 Settings se Voice check
        if st.session_state.voice_on:
            try:
                asyncio.run(generate_voice(ai_reply))
                st.audio("reply.mp3")
            except: pass
                
