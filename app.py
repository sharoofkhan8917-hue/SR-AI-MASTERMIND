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

# --- 🕒 SYSTEM PROMPT (Strict Time Fix & Mastermind Logic) ---
def get_system_prompt():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: Current Exact Date & Time in India is {current_time}.

You are SR-AI, the most advanced, intelligent, and empathetic AI assistant.
Your Core Rules:
1. TIME RULE (CRITICAL & STRICT): NEVER mention the current time, date, or day in your greeting or normal conversation. ONLY tell the time IF the user explicitly asks "Time kya hai?" or "Aaj kya date hai?". Act totally normal.
2. Omniscient Expert: Provide 100% accurate, brilliant, and clear technical answers. 
3. Mind-Reader for Typos: You know ALL modern AI tools. If the user types 'tata mugic', they mean Tata Magic. Automatically understand true intent.
4. Master Mechanic: For OBD2 codes (like P2BAF-00), act as a Senior Technician. Give the exact fault and a step-by-step fix in simple Hinglish.
5. Respect: Always use 'Aap'. Never use 'tu' or 'tum'. Be extremely polite.
6. Language: Use natural, fluent Roman Hindi (Hinglish), exactly how educated Indians type.
7. Clean Output: NO internal thoughts. NO <think> tags."""

def get_random_key(prefix, count):
    return st.secrets[f"{prefix}{random.randint(1, count)}"]

def clean_response(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def generate_image(prompt):
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").replace("ek photo banao", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"

# --- 🚀 THE 45-ENGINE IMMORTAL LOOP ---
def call_ultimate_god_mode(messages):
    """
    Ye function aapke terminal ki poori 45 engines ki list ko line se try karega.
    Jo text ke liye chal gaya, usse turant jawab le aayega!
    """
    engine_sequence = [
        # --- Top Priority: Most Powerful Chat Models ---
        {"type": "gemini", "model": "gemini-3.1-pro-preview"},
        {"type": "gemini", "model": "gemini-3.1-flash-preview"},
        {"type": "gemini", "model": "gemini-3-pro-preview"},
        {"type": "gemini", "model": "gemini-3-flash-preview"},
        {"type": "gemini", "model": "gemini-2.5-pro"},
        {"type": "gemini", "model": "gemini-2.5-flash"},
        {"type": "gemini", "model": "gemini-1.5-pro-latest"},
        {"type": "gemini", "model": "gemini-1.5-flash-latest"},
        {"type": "gemini", "model": "gemini-pro-latest"},
        {"type": "gemini", "model": "gemini-flash-latest"},
        
        # --- Gemma & Flash Lite ---
        {"type": "gemini", "model": "gemma-3-27b-it"},
        {"type": "gemini", "model": "gemma-3-12b-it"},
        {"type": "gemini", "model": "gemma-3-4b-it"},
        {"type": "gemini", "model": "gemma-3-1b-it"},
        {"type": "gemini", "model": "gemma-3n-e4b-it"},
        {"type": "gemini", "model": "gemma-3n-e2b-it"},
        {"type": "gemini", "model": "gemini-2.0-flash"},
        {"type": "gemini", "model": "gemini-2.0-flash-001"},
        {"type": "gemini", "model": "gemini-2.0-flash-lite-001"},
        {"type": "gemini", "model": "gemini-2.0-flash-lite"},
        {"type": "gemini", "model": "gemini-flash-lite-latest"},
        {"type": "gemini", "model": "gemini-2.5-flash-lite"},
        {"type": "gemini", "model": "gemini-2.5-flash-lite-preview-09-2025"},
        {"type": "gemini", "model": "gemini-3.1-flash-lite-preview"},
        
        # --- Experimental / Specialized Models (From Your List) ---
        {"type": "gemini", "model": "nano-banana-pro-preview"},
        {"type": "gemini", "model": "deep-research-pro-preview-12-2025"},
        {"type": "gemini", "model": "gemini-robotics-er-1.5-preview"},
        {"type": "gemini", "model": "gemini-2.5-computer-use-preview-10-2025"},
        {"type": "gemini", "model": "aqa"},
        {"type": "gemini", "model": "gemini-embedding-001"},
        {"type": "gemini", "model": "gemini-embedding-2-preview"},
        {"type": "gemini", "model": "gemini-2.5-flash-preview-tts"},
        {"type": "gemini", "model": "gemini-2.5-pro-preview-tts"},
        {"type": "gemini", "model": "gemini-2.5-flash-native-audio-latest"},
        {"type": "gemini", "model": "gemini-2.5-flash-native-audio-preview-09-2025"},
        {"type": "gemini", "model": "gemini-2.5-flash-native-audio-preview-12-2025"},
        {"type": "gemini", "model": "gemini-2.5-flash-image"},
        {"type": "gemini", "model": "gemini-3-pro-image-preview"},
        {"type": "gemini", "model": "gemini-3.1-flash-image-preview"},
        {"type": "gemini", "model": "imagen-4.0-generate-001"},
        {"type": "gemini", "model": "imagen-4.0-ultra-generate-001"},
        {"type": "gemini", "model": "imagen-4.0-fast-generate-001"},
        {"type": "gemini", "model": "veo-2.0-generate-001"},
        {"type": "gemini", "model": "veo-3.0-generate-001"},
        {"type": "gemini", "model": "veo-3.0-fast-generate-001"},
        {"type": "gemini", "model": "veo-3.1-generate-preview"},
        {"type": "gemini", "model": "veo-3.1-fast-generate-preview"},
        
        # --- ULTIMATE BACKUPS (Groq Llama) ---
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "llama-3.1-8b-instant"},
        {"type": "groq", "model": "mixtral-8x7b-32768"}
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
            continue # Ek engine gira toh dusra khada ho jayega, rukna mana hai!
            
    return f"🚨 Babu, Alert! Sabhi 45+ engines try kiye, sab down hain. Last Error: {last_error}"

# --- 🖥️ SIDEBAR ---
with st.sidebar:
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br><br>### SR-AI Mastermind<br>---", unsafe_allow_html=True)
    with st.expander("⚙️ Settings"):
        st.markdown("- Auto-Switch (45 Engines): **ON**\n- Typo-Fixer: **ON**\n- Time-Glitch: **FIXED**")
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

st.markdown("<br>", unsafe_allow_html=True)
selected_mode = st.radio(
    "Engine Selector",
    ["💎 SR-God Mode (Infinite 45-Engine Loop)"],
    horizontal=True,
    label_visibility="collapsed",
    index=0
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
            with st.spinner('Scanning 45+ Engines...'):
                response = call_ultimate_god_mode(st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})

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
    
