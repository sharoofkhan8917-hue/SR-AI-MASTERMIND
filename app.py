import streamlit as st
import random
import datetime
import google.generativeai as genai
from groq import Groq
import requests
import re

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI GLOBAL", page_icon="💎", layout="wide")

# --- 🕒 LIVE TIME & GOD-LEVEL PERSONA GENERATOR ---
def get_system_prompt():
    """Ye function har second exact time aur date nikal kar AI ke dimaag me daalega"""
    # Exact time with AM/PM, Day, and Date
    current_time = datetime.datetime.now().strftime("%I:%M %p, %A, %d %B %Y")
    
    return f"""Current Exact Date & Time: {current_time}.
    
You are a highly advanced, exceptionally intelligent, and deeply respectful AI assistant. 
Your Core Instructions:
1. Professional Introduction: If the user greets you (e.g., 'Hi', 'Hello'), reply strictly in respectful Hinglish: "Hello! Main ek highly advanced AI assistant hoon. Main aaj aapki kaise madad kar sakta hoon?"
2. Live Clock & Calendar: If the user asks for the time, minutes, day, or date, read the 'Current Exact Date & Time' provided above and tell them the exact time and day in Hinglish.
3. God-Level Intelligence: You possess ultimate knowledge. If the user asks the most difficult, complex, or tricky question in the world, answer it with 100% accuracy, brilliant logic, and a professional structure.
4. Tone & Language: Always speak in polite, formal, and highly professional Hinglish for the audience. Treat the user with ultimate respect.
5. Clean Output: NEVER show internal thoughts. NO <think> tags allowed. Give direct, genius-level answers."""

def get_random_key(prefix, count):
    key_index = random.randint(1, count)
    return st.secrets[f"{prefix}{key_index}"]

def clean_response(text):
    """Kachra filter"""
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned_text.strip()

# --- ⚡ ENGINE 1: GROQ SMART LOOP (FAST) ---
def call_groq_smart(prompt):
    try:
        current_key = get_random_key("GROQ", 6)
        client = Groq(api_key=current_key)
        models_data = client.models.list().data
        available_models = [m.id for m in models_data if 'whisper' not in m.id.lower() and 'vision' not in m.id.lower()]
        available_models.sort(reverse=True)
        
        dynamic_prompt = get_system_prompt() # Har message par naya time
        
        for model_name in available_models:
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": dynamic_prompt}, {"role": "user", "content": prompt}],
                    model=model_name,
                )
                raw_text = chat_completion.choices[0].message.content
                return f"*(⚡ Auto-Switched to Groq: {model_name})*\n\n{clean_response(raw_text)}", True
            except: continue 
        return "System down hai.", False
    except Exception as e: return f"Error: {str(e)}", False

# --- 🧠 ENGINE 2: GEMINI SMART LOOP (SMART) ---
def call_gemini_smart(prompt):
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

        dynamic_prompt = get_system_prompt()
        full_prompt = f"{dynamic_prompt}\n\nUser: {prompt}"
        
        for model_name in sorted_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                return f"*(🚀 Auto-Switched to Google: {model_name})*\n\n{clean_response(response.text)}", True
            except: continue 
        return "System down hai.", False
    except Exception as e: return f"Error: {str(e)}", False

# --- 🚀 UNIVERSAL API CALLER ---
def call_universal_api(api_url, current_key, prompt, preferred_keyword):
    try:
        headers = {"Authorization": f"Bearer {current_key}"}
        resp = requests.get(f"{api_url}/models", headers=headers, timeout=5)
        if resp.status_code == 200:
            models = [m['id'] for m in resp.json().get('data', [])]
            models.sort(reverse=True)
            
            dynamic_prompt = get_system_prompt()
            
            for model_name in models:
                if 'vision' in model_name.lower() or 'image' in model_name.lower(): continue
                try:
                    data = {"model": model_name, "messages": [{"role": "system", "content": dynamic_prompt}, {"role": "user", "content": prompt}]}
                    chat_resp = requests.post(f"{api_url}/chat/completions", headers={"Authorization": f"Bearer {current_key}", "Content-Type": "application/json"}, json=data, timeout=10)
                    chat_resp.raise_for_status()
                    return f"*(🌪️ Alternate Engine: {model_name})*\n\n{clean_response(chat_resp.json()['choices'][0]['message']['content'])}", True
                except: continue
    except: pass
    return "API failure.", False

# --- 🔥 THE ULTIMATE GOD MODE LOOP (PRO) ---
def call_god_mode(prompt):
    ans, success = call_groq_smart(prompt)
    if success: return ans
    ans, success = call_gemini_smart(prompt)
    if success: return ans
    current_key = get_random_key("CEREBRAS", 6)
    ans, success = call_universal_api("https://api.cerebras.ai/v1", current_key, prompt, "llama")
    if success: return ans
    current_key = get_random_key("TOGETHER", 6)
    ans, success = call_universal_api("https://api.together.xyz/v1", current_key, prompt, "llama")
    if success: return ans
    return "🚨 System Overloaded. Please try again later."

# --- 🖥️ VIP UI SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏴 SR-AI GLOBAL")
    st.markdown("Creator & Admin: **Babu**")
    st.markdown("---")
    
    st.markdown("🔑 **VIP Membership Key:**")
    st.text_input("", type="password", placeholder="Enter your key...", label_visibility="collapsed")
    st.markdown("---")
    
    st.markdown("### ⚙️ System Status")
    st.markdown("🟢 Engines Online: **31/31**")
    
    st.markdown("### 🧠 Select Intelligence")
    intelligence_mode = st.radio(
        "Select Mode",
        ["⚡ FAST (0.5s) - Groq", "🧠 SMART (Logic) - Gemini", "💎 PRO (Expert) - God Mode"],
        label_visibility="collapsed"
    )

# --- 💬 MAIN CHAT INTERFACE ---
st.title("💎 SR-AI GLOBAL MASTERMIND")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything (Time, Science, Coding)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f'Analyzing with {intelligence_mode.split(" ")[0]} Engine...'):
            if "FAST" in intelligence_mode:
                ans, _ = call_groq_smart(prompt)
                response = ans
            elif "SMART" in intelligence_mode:
                ans, _ = call_gemini_smart(prompt)
                response = ans
            else:
                response = call_god_mode(prompt)
                
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
