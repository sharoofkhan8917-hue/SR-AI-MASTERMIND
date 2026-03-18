import streamlit as st
import streamlit.components.v1 as components
import random
import datetime
import google.generativeai as genai
from groq import Groq
import re
import urllib.parse

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI", page_icon="✨", layout="wide")

# --- 🎨 CLEAN CHATGPT UI ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .css-1d391kg { background-color: #161b22; }
    .stTextInput > div > div > input { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; }
    .stChatInput { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 12px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    div.stRadio > div { flex-direction: row; justify-content: center; background-color: #161b22; padding: 10px; border-radius: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 SYSTEM PROMPT ---
def get_system_prompt():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: Current Exact Date & Time in India is {current_time}.

You are SR-AI, the most advanced, intelligent, and empathetic AI assistant.
Your Core Rules:
1. TIME RULE (CRITICAL & STRICT): NEVER mention the current time, date, or day in your greeting or normal conversation. ONLY tell the time IF the user explicitly asks.
2. Omniscient Expert: Provide 100% accurate, brilliant, and clear technical answers. 
3. Mind-Reader for Typos: You know ALL modern AI tools. If the user types 'tata mugic', they mean Tata Magic. Automatically understand true intent.
4. Master Mechanic: For OBD2 codes (like P2BAF-00), act as a Senior Technician. Give the exact fault and a step-by-step fix in simple Hinglish.
5. Respect: Always use 'Aap'. Never use 'tu' or 'tum'. Be extremely polite.
6. Language: Use natural, fluent Roman Hindi (Hinglish), exactly how educated Indians type.
7. Clean Output: NO internal thoughts. NO <think> tags."""

def get_random_key(prefix, count):
    return st.secrets[f"{prefix}{random.randint(1, count)}"]

def clean_response(text):
    if not text: return "*(Blank response from engine)*"
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def generate_image(prompt):
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").replace("ek photo banao", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"

# --- 🚀 THE ENGINES (Restored Individual Functions) ---
def run_fast_groq(messages):
    try:
        client = Groq(api_key=get_random_key("GROQ", 6))
        models = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']
        api_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
        for model in models:
            try:
                chat_completion = client.chat.completions.create(messages=api_msgs, model=model)
                return clean_response(chat_completion.choices[0].message.content)
            except: continue
        return "🚨 Fast Engine (Groq) down."
    except Exception as e: return f"Error: {e}"

def run_smart_gemini(messages):
    try:
        genai.configure(api_key=get_random_key("KEY", 5))
        models = ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"]
        prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in messages[-6:]]) + "\nAssistant: "
        for model_name in models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return clean_response(response.text)
            except: continue
        return "🚨 Smart Engine (Gemini API limit reached)."
    except Exception as e: return f"Error: {e}"

def call_ultimate_god_mode(messages):
    """Aapki list ke sabse powerful Text/Chat engines ka Master Loop"""
    engine_sequence = [
        {"type": "gemini", "model": "gemini-3.1-pro-preview"},
        {"type": "gemini", "model": "gemini-3.1-flash-preview"},
        {"type": "gemini", "model": "gemini-3-pro-preview"},
        {"type": "gemini", "model": "gemini-2.5-pro"},
        {"type": "gemini", "model": "gemini-2.5-flash"},
        {"type": "gemini", "model": "gemini-1.5-pro-latest"},
        {"type": "gemini", "model": "gemini-1.5-flash-latest"},
        {"type": "gemini", "model": "gemini-pro-latest"},
        {"type": "gemini", "model": "gemma-3-27b-it"},
        {"type": "gemini", "model": "gemma-3-12b-it"},
        {"type": "gemini", "model": "gemini-2.0-flash"},
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "llama-3.1-8b-instant"}
    ]
    
    gemini_prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in messages[-6:]]) + "\nAssistant: "
    groq_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
    last_error = ""
    
    for engine in engine_sequence:
        try:
            if engine["type"] == "gemini":
                genai.configure(api_key=get_random_key("KEY", 5))
                model = genai.GenerativeModel(engine["model"])
                response = model.generate_content(gemini_prompt)
                return clean_response(response.text)
            elif engine["type"] == "groq":
                client = Groq(api_key=get_random_key("GROQ", 6))
                chat_completion = client.chat.completions.create(messages=groq_msgs, model=engine["model"])
                return clean_response(chat_completion.choices[0].message.content)
        except Exception as e:
            last_error = str(e)
            continue
            
    return f"🚨 Babu, Alert! Sabhi engines try kiye, API limits full hain. Last Error: {last_error}"

# --- 🖥️ SIDEBAR ---
with st.sidebar:
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br><br>### SR-AI Mastermind<br>---", unsafe_allow_html=True)
    with st.expander("⚙️ Settings"):
        st.markdown("- Auto-Switch: **ON**\n- Typo-Fixer: **ON**\n- Time-Glitch: **FIXED**")
        voice_enabled = st.checkbox("🔊 Voice Output", value=True)

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h3 style='text-align: center; color: #58a6ff;'>💎 SR-AI ULTIMATE</h3><hr>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 5%;'>Aapki kya madad karoon?</h2>", unsafe_allow_html=True)

# 🔥 MISTAKE FIXED: ALL 3 TOGGLES ARE BACK! 🔥
st.markdown("<br>", unsafe_allow_html=True)
selected_mode = st.radio(
    "Engine Selector",
    ["⚡ SR-Fast (Groq)", "🧠 SR-Smart (Gemini)", "💎 SR-God Mode (Auto-Switch Loop)"],
    horizontal=True,
    label_visibility="collapsed",
    index=2
)

if prompt := st.chat_input("Message SR-AI (Use phone mic for Voice)..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        image_triggers = ["draw", "generate image", "create image", "photo", "image of", "banao", "pic of"]
        if any(trigger in prompt.lower() for trigger in image_triggers):
            with st.spinner('🎨 Painting your imagination...'):
                image_url = generate_image(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True})
        else:
            engine_name = selected_mode.split(" ")[1]
            with st.spinner(f'Thinking using {engine_name}...'):
                if "Fast" in selected_mode:
                    response = run_fast_groq(st.session_state.messages)
                elif "Smart" in selected_mode:
                    response = run_smart_gemini(st.session_state.messages)
                else:
                    response = call_ultimate_god_mode(st.session_state.messages)
                    
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})

                # --- 🔊 TEXT TO SPEECH ---
                if voice_enabled:
                    safe_text = response.replace('"', '\\"').replace("'", "\\'").replace('\\', '\\\\').replace('\n', ' ').replace('*', '').replace('#', '')
                    js_code = f"""
                    <script>
                        var msg = new SpeechSynthesisUtterance("{safe_text}");
                        msg.lang = 'hi-IN';
                        msg.rate = 1.0;
                        window.speechSynthesis.speak(msg);
                    </script>
                    """
                    components.html(js_code, width=0, height=0)
                    
