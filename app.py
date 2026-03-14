import streamlit as st
import random
import datetime
import google.generativeai as genai
from groq import Groq
import requests

# --- 🎯 PAGE CONFIG ---
st.set_page_config(page_title="SR-AI GLOBAL", page_icon="💎", layout="wide")

st.title("💎 SR-AI GLOBAL: V7 ULTIMATE GOD MODE")
st.markdown("*Groq, Gemini aur saare engines ab apne andar ke sabse latest models khud dhoondhenge. Ek fail hua, toh turant dusre working model par switch karenge!*")
st.markdown("---")

# --- 🕒 TIME MACHINE & PERSONA ---
aaj_ki_tareekh = datetime.datetime.now().strftime("%B %d, %Y")
SYSTEM_PROMPT = f"You are a highly advanced AI. Today's date is {aaj_ki_tareekh}. You must act as the ultimate creative assistant for 'SR Comedy Gang' in 2026. Provide highly accurate, creative, and current answers."

def get_random_key(prefix, count):
    """Random chabi uthane wala jadoo"""
    key_index = random.randint(1, count)
    return st.secrets[f"{prefix}{key_index}"]

# --- ⚡ ENGINE 1: GROQ SMART LOOP (Ab Groq bhi switch karega!) ---
def call_groq_smart(prompt):
    try:
        current_key = get_random_key("GROQ", 6)
        client = Groq(api_key=current_key)
        
        # 1. Groq ke server se saare models ki list nikalo
        models_data = client.models.list().data
        available_models = [m.id for m in models_data if 'whisper' not in m.id.lower() and 'vision' not in m.id.lower()]
        
        # 2. Latest aur Heavy models ko upar rakho
        available_models.sort(reverse=True)
        
        # 3. Ek-ek karke try karo. Jo chal jaye, usse answer le lo!
        for model_name in available_models:
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    model=model_name,
                )
                return f"*(⚡ Auto-Switched to Groq: {model_name})*\n\n{chat_completion.choices[0].message.content}", True
            except Exception as e:
                continue # Agar ye fail hua, toh loop agle model par jayega
                
        return "Groq ke saare internal models down hain.", False
    except Exception as e:
        return f"Groq Connection Error: {str(e)}", False

# --- 🧠 ENGINE 2: GEMINI SMART LOOP ---
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
        pro_models = [m for m in available_models if 'pro' in m]
        other_models = [m for m in available_models if 'pro' not in m]
        sorted_models = pro_models + other_models # Pro ko pehle try karega

        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
        
        for model_name in sorted_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                return f"*(🚀 Auto-Switched to Google: {model_name})*\n\n{response.text}", True
            except Exception as e:
                continue # Try next Google model
                
        return "Google ke saare internal models down hain.", False
    except Exception as e:
        return f"Gemini Connection Error: {str(e)}", False

# --- 🚀 UNIVERSAL API CALLER (For Cerebras, Together, Mistral) ---
def call_universal_api(api_url, current_key, prompt, preferred_keyword):
    try:
        headers = {"Authorization": f"Bearer {current_key}"}
        resp = requests.get(f"{api_url}/models", headers=headers, timeout=5)
        if resp.status_code == 200:
            models = [m['id'] for m in resp.json().get('data', [])]
            models.sort(reverse=True)
            
            # Jo model chal jaye, bas usi se kaam nikal lo
            for model_name in models:
                if 'vision' in model_name.lower() or 'image' in model_name.lower(): continue
                try:
                    data = {"model": model_name, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]}
                    chat_resp = requests.post(f"{api_url}/chat/completions", headers={"Authorization": f"Bearer {current_key}", "Content-Type": "application/json"}, json=data, timeout=10)
                    chat_resp.raise_for_status()
                    return f"*(🌪️ Auto-Switched to Alternate Engine: {model_name})*\n\n{chat_resp.json()['choices'][0]['message']['content']}", True
                except:
                    continue
    except: pass
    return "API internal failure.", False

# --- 🔥 THE ULTIMATE GOD MODE LOOP (External Switcher) ---
def call_god_mode(prompt):
    # STEP 1: Groq ko sabse pehle mauka do (kyunki ye sabse fast hai)
    ans, success = call_groq_smart(prompt)
    if success: return ans

    # STEP 2: Agar Groq fail hua toh Google Gemini par jao
    ans, success = call_gemini_smart(prompt)
    if success: return ans

    # STEP 3: Agar dono fail hue, toh baaki khazana kholo
    # Cerebras
    current_key = get_random_key("CEREBRAS", 6)
    ans, success = call_universal_api("https://api.cerebras.ai/v1", current_key, prompt, "llama")
    if success: return ans

    # Together AI
    current_key = get_random_key("TOGETHER", 6)
    ans, success = call_universal_api("https://api.together.xyz/v1", current_key, prompt, "llama")
    if success: return ans

    return "🚨 Babu, ALERT! Duniya ke saare AI engines down hain (Ya aapka net band hai)!"

# --- 🖥️ UI SIDEBAR ---
st.sidebar.image("https://via.placeholder.com/150", caption="SR Comedy Gang")
st.sidebar.header("🕹️ Control Panel")
engine_choice = st.sidebar.selectbox("Select Strategy", [
    "🔥 THE ULTIMATE GOD MODE (Auto-Everything)"
])

# --- 💬 CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Babu, aaj kaunsi script banani hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Mastermind Engine auto-scanning and switching...'):
            response = call_god_mode(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
