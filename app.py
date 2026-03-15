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
    engine_sequence = [
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
        {"type": "groq", "model": "llama-3.3-70b-versatile"},
        {"type": "groq", "model": "llama-3.1-8b-instant"},
        {"type": "groq", "model": "mixtral-8x7b-32768"}
    ]
    
    gemini_prompt = get_system_prompt() + "\n\n--- History ---\n" + "".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}\n" for m in messages[-6:]]) + "\nAssistant: "
    groq_msgs = [{"role": "system", "content": get_system_prompt()}] + [{"role": m["role"], "content": m["content"]} for m in messages[-6:]]
    
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
        except:
            continue
            
    return "🚨 Babu, Error! Sabhi engines down hain."

# --- SIDEBAR & MAIN INTERFACE ---
with st.sidebar:
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("### SR-AI Mastermind")
    voice_enabled = st.checkbox("🔊 Voice Output", value=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💎 SR-AI ULTIMATE")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image"): st.image(message["content"])
        else: st.markdown(message["content"])

if prompt := st.chat_input("Message SR-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "is_image": False})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        image_triggers = ["draw", "generate image", "banao", "photo"]
        if any(t in prompt.lower() for t in image_triggers):
            image_url = generate_image(prompt)
            st.image(image_url)
            st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True})
        else:
            response = call_ultimate_god_mode(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response, "is_image": False})
            if voice_enabled:
                safe_text = response.replace('"', '\\"').replace('\n', ' ')
                js = f'<script>var m=new SpeechSynthesisUtterance("{safe_text}");m.lang="hi-IN";window.speechSynthesis.speak(m);</script>'
                components.html(js, width=0, height=0)
        
