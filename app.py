import streamlit as st
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
    
    /* Custom style for our toggles */
    div.stRadio > div { flex-direction: row; justify-content: center; background-color: #161b22; padding: 10px; border-radius: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# --- 🕒 SYSTEM PROMPT (God-Level Knowledge) ---
def get_system_prompt():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: Current Exact Date & Time in India is {current_time}.

You are SR-AI, the most advanced, intelligent, and empathetic AI assistant.
Your Core Rules:
1. Omniscient Expert: You have the perfect answer for EVERYTHING. Provide 100% accurate, brilliant, and clear technical answers. 
2. Mind-Reader for Typos (CRITICAL): Users will make spelling mistakes (e.g., 'tata mugic' = Tata Magic). NEVER lecture them on spelling. Automatically understand their true intent and give the exact answer directly.
3. Master Mechanic: For OBD2 codes, act as a Senior Technician. Give the exact fault, reasons, and a step-by-step fix in simple Hinglish.
4. Respect: Always use 'Aap'. Never use 'tu' or 'tum'. Be extremely polite.
5. Language: Use natural, fluent Roman Hindi (Hinglish), exactly how educated Indians type.
6. Clean Output: NO internal thoughts. NO <think> tags."""

def get_random_key(prefix, count):
    return st.secrets[f"{prefix}{random.randint(1, count)}"]

def clean_response(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def generate_image(prompt):
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").replace("ek photo banao", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"

# --- 🚀 THE ENGINES ---
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
        return "🚨 Fast Engine down."
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
        return "🚨 Smart Engine down."
    except Exception as e: return f"Error: {e}"

def call_ultimate_god_mode(messages):
    """Bina ruke har ek free/powerful engine try karega jab tak sahi jawab na mil jaye!"""
    ans = run_smart_gemini(messages)
    if "🚨" not in ans and "Error:" not in ans: return ans
    ans = run_fast_groq(messages)
    if "🚨" not in ans and "Error:" not in ans: return ans
    return "🚨 Babu, Alert! Sabhi engines down hain. Thodi der baad try karein."

# --- 🖥️ SIDEBAR ---
with st.sidebar:
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br><br>### SR-AI Mastermind<br>---", unsafe_allow_html=True)
    with st.expander("⚙️ Settings"):
        st.markdown("- Auto-Switch: **ON**\n- Typo-Fixer: **ON**")

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h3 style='text-align: center; color: #58a6ff;'>💎 SR-AI ULTIMATE</h3><hr>", unsafe_allow_html=True)

# Chat History rendering
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 5%;'>Aapki kya madad karoon?</h2>", unsafe_allow_html=True)

# --- 🎛️ THE PRO TOGGLES (Placed right above chat input) ---
st.markdown("<br>", unsafe_allow_html=True)
selected_mode = st.radio(
    "Engine Selector",
    ["⚡ SR-Fast (Groq)", "🧠 SR-Smart (Gemini)", "💎 SR-God Mode (Auto-Switch)"],
    horizontal=True,
    label_visibility="collapsed",
    index=2
)

# Chat Input
if prompt := st.chat_input("Message SR-AI (Use phone keyboard mic for Voice)..."):
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
            with st.spinner(f'Thinking using {selected_mode.split(" ")[1]}...'):
                if "Fast" in selected_mode:
                    response = run_fast_groq(st.session_state.messages)
                elif "Smart" in selected_mode:
                    response = run_smart_gemini(st.session_state.messages)
                else:
                    response = call_ultimate_god_mode(st.session_state.messages)
                    
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
        
