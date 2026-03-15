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
    .stSelectbox > div > div > div { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; }
    .stChatInput { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 12px; }
    .stButton > button { background-color: #1f2937; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; transition: 0.3s; }
    .stButton > button:hover { background-color: #2d3748; border-color: #58a6ff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# --- 🕒 SYSTEM PROMPT (Mind-Reader & Expert) ---
def get_system_prompt():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: Current Exact Date & Time in India is {current_time}.

You are SR-AI, the most advanced, intelligent, and empathetic AI assistant.
Your Core Rules:
1. Omniscient Expert: Provide 100% accurate, brilliant, and clear technical answers. 
2. Mind-Reader for Typos (CRITICAL): Users will make spelling mistakes (e.g., 'tata mugic' = Tata Magic, 'sujuki' = Suzuki, 'maruti sutuki' = Maruti Suzuki). NEVER lecture them on spelling. Automatically understand their true intent and give the exact technical answer directly.
3. Master Mechanic: If given an OBD2 code (like P2BAF-00 or P206A-08), act as a Senior Technician. Give the exact fault, reasons, and a step-by-step fix in simple Hinglish.
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

# --- 🚀 THE IMMORTAL AUTO-SWITCH ENGINE ---
def call_ultimate_god_mode(messages):
    """
    Ye function bina ruke har ek free/powerful engine try karega jab tak sahi jawab na mil jaye!
    """
    # List of all available powerful free engines (Gemini first, then Groq)
    engine_sequence = [
        {"type": "gemini", "model": "gemini-1.5-pro-latest"},
        {"type": "gemini", "model": "gemini-1.5-flash-latest"},
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "llama-3.1-8b-instant"},
        {"type": "groq", "model": "mixtral-8x7b-32768"}
    ]
    
    # Pre-build prompts
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
            continue # Ek fail hua? Bina ruke agle pe jao!
            
    return f"🚨 Babu, Alert! Sabhi 5 engines down hain. Pichla error: {last_error}"

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

# Top Header 
st.markdown("<h3 style='text-align: center; color: #58a6ff;'>💎 SR-AI ULTIMATE ENGINE</h3><hr>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 15%;'>Aapki kya madad karoon?</h2>", unsafe_allow_html=True)

if prompt := st.chat_input("Message SR-AI..."):
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
            with st.spinner('Thinking (Auto-Switching Engines if needed)...'):
                # DIRECTLY CALLING THE ULTIMATE LOOP!
                response = call_ultimate_god_mode(st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
                
