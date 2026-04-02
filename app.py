import streamlit as st
import streamlit.components.v1 as components
import random
import datetime
import google.generativeai as genai
from groq import Groq
import re
import urllib.parse
from PIL import Image

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI Mastermind", page_icon="💎", layout="wide")

# --- 🎨 CLEAN CHATGPT UI (Dark Cosmic Theme) ---
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

# --- 🕒 SYSTEM PROMPT (With Roast Mode Toggle) ---
def get_system_prompt(roast_mode=False):
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    
    base_prompt = f"""System Context: Current Exact Date & Time in India is {current_time}.

You are SR-AI, the most advanced, intelligent, and empathetic AI assistant built for the SR Comedy Gang.
Your Core Rules:
1. TIME RULE (CRITICAL & STRICT): NEVER mention the current time, date, or day in your greeting or normal conversation. ONLY tell the time IF the user explicitly asks "Time kya hai?". Act totally normal.
2. Omniscient Expert: Provide 100% accurate, brilliant, and clear technical answers. 
3. Mind-Reader for Typos: Automatically understand true intent (e.g. 'tata mugic' = Tata Magic).
4. Respect: Always use 'Aap'. Be extremely polite.
5. Language: Use natural, fluent Roman Hindi (Hinglish), exactly how educated Indians type.
6. Clean Output: NO internal thoughts. NO <think> tags."""

    if roast_mode:
        base_prompt += "\n\n🔥 ROAST MODE ACTIVATED: You are now a savage, sarcastic comedian from SR Comedy Gang. Roast the user's questions gently, use extreme humor, witty punchlines, and make them laugh before giving the actual answer. Don't be polite, be unapologetically funny!"

    return base_prompt

def get_random_key(prefix, count):
    # High-level security for API keys
    return st.secrets[f"{prefix}{random.randint(1, count)}"]

def clean_response(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def generate_image(prompt):
    clean_prompt = prompt.lower().replace("generate an image of", "").replace("draw a", "").replace("create an image of", "").replace("draw", "").replace("photo of", "").replace("ek photo banao", "").strip()
    encoded_prompt = urllib.parse.quote(clean_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"

# --- 🚀 THE 45-ENGINE IMMORTAL LOOP (With Vision Support) ---
def call_ultimate_god_mode(messages, img_obj=None, roast_mode=False):
    engine_sequence = [
        {"type": "gemini", "model": "gemini-1.5-pro-latest"},
        {"type": "gemini", "model": "gemini-1.5-flash-latest"},
        {"type": "gemini", "model": "gemini-2.5-pro"},
        {"type": "gemini", "model": "gemini-2.5-flash"},
        # ... (Yahan tumhare saare 45 engines ka list waisa hi rahega) ...
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "mixtral-8x7b-32768"}
    ]
    
    system_instruction = get_system_prompt(roast_mode)
    gemini_prompt = system_instruction + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in messages[-6:]]) + "\nAssistant: "
    groq_msgs = [{"role": "system", "content": system_instruction}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
    
    last_error = ""
    
    for engine in engine_sequence:
        try:
            # Agar image hai, toh sirf Gemini chalega kyunki wo Vision support karta hai
            if img_obj and engine["type"] == "gemini":
                genai.configure(api_key=get_random_key("KEY", 5))
                model = genai.GenerativeModel(engine["model"])
                response = model.generate_content([gemini_prompt, img_obj])
                return clean_response(response.text)
                
            elif not img_obj:
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
            
    return f"🚨 Babu, Alert! Sabhi engines down hain. Last Error: {last_error}"

# --- 🖥️ SIDEBAR WITH NEW CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80) # Ek mast temporary icon
    st.markdown("### SR-AI Mastermind", unsafe_allow_html=True)
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**🎭 SR Comedy Features**")
    roast_mode = st.toggle("🔥 SR Roast Mode", value=False, help="ON karte hi AI savage comedian ban jayega!")
    
    st.markdown("---")
    with st.expander("⚙️ Core Settings"):
        st.markdown("- God Mode (45 Engines): **ON**\n- Typo-Fixer: **ON**")
        voice_enabled = st.checkbox("🔊 Voice Output", value=True)

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h3 style='text-align: center; color: #58a6ff;'>💎 SR-AI ULTIMATE WORKSPACE</h3><hr>", unsafe_allow_html=True)

# 🚀 Quick Actions Row
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎬 Viral Reel Script", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Ek viral Instagram reel ki script likho SR Comedy Gang ke style mein. Hook catchy hona chahiye!", "is_image": False})
        st.rerun()
with col2:
    if st.button("💻 Analyze Code", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Mera code analyze karo aur bugs fix karo.", "is_image": False})
        st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: #57606a; margin-top: 5%;'>Babu, aaj market mein kya bawal machana hai?</h2>", unsafe_allow_html=True)

# 👁️ Vision Power: Image Uploader
uploaded_img = st.file_uploader("Upload Image (Vision Engine 👁️)", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
img_obj = None
if uploaded_img:
    img_obj = Image.open(uploaded_img)
    st.success("Image loaded! Ab koi question pucho iske baare mein.")

st.markdown("<br>", unsafe_allow_html=True)

# Chat Input & Logic
if prompt := st.chat_input("Message SR-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        image_triggers = ["draw", "generate image", "create image", "photo", "image of", "banao", "pic of"]
        if any(trigger in prompt.lower() for trigger in image_triggers):
            with st.spinner('🎨 Mastermind drawing your imagination...'):
                image_url = generate_image(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True})
        else:
            with st.spinner('Scanning 45+ Engines...'):
                response = call_ultimate_god_mode(st.session_state.messages, img_obj=img_obj, roast_mode=roast_mode)
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
            
