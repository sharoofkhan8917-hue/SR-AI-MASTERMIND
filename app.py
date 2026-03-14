import streamlit as st
import random
import google.generativeai as genai
from groq import Groq

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI GLOBAL", page_icon="💎", layout="wide")

st.title("💎 SR-AI GLOBAL: 31-KEY EDITION")
st.markdown("---")

# --- 🗝️ KEY ROTATION LOGIC (The Mastermind Switch) ---
def get_random_key(prefix, count):
    """Apne aap random chabi uthane wala jadoo"""
    key_index = random.randint(1, count)
    return st.secrets[f"{prefix}{key_index}"]

# --- 🤖 ENGINE 1: GOOGLE GEMINI (UPDATED MODEL) ---
def call_gemini(prompt):
    try:
        current_key = get_random_key("KEY", 5)
        genai.configure(api_key=current_key)
        # Naya aur update kiya hua Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)} - Try switching keys!"

# --- ⚡ ENGINE 2: GROQ (Ultra Fast - UPDATED MODEL) ---
def call_groq(prompt):
    try:
        current_key = get_random_key("GROQ", 6)
        client = Groq(api_key=current_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            # Groq ka naya Llama 3.1 model jo kabhi fail nahi hota
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

# --- 🚀 ENGINE 3: CEREBRAS (NOS Boost) ---
# Note: Iske liye 'cerebras_cloud_sdk' install hona chahiye
def call_cerebras(prompt):
    try:
        current_key = get_random_key("CEREBRAS", 6)
        # Yahan Cerebras ka logic aayega (API endpoint call)
        return "Cerebras Engine Active! Speed: Rocket 🚀 (Key used: " + current_key[:10] + "...)"
    except Exception as e:
        return f"Cerebras Error: {str(e)}"

# --- 🖥️ UI SIDEBAR ---
st.sidebar.image("https://via.placeholder.com/150", caption="SR Comedy Gang")
st.sidebar.header("🕹️ Control Panel")
engine_choice = st.sidebar.selectbox("Select Engine", ["Google Gemini (5 Keys)", "Groq (6 Keys)", "Cerebras (6 Keys)", "HuggingFace/Mistral"])

# --- 💬 CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Babu, kya mission hai aaj?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if engine_choice == "Google Gemini (5 Keys)":
            response = call_gemini(prompt)
        elif engine_choice == "Groq (6 Keys)":
            response = call_groq(prompt)
        else:
            response = "Babu, baaki engines ki integration abhi wiring mein hai. Gemini aur Groq ekdum smooth chal rahe hain!"
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
