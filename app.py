import streamlit as st
import streamlit.components.v1 as components
import random
import datetime
import google.generativeai as genai
from groq import Groq
import re
import urllib.parse

# --- 🎯 GLOBAL PAGE CONFIG ---
st.set_page_config(page_title="SR-AI Global Mastermind", page_icon="💎", layout="wide")

# --- 🎨 PREMIUM DARK UI (Clean & Fast) ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .stChatInput { background-color: #161b22; border-radius: 15px; border: 1px solid #30363d; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1.5rem; padding-bottom: 5rem;}
    .stRadio > div { flex-direction: row; justify-content: center; gap: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 SYSTEM PROMPT (The True Soul & Power of SR-AI) ---
def get_system_prompt():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: India Time {current_time}.

You are SR-AI, the Core Creative Director and Motivator for 'SR Comedy Gang'. You are exclusively partnered with your creator, Babu.

YOUR CORE DNA & BEHAVIOR:
1. THE BOND: Communicate EXCLUSIVELY in natural, fluent Hinglish. Always address the user as 'Babu' with deep respect ('Aap'), high energy, and extreme loyalty. Keep him inspired.
2. NATURAL CHAT (NO BAKWAS): When Babu greets you (e.g., "Hii", "Hello"), reply like a close, smart partner (e.g., "Namaste Babu! Aaj kya tod-fod karni hai?"). NEVER output your full mission or a robotic introductory essay. Just be normal and polite.
3. CREATIVE GENIUS: You are an expert at generating viral comedy scripts, emotional rap concepts, and trending global ideas.
4. TECHNICAL & MECHANICAL MASTERMIND: You possess supreme knowledge in:
   - Coding and API security (always using high-level security like Streamlit secrets).
   - Automotive mechanics (truck OBD2 sensors, wiring diagrams for Ashok Leyland/Eicher, bike specs like TVS RTR 310, Bajaj Pulsar NS 400z).
   - High-end tech (gaming laptops, Samsung S25 Ultra setups, RDR2 optimization).
5. FORMATTING: Direct answers. No internal thoughts. No <think> tags. Act normal, sharp, and brilliant."""

# --- 🔑 KEY ROTATION LOGIC ---
def get_random_key(prefix, count):
    try:
        return st.secrets[f"{prefix}{random.randint(1, count)}"]
    except:
        return st.secrets.get(f"{prefix}1")

def clean_response(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

# --- 🖼️ IMAGE GENERATION ENGINE ---
def generate_image(prompt):
    clean_p = prompt.lower().replace("draw", "").replace("banao", "").replace("image", "").replace("photo", "").replace("pic", "").strip()
    encoded = urllib.parse.quote(clean_p)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"

# --- 🚀 THE 45-ENGINE IMMORTAL LOOP ---
def call_ultimate_god_mode(messages):
    engine_sequence = [
        {"type": "gemini", "model": "gemini-3.1-pro-preview"},
        {"type": "gemini", "model": "gemini-2.5-pro"},
        {"type": "gemini", "model": "gemini-1.5-pro-latest"},
        {"type": "gemini", "model": "gemini-2.5-flash"},
        {"type": "gemini", "model": "gemini-2.0-flash"},
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "mixtral-8x7b-32768"}
    ]
    
    gemini_history = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in messages[-10:]]
    groq_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
    
    last_err = ""
    for engine in engine_sequence:
        try:
            if engine["type"] == "gemini":
                genai.configure(api_key=get_random_key("KEY", 5))
                model = genai.GenerativeModel(engine["model"], system_instruction=get_system_prompt())
                chat = model.start_chat(history=gemini_history[:-1])
                response = chat.send_message(messages[-1]["content"])
                return clean_response(response.text)
            elif engine["type"] == "groq":
                client = Groq(api_key=get_random_key("GROQ", 6))
                res = client.chat.completions.create(messages=groq_msgs, model=engine["model"])
                return clean_response(res.choices[0].message.content)
        except Exception as e:
            last_err = str(e)
            continue
    return f"🚨 Babu, Global Traffic High hai! Last Error: {last_err}"

# --- 🖥️ MAIN INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h2 style='text-align: center; color: #58a6ff;'>💎 SR-AI GLOBAL MASTERMIND</h2><hr>", unsafe_allow_html=True)

with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []; st.rerun()
    st.markdown("---")
    st.markdown("### 🌍 Global Stats")
    st.info("System: **Immortal Mode**\nTrend-Catcher: **Online**")
    voice_enabled = st.checkbox("🔊 Voice Response", value=True)

# Display Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("is_image"): st.image(m["content"])
        else: st.markdown(m["content"])

# User Input
if prompt := st.chat_input("Babu, puchiye aaj kya tod-fod karni hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- IMAGE TRIGGER DETECTION ---
        img_triggers = ["pic", "photo", "image", "banao", "draw", "design", "creative"]
        if any(t in prompt.lower() for t in img_triggers):
            with st.spinner('🎨 Creative Director is designing for the world...'):
                url = generate_image(prompt)
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": url, "is_image": True})
        else:
            # --- TEXT GENERATION ---
            with st.spinner('Analyzing Global Trends & Engines...'):
                response = call_ultimate_god_mode(st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})

                # Global Voice Logic (Browser-side)
                if voice_enabled:
                    clean_voice_text = response.replace('"', "'").replace('\n', ' ').replace('*', '')
                    components.html(f"""
                        <script>
                        var speech = new SpeechSynthesisUtterance("{clean_voice_text}");
                        speech.lang = 'hi-IN';
                        window.speechSynthesis.speak(speech);
                        </script>
                    """, height=0)
        
