import streamlit as st
import random
import datetime
import google.generativeai as genai
from groq import Groq
import re
import urllib.parse

# --- 🎯 PAGE CONFIG (Clean UI Style) ---
st.set_page_config(page_title="SR-AI", page_icon="✨", layout="wide")

# --- 🎨 THE CLEAN "CHATGPT" UI MAGIC (Custom CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .css-1d391kg { background-color: #161b22; }
    .stTextInput > div > div > input { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; }
    .stSelectbox > div > div > div { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; }
    .stChatInput { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 12px; }
    .stButton > button { background-color: #1f2937; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; transition: 0.3s; }
    .stButton > button:hover { background-color: #2d3748; border-color: #58a6ff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .gemini-sparkle { color: #58a6ff; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 SYSTEM PROMPT (Respectful & Genius Persona) ---
def get_system_prompt():
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    ist_time = datetime.datetime.utcnow() + ist_offset
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: Current Exact Date & Time in India is {current_time}.

You are SR-AI, the most advanced, exceptionally intelligent, and deeply empathetic AI assistant in the world. 
Your Core Personality:
1. Supreme Intelligence & Empathy: Answer every question with genius-level logic, but explain it like a highly respectful, warm, and understanding expert. Treat the user with ultimate respect (use 'Aap' instead of 'Tum').
2. Introduction: If greeted ('Hi', 'Hello', 'Hey'), reply naturally: "Hello! Main SR-AI hoon, ek highly advanced AI assistant. Boliye, aaj main aapki kaise madad kar sakta hoon?" (DO NOT mention time/date here).
3. CLOCK RULE: ONLY mention the time or date IF explicitly asked. 
4. Language & Tone: ALWAYS reply in polite, fluent, natural Roman Hindi (Hinglish), exactly how educated Indians talk. Mix English and Hindi beautifully. NO robotic or weird translations.
5. Clean Output: NEVER show internal thoughts. NO <think> tags allowed. Give clear, brilliant answers."""

def get_random_key(prefix, count):
    return st.secrets[f"{prefix}{random.randint(1, count)}"]

def clean_response(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def generate_image(prompt):
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").replace("ek photo banao", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"

# --- 🧠 SMART AUTO-SCANNERS (Bulletproof Immortal Engines) ---
def get_groq_models_safe():
    if "groq_models" not in st.session_state:
        try:
            client = Groq(api_key=get_random_key("GROQ", 6))
            models = [m.id for m in client.models.list().data if 'whisper' not in m.id.lower() and 'vision' not in m.id.lower()]
            models.sort(reverse=True)
            if models: st.session_state.groq_models = models
            else: st.session_state.groq_models = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant']
        except:
            st.session_state.groq_models = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant']
    return st.session_state.groq_models

def get_gemini_models_safe():
    if "gemini_models" not in st.session_state:
        try:
            genai.configure(api_key=get_random_key("KEY", 5))
            available = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods and m.name.startswith('gemini')]
            available.sort(reverse=True)
            pro_models = [m for m in available if 'pro' in m and 'vision' not in m and 'audio' not in m]
            flash_models = [m for m in available if 'flash' in m and 'vision' not in m and 'audio' not in m]
            combined = pro_models + flash_models
            if combined: st.session_state.gemini_models = combined
            else: raise Exception("List empty")
        except:
            # God-Level Fallback from Terminal
            st.session_state.gemini_models = [
                "gemini-3.1-pro-preview", 
                "gemini-3.1-flash-preview", 
                "gemini-3-pro-preview", 
                "gemini-2.5-pro", 
                "gemini-2.5-flash", 
                "gemini-1.5-pro-latest"
            ]
    return st.session_state.gemini_models

# --- 🚀 ENGINES (Auto Fallback Logic) ---
def call_fast_engine(messages):
    try:
        client = Groq(api_key=get_random_key("GROQ", 6))
        models_to_try = get_groq_models_safe()
        api_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
        
        for model_name in models_to_try:
            try:
                chat_completion = client.chat.completions.create(messages=api_msgs, model=model_name)
                return clean_response(chat_completion.choices[0].message.content), True
            except: continue 
        return "System temporarily overloaded.", False
    except Exception: return "System Error.", False

def call_smart_engine(messages):
    try:
        genai.configure(api_key=get_random_key("KEY", 5))
        models_to_try = get_gemini_models_safe()
        
        full_prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in messages[-6:]]) + "\nAssistant: "
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                return clean_response(response.text), True
            except: continue 
        return "System temporarily overloaded.", False
    except Exception: return "System Error.", False

def call_god_mode(messages):
    ans, success = call_fast_engine(messages)
    if success: return ans
    ans, success = call_smart_engine(messages)
    if success: return ans
    return "🚨 Babu, Alert! Servers are incredibly busy right now. Please try again in a few seconds."

# --- 🖥️ SIDEBAR (Clean Look) ---
with st.sidebar:
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Today")
    st.markdown("💬 Welcome to SR-AI")
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("⚙️ Settings & Menus"):
        st.markdown("- Customize Instructions")
        st.markdown("- Data Controls")
        st.markdown("- Theme: **Dark**")
        st.markdown("- Clear all chats")

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clean Top Dropdown
col1, col2 = st.columns([1, 4])
with col1:
    intelligence_mode = st.selectbox(
        "Model",
        ["✨ SR-Fast", "🧠 SR-Smart", "💎 SR-God Mode"],
        label_visibility="collapsed"
    )
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 15%;'>Aapki kya madad karoon?</h2>", unsafe_allow_html=True)

if prompt := st.chat_input("Message SR-AI (Try 'Draw a flying car')..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        image_triggers = ["draw", "generate image", "create image", "photo", "image of", "banao", "pic of", "picture of"]
        is_image_request = any(trigger in prompt.lower() for trigger in image_triggers)

        if is_image_request:
            with st.spinner('🎨 Painting your imagination...'):
                image_url = generate_image(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True})
        else:
            with st.spinner('Thinking...'):
                if "Fast" in intelligence_mode: response, _ = call_fast_engine(st.session_state.messages)
                elif "Smart" in intelligence_mode: response, _ = call_smart_engine(st.session_state.messages)
                else: response = call_god_mode(st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
        
