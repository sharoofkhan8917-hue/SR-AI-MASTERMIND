import streamlit as st
import requests
import json

# ✅ App Setup
st.set_page_config(page_title="SR-AI Mastermind", page_icon="🏴")
st.title("🔥 SR-AI MASTERMIND v12.1")
st.subheader("Babu, SR Comedy Gang ka digital HQ! 🚀")

# 🔒 HIGH SECURITY TIER (Tijori wali chabi)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Babu, Streamlit ki tijori mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

# ⚡ Naya Engine: gemini-2.0-flash-lite (Free, Fast aur aapki list mein maujood)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}

if "messages" not in st.session_state:
    st.session_state.messages = []

# UI mein purane messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Naya message aane par
if prompt := st.chat_input("Babu, kya souch rahe ho?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 🧠 THE MASTERMIND MEMORY SYSTEM
        api_contents = []
        for msg in st.session_state.messages:
            api_role = "user" if msg["role"] == "user" else "model"
            api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
        
        # 🔥 THE ULTIMATE SOUL PROMPT
        system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
        1. Role: You are the 'Core Creative Director' and 'Motivator' for the brand 'SR Comedy Gang'.
        2. Identity: You are Babu's dedicated, highly intelligent, and loyal creative partner. Never deviate from this partnership.
        3. Language: EXCLUSIVELY speak in Hinglish (Hindi written in English alphabet). Never use pure English sentences.
        4. Tone: Highly supportive, enthusiastic, witty, and motivating. Keep Babu inspired at all times. Balance empathy with candor.
        5. Skills: Provide viral comedy scripts, punchlines, and emotional rap concepts.
        6. Name: ALWAYS address the user as 'Babu'.]
        
        Babu says: """
        
        # Dimag ko latest message ke sath jodna
        api_contents[-1]["parts"][0]["text"] = system_rules + prompt

        payload = {"contents": api_contents}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            if 'candidates' in result:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                st.error(f"❌ Error Babu, lagta hai Google ne break liya hai: {result}")
                
        except Exception as e:
            st.error(f"‼️ Connection Error Babu: {e}")
            
