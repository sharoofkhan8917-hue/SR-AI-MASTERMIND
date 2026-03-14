import streamlit as st
import random
import datetime
import google.generativeai as genai
from groq import Groq
import requests
import re

# --- 🎯 PAGE CONFIG (ChatGPT Style) ---
st.set_page_config(page_title="SR-AI", page_icon="✨", layout="wide")

# --- CUSTOM CSS FOR CLEAN LOOK ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# --- 🕒 SYSTEM PROMPT (Logic Wahi, Look Naya) ---
def get_system_prompt():
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    ist_time = datetime.datetime.utcnow() + ist_offset
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    
    return f"""Current Exact Date & Time in India: {current_time}.
You are a highly advanced AI assistant. 
1. Conversation Memory: ALWAYS look at the conversation history. If the user says "Good" or "Thanks", DO NOT repeat your introduction. Reply naturally.
2. Introduction: If the user says 'Hi' or 'Hello' initially, say: "Hello! Main ek highly advanced AI assistant hoon. Main aaj aapki kaise madad kar sakta hoon?"
3. Live Clock: If asked for time/date, use the 'Current Exact Date & Time in India' provided above.
4. Tone: Speak in polite, formal, fluent, and highly professional Hinglish.
5. Clean Output: NEVER show internal thoughts. NO <think> tags allowed."""

def get_random_key(prefix, count):
    key_index = random.randint(1, count)
    return st.secrets[f"{prefix}{key_index}"]

def clean_response(text):
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned_text.strip()

# --- 🧠 MEMORY MANAGER ---
def get_api_messages(messages):
    api_msgs = [{"role": "system", "content": get_system_prompt()}]
    for m in messages[-6:]:
        api_msgs.append({"role": m["role"], "content": m["content"]})
    return api_msgs

def get_gemini_prompt(messages):
    prompt = get_system_prompt() + "\n\n--- Conversation History ---\n"
    for m in messages[-6:]:
        speaker = "User" if m["role"] == "user" else "Assistant"
        prompt += f"{speaker}: {m['content']}\n"
    prompt += "\nAssistant: "
    return prompt

# --- ENGINES (Backend Wahi, Sirf Name Change) ---
def call_fast_engine(messages):
    try:
        current_key = get_random_key("GROQ", 6)
        client = Groq(api_key=current_key)
        models_data = client.models.list().data
        available_models = [m.id for m in models_data if 'whisper' not in m.id.lower() and 'vision' not in m.id.lower()]
        available_models.sort(reverse=True)
        api_msgs = get_api_messages(messages)
        for model_name in available_models:
            try:
                chat_completion = client.chat.completions.create(messages=api_msgs, model=model_name)
                return clean_response(chat_completion.choices[0].message.content), True
            except: continue 
        return "System down hai.", False
    except Exception as e: return f"Error: {str(e)}", False

def call_smart_engine(messages):
    try:
        current_key = get_random_key("KEY", 5)
        genai.configure(api_key=current_key)
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace('models/', '')
                if name.startswith('gemini') and not any(x in name for x in ['audio', 'tts', 'image', 'embedding', 'video', 'aqa', 'lite']):
                    available_models.append(name)
        available_models.sort(reverse=True)
        sorted_models = [m for m in available_models if 'pro' in m] + [m for m in available_models if 'pro' not in m] 
        full_prompt = get_gemini_prompt(messages)
        for model_name in sorted_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                return clean_response(response.text), True
            except: continue 
        return "System down hai.", False
    except Exception as e: return f"Error: {str(e)}", False

def call_universal_api(api_url, current_key, messages, preferred_keyword):
    try:
        headers = {"Authorization": f"Bearer {current_key}"}
        resp = requests.get(f"{api_url}/models", headers=headers, timeout=5)
        if resp.status_code == 200:
            models = [m['id'] for m in resp.json().get('data', [])]
            models.sort(reverse=True)
            api_msgs = get_api_messages(messages)
            for model_name in models:
                if 'vision' in model_name.lower() or 'image' in model_name.lower(): continue
                try:
                    data = {"model": model_name, "messages": api_msgs}
                    chat_resp = requests.post(f"{api_url}/chat/completions", headers={"Authorization": f"Bearer {current_key}", "Content-Type": "application/json"}, json=data, timeout=10)
                    chat_resp.raise_for_status()
                    return clean_response(chat_resp.json()['choices'][0]['message']['content']), True
                except: continue
    except: pass
    return "API failure.", False

def call_god_mode(messages):
    ans, success = call_fast_engine(messages)
    if success: return ans
    ans, success = call_smart_engine(messages)
    if success: return ans
    ans, success = call_universal_api("https://api.cerebras.ai/v1", get_random_key("CEREBRAS", 6), messages, "llama")
    if success: return ans
    ans, success = call_universal_api("https://api.together.xyz/v1", get_random_key("TOGETHER", 6), messages, "llama")
    if success: return ans
    return "🚨 System Overloaded. Please try again later."

# --- 🖥️ SIDEBAR (ChatGPT Style) ---
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
        st.markdown("- Theme: System")
        st.markdown("- Clear all chats")

# --- 💬 MAIN CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Top Model Selector (ChatGPT Style)
col1, col2 = st.columns([1, 4])
with col1:
    intelligence_mode = st.selectbox(
        "Model",
        ["✨ SR-Fast", "🧠 SR-Smart", "💎 SR-God Mode"],
        label_visibility="collapsed"
    )
st.markdown("---")

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Empty State (When no messages)
if len(st.session_state.messages) == 0:
    st.markdown("<h2 style='text-align: center; color: gray; margin-top: 20%;'>How can I help you today?</h2>", unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Message SR-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Thinking...'):
            if "Fast" in intelligence_mode:
                response, _ = call_fast_engine(st.session_state.messages)
            elif "Smart" in intelligence_mode:
                response, _ = call_smart_engine(st.session_state.messages)
            else:
                response = call_god_mode(st.session_state.messages)
                
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
