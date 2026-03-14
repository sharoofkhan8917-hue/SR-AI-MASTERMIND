import streamlit as st
import random
import datetime
import google.generativeai as genai
from groq import Groq
import requests
import re
import urllib.parse

# --- 🎯 PAGE CONFIG (Gemini Style) ---
st.set_page_config(page_title="SR-AI", page_icon="✨", layout="wide")

# --- 🎨 THE "GEMINI DARK" UI MAGIC (Custom CSS) ---
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

# --- 🕒 SYSTEM PROMPT ---
def get_system_prompt():
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    ist_time = datetime.datetime.utcnow() + ist_offset
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""Current Exact Date & Time in India: {current_time}.
You are a highly advanced AI assistant. 
1. Conversation Memory: ALWAYS look at the conversation history. Reply naturally.
2. Introduction: If the user says 'Hi' or 'Hello', say: "Hello! Main ek highly advanced AI assistant hoon. Main aaj aapki kaise madad kar sakta hoon?"
3. Live Clock: Use the 'Current Exact Date & Time in India' provided above.
4. Language: ALWAYS reply in polite, fluent Roman Hindi (Hinglish). Mix English/Hindi naturally.
5. Clean Output: NEVER show internal thoughts. NO <think> tags allowed."""

def get_random_key(prefix, count):
    return st.secrets[f"{prefix}{random.randint(1, count)}"]

def clean_response(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

# --- 🎨 IMAGE GENERATOR ENGINE ---
def generate_image(prompt):
    """Ye function text padhkar direct image banayega"""
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    # Using a fast, keyless image generation API for Streamlit
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"
    return image_url

# --- 🧠 ENGINES (Text) ---
def call_fast_engine(messages):
    try:
        client = Groq(api_key=get_random_key("GROQ", 6))
        models_data = client.models.list().data
        available_models = [m.id for m in models_data if 'whisper' not in m.id.lower() and 'vision' not in m.id.lower()]
        available_models.sort(reverse=True)
        api_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
        for model_name in available_models:
            try:
                chat_completion = client.chat.completions.create(messages=api_msgs, model=model_name)
                return clean_response(chat_completion.choices[0].message.content), True
            except: continue 
        return "System down hai.", False
    except Exception as e: return f"Error: {str(e)}", False

def call_smart_engine(messages):
    try:
        genai.configure(api_key=get_random_key("KEY", 5))
        available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods and m.name.startswith('gemini') and not any(x in m.name for x in ['audio', 'tts', 'image', 'embedding', 'video', 'aqa', 'lite'])]
        available_models.sort(reverse=True)
        sorted_models = [m for m in available_models if 'pro' in m] + [m for m in available_models if 'pro' not in m] 
        full_prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in messages[-6:]]) + "\nAssistant: "
        for model_name in sorted_models:
            try:
                model = genai.GenerativeModel(model_name)
                return clean_response(model.generate_content(full_prompt).text), True
            except: continue 
        return "System down hai.", False
    except Exception as e: return f"Error: {str(e)}", False

def call_god_mode(messages):
    ans, success = call_fast_engine(messages)
    if success: return ans
    ans, success = call_smart_engine(messages)
    if success: return ans
    return "🚨 System Overloaded. Please try again later."

# --- 🖥️ SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='gemini-sparkle'>✨ SR-AI GLOBAL</h2>", unsafe_allow_html=True)
    st.markdown("Creator & Admin: **Babu**")
    st.markdown("---")
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br><br><br><br><hr>", unsafe_allow_html=True)
    with st.expander("⚙️ Settings & Menus"):
        st.markdown("- Customize Instructions\n- Theme: **Dark** (Gemini)\n- Clear all chats")

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns([1, 4])
with col1:
    intelligence_mode = st.selectbox("Model", ["✨ SR-Fast", "🧠 SR-Smart", "💎 SR-God Mode"], label_visibility="collapsed")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"], caption="✨ Generated by SR-AI")
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 15%;'>How can I help you today?</h2>", unsafe_allow_html=True)

if prompt := st.chat_input("Message SR-AI (Try 'Draw a flying car')..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Trigger Check: Is the user asking for an image?
        image_triggers = ["draw", "generate image", "create image", "photo of", "image of", "ek photo banao"]
        is_image_request = any(trigger in prompt.lower() for trigger in image_triggers)

        if is_image_request:
            with st.spinner('🎨 Painting your imagination...'):
                image_url = generate_image(prompt)
                st.image(image_url, caption="✨ Generated by SR-AI")
                st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True})
        else:
            with st.spinner('Thinking...'):
                if "Fast" in intelligence_mode: response, _ = call_fast_engine(st.session_state.messages)
                elif "Smart" in intelligence_mode: response, _ = call_smart_engine(st.session_state.messages)
                else: response = call_god_mode(st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
                
