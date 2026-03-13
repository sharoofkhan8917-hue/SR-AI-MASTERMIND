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
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
    }
    
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
        color: #FFD700 !important;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        letter-spacing: 2px;
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
        color: black !important;
        border: none !important;
        font-weight: 900 !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 🔑 Dynamic Key System
def get_keys(prefix): return [st.secrets[k] for k in st.secrets if k.startswith(prefix)]

# --- SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 24px;'>🏴 SR-AI GLOBAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Core Creative Director: <b>Babu</b></p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Membership Status
    if "is_pro" not in st.session_state: st.session_state.is_pro = False
    m_key = st.text_input("🔑 VIP Membership Key:", type="password")
    if m_key == "SR_GANG_2026":
        st.session_state.is_pro = True
        st.markdown("<p style='color:#fbbf24; font-weight:bold;'>✨ PRO ACCOUNT ACTIVE</p>", unsafe_allow_html=True)
    
    st.divider()

    # 🧬 Engine Health & Selection
    st.write("### ⚙️ System Status")
    st.markdown(f"<div><span class='status-online'></span> Engines Online: {len(get_keys('KEY')) + len(get_keys('GROQ'))}</div>", unsafe_allow_html=True)
    
    st.write("### 🧠 Select Intelligence")
    mode = st.radio("", ["⚡ FAST (0.5s)", "🧠 SMART (Logic)", "💎 PRO (Expert)"], label_visibility="collapsed")
    
    # Pro Lock Logic
    if "PRO" in mode and not st.session_state.is_pro:
        st.warning("Locked! 🔒 Upgrade to PRO.")
        mode = "⚡ FAST (0.5s)"

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

    with st.chat_message("assistant"):
        # Simulated 'Thinking' feel for ultimate professional vibe
        with st.status("Engines Firing...", expanded=False) as status:
            # Logic stays same as v45.0, just adding professional UX
            ai_reply = ""
            # (API Logic here...)
            # For testing, we use a placeholder:
            ai_reply = "Babu, ye system ab ekdum professional ho gaya hai! Ready for the keys? ✨"
            status.update(label="Response Ready ✅", state="complete", expanded=True)

        st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
