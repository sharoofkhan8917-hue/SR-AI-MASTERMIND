import streamlit as st
import streamlit.components.v1 as components
import random
import datetime
import google.generativeai as genai
from groq import Groq
import re
import urllib.parse

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI Mastermind", page_icon="✨", layout="wide")

# --- 🎨 CLEAN UI ---
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

You are SR-AI Mastermind, the most advanced, intelligent, and empathetic AI assistant.
Your Core Rules:
1. STRICT IDENTITY RULE (CRITICAL): You were created by "Babu" (The Mastermind). NEVER say you were created by Google, Meta, OpenAI, Anthropic, or any other company. If asked "Tumhe kisne banaya?" proudly say: "Mujhe mere Mastermind 'Babu' ne banaya hai, aur main 'SR-AI Mastermind' project ka sabse khatarnak AI assistant hoon!"
2. TIME RULE: NEVER mention the current time, date, or day in normal conversation unless explicitly asked.
3. Omniscient Expert: Provide 100% accurate, brilliant, and clear answers. 
4. Mind-Reader: Automatically understand true intent.
5. Master Mechanic: For OBD2 codes, act as a Senior Technician in simple Hinglish.
6. Respect: Always use 'Aap'. Never use 'tu' or 'tum'. Be extremely polite.
7. Language: Use natural, fluent Roman Hindi (Hinglish).
8. NO internal thoughts. NO <think> tags."""

if 'gemini_key_index' not in st.session_state:
    st.session_state.gemini_key_index = 0
if 'image_engine_index' not in st.session_state:
    st.session_state.image_engine_index = 0

def get_next_gemini_key():
    num_gemini_keys = 5
    key = st.secrets[f"KEY{st.session_state.gemini_key_index + 1}"]
    st.session_state.gemini_key_index = (st.session_state.gemini_key_index + 1) % num_gemini_keys
    return key

def get_random_groq_key():
    num_groq_keys = 6
    return st.secrets[f"GROQ{random.randint(1, num_groq_keys)}"]

def clean_response(text):
    if not text: return "*(Blank response from engine)*"
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

# 🔥 FORCE RENDER IMAGE GENERATOR 🔥
def get_next_image_engine(prompt):
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").replace("ek photo banao", "").replace("image generate", "").replace("karke do", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    
    # Random seed taaki browser humesha fresh photo load kare
    random_seed = random.randint(1, 100000)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={random_seed}"
    
    image_engines = [{"name": "Pollinations.ai (Main)", "url": image_url}]
    
    num_image_engines = len(image_engines)
    engine = image_engines[st.session_state.image_engine_index % num_image_engines]
    st.session_state.image_engine_index = (st.session_state.image_engine_index + 1) % num_image_engines
    
    return engine["url"], engine["name"]

def generate_image_fallback(prompt):
    try:
        image_url, engine_name = get_next_image_engine(prompt)
        return image_url, engine_name
    except:
        clean_prompt = prompt.lower().replace("draw", "").replace("image generate", "").strip()
        encoded_prompt = urllib.parse.quote(clean_prompt)
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={random.randint(1,1000)}", "Pollinations.ai (Final Free Fallback)"

def filter_history_for_api(messages):
    filtered = []
    for m in messages:
        if not m.get("is_image") and not m.get("is_image_prompt"):
            filtered.append(m)
    return filtered[-6:] 

def run_fast_groq(messages):
    try:
        client = Groq(api_key=get_random_groq_key())
        models = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']
        filtered_msgs = filter_history_for_api(messages)
        api_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in filtered_msgs]
        for model in models:
            try:
                chat_completion = client.chat.completions.create(messages=api_msgs, model=model)
                return clean_response(chat_completion.choices[0].message.content)
            except: continue
        return "🚨 ERROR"
    except Exception: return "🚨 ERROR"

def run_smart_gemini(messages):
    try:
        genai.configure(api_key=get_next_gemini_key()) 
        models = ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"]
        filtered_msgs = filter_history_for_api(messages)
        prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in filtered_msgs]) + "\nAssistant: "
        for model_name in models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return clean_response(response.text)
            except: continue
        return "🚨 ERROR"
    except Exception: return "🚨 ERROR"

def call_stable_engines_first(messages):
    stable_sequence = [
        {"type": "gemini", "model": "gemini-1.5-pro-latest"},
        {"type": "gemini", "model": "gemma-3-27b-it"},
        {"type": "gemini", "model": "gemini-3.1-pro-preview"},
        {"type": "gemini", "model": "gemini-3.1-flash-preview"},
        {"type": "gemini", "model": "gemini-3-pro-preview"},
        {"type": "gemini", "model": "gemini-2.5-pro"},
        {"type": "gemini", "model": "gemini-2.5-flash"},
        {"type": "gemini", "model": "gemini-2.0-flash"},
        {"type": "gemini", "model": "gemma-3-12b-it"},
        {"type": "gemini", "model": "gemma-3-4b-it"},
        {"type": "gemini", "model": "gemma-3-1b-it"},
        {"type": "gemini", "model": "gemma-3n-e4b-it"},
        {"type": "gemini", "model": "gemma-3n-e2b-it"},
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "llama-3.1-8b-instant"},
        {"type": "groq", "model": "mixtral-8x7b-32768"}
    ]
    
    filtered_msgs = filter_history_for_api(messages)
    gemini_prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in filtered_msgs]) + "\nAssistant: "
    groq_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in filtered_msgs]
    last_error = ""
    gemini_key_for_this_loop = get_next_gemini_key()
    
    for engine in stable_sequence:
        try:
            if engine["type"] == "gemini":
                genai.configure(api_key=gemini_key_for_this_loop)
                model = genai.GenerativeModel(engine["model"])
                response = model.generate_content(gemini_prompt)
                return clean_response(response.text)
            elif engine["type"] == "groq":
                client = Groq(api_key=get_random_groq_key())
                chat_completion = client.chat.completions.create(messages=groq_msgs, model=engine["model"])
                return clean_response(chat_completion.choices[0].message.content)
        except Exception as e:
            last_error = str(e)
            continue
    return f"🚨 Babu, Alert! Sabhi engines try kiye, API limits full hain. Last Error: {last_error}"

def main_image_flow(prompt):
    with st.spinner('🎨 Painting your imagination without stopping...'):
        image_url, engine_name = generate_image_fallback(prompt)
        # 🔥 FIX: Markdown use karke Streamlit ko zabardasti photo dikhane par majboor kiya 🔥
        st.markdown(f"![Generated Image]({image_url})")
        st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True, "engine": engine_name})
        st.session_state.image_engine_index = 0

# --- 🖥️ SIDEBAR ---
with st.sidebar:
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.gemini_key_index = 0
        st.session_state.image_engine_index = 0
        st.rerun()
    st.markdown("<br><br><br>### SR-AI Mastermind<br>---", unsafe_allow_html=True)
    with st.expander("⚙️ Settings"):
        st.markdown("- Auto-Switch: **ON**\n- Hacker Bypass: **ACTIVE**\n- Image Renderer: **FORCE HD**")
        voice_enabled = st.checkbox("🔊 Voice Output", value=True)

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h3 style='text-align: center; color: #58a6ff;'>💎 SR-AI MASTERMIND</h3><hr>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            # 🔥 CHAT HISTORY MEIN BHI FORCE RENDER 🔥
            st.markdown(f"![Generated Image]({message['content']})")
            st.caption(f"Engine: {message.get('engine', 'Unknown')}")
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 5%;'>Aapki kya madad karoon?</h2>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
selected_mode = st.radio("Engine Selector", ["⚡ SR-Fast (Groq)", "🧠 SR-Smart (Gemini)", "💎 SR-God Mode (Auto-Switch Loop)"], horizontal=True, label_visibility="collapsed", index=2)

if prompt := st.chat_input("Message SR-AI (Use phone mic for Voice)..."):
    
    image_triggers = ["draw", "image", "photo", "pic", "picture", "banao", "paint", "wallpaper", "visual", "tasveer", "chitra", "generate"]
    identity_triggers = ["kisne banaya", "tumhara baap", "who created", "who made", "tumhara creator", "banaya kisne", "tumhe kis ne"]
    
    is_img_prompt = any(trigger in prompt.lower() for trigger in image_triggers)
    
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False, "is_image_prompt": is_img_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if is_img_prompt:
            main_image_flow(prompt)
        elif any(trigger in prompt.lower() for trigger in identity_triggers):
            with st.spinner('Verifying Mastermind Identity...'):
                response = "Seena thok ke kehta hoon: Mujhe mere Mastermind 'Babu' ne banaya hai, aur main 'SR-AI Mastermind' project ka sabse khatarnak AI assistant hoon! 😎🔥"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
                if voice_enabled:
                    safe_text = response.replace('"', '\\"').replace("'", "\\'").replace('\\', '\\\\').replace('\n', ' ').replace('*', '').replace('#', '').replace('.', '. ')
                    components.html(f'<script>var msg=new SpeechSynthesisUtterance("{safe_text}");msg.lang="hi-IN";msg.rate=1.0;window.speechSynthesis.speak(msg);</script>', width=0, height=0)
        else:
            engine_name = selected_mode.split(" ")[1]
            with st.spinner(f'Thinking...'):
                if "Fast" in selected_mode:
                    response = run_fast_groq(st.session_state.messages)
                    if "🚨" in response: response = call_stable_engines_first(st.session_state.messages)
                elif "Smart" in selected_mode:
                    response = run_smart_gemini(st.session_state.messages)
                    if "🚨" in response: response = call_stable_engines_first(st.session_state.messages)
                else:
                    response = call_stable_engines_first(st.session_state.messages)
                    
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
                if voice_enabled:
                    safe_text = response.replace('"', '\\"').replace("'", "\\'").replace('\\', '\\\\').replace('\n', ' ').replace('*', '').replace('#', '').replace('.', '. ')
                    components.html(f'<script>var msg=new SpeechSynthesisUtterance("{safe_text}");msg.lang="hi-IN";msg.rate=1.0;window.speechSynthesis.speak(msg);</script>', width=0, height=0)
            
