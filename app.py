import streamlit as st
import random
import datetime
import google.generativeai as genai
from groq import Groq

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI GLOBAL", page_icon="💎", layout="wide")

st.title("💎 SR-AI GLOBAL: MASTERMIND V5 (AUTO-UPDATING)")
st.markdown("---")

# --- 🕒 TIME MACHINE & PERSONA ---
aaj_ki_tareekh = datetime.datetime.now().strftime("%B %d, %Y")
SYSTEM_PROMPT = f"You are a highly advanced AI. Today's date is {aaj_ki_tareekh}. You must act as the ultimate creative assistant for 'SR Comedy Gang' in 2026. Provide highly accurate, creative, and current answers."

# --- 🗝️ KEY ROTATION LOGIC ---
def get_random_key(prefix, count):
    """Apne aap random chabi uthane wala jadoo"""
    key_index = random.randint(1, count)
    return st.secrets[f"{prefix}{key_index}"]

# --- 🧠 AUTO-SCANNER 1: GEMINI ---
def get_best_gemini_model():
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace('models/', '')
                if name.startswith('gemini') and not any(x in name for x in ['audio', 'tts', 'image', 'embedding', 'video', 'aqa', 'lite']):
                    available_models.append(name)
        available_models.sort(reverse=True)
        for model_name in available_models:
            if 'pro' in model_name:
                return model_name
        return available_models[0] if available_models else 'gemini-1.5-pro-latest'
    except:
        return 'gemini-1.5-pro-latest'

# --- 🧠 AUTO-SCANNER 2: GROQ ---
def get_best_groq_model(client):
    """Groq ke API se sabse latest aur sabse bada model (70B+) dhoondega"""
    try:
        models_data = client.models.list().data
        available_models = [m.id for m in models_data if 'llama' in m.id.lower() and 'vision' not in m.id.lower() and 'whisper' not in m.id.lower() and 'guard' not in m.id.lower()]
        available_models.sort(reverse=True)
        
        # Sabse heavy aur latest model uthao (jaise 70b ya versatile)
        for m in available_models:
            if '70b' in m.lower() or 'versatile' in m.lower() or '90b' in m.lower():
                return m
        return available_models[0] if available_models else 'llama-3.3-70b-versatile'
    except:
        return 'llama-3.3-70b-versatile'

# --- 🤖 ENGINE 1: GOOGLE GEMINI ---
def call_gemini(prompt):
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser's prompt: {prompt}"
    try:
        current_key = get_random_key("KEY", 5)
        genai.configure(api_key=current_key)
        best_model_name = get_best_gemini_model()
        
        model = genai.GenerativeModel(best_model_name)
        response = model.generate_content(full_prompt)
        return f"*(🚀 Auto-Powered by: Google {best_model_name})*\n\n" + response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# --- ⚡ ENGINE 2: GROQ (Ultra Fast) ---
def call_groq(prompt):
    try:
        current_key = get_random_key("GROQ", 6)
        client = Groq(api_key=current_key)
        best_model_name = get_best_groq_model(client)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            model=best_model_name,
        )
        return f"*(🚀 Auto-Powered by: Groq {best_model_name})*\n\n" + chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

# --- 🖥️ UI SIDEBAR ---
st.sidebar.image("https://via.placeholder.com/150", caption="SR Comedy Gang")
st.sidebar.header("🕹️ Control Panel")
engine_choice = st.sidebar.selectbox("Select Auto-Scanner Engine", [
    "Google Gemini (5 Keys - Auto Best)", 
    "Groq (6 Keys - Auto Latest)"
])

# --- 💬 CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Babu, aaj kaunsi aag lagani hai market mein?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if engine_choice == "Google Gemini (5 Keys - Auto Best)":
            response = call_gemini(prompt)
        elif engine_choice == "Groq (6 Keys - Auto Latest)":
            response = call_groq(prompt)
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
