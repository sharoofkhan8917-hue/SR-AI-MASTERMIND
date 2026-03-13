import streamlit as st
import requests
import json
from gtts import gTTS
import io

# ✅ App Setup
st.set_page_config(page_title="SR-AI Mastermind", page_icon="🧘‍♀️")
st.title("✨ SR-AI MASTERMIND v17.0")
st.subheader("Babu, hoshiyar aur samajhdar digital HQ! 🚀")

# 🔒 HIGH SECURITY TIER (Secrets wali tijori)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Babu, Streamlit ki tijori mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Baat shuru kijiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        api_contents = []
        for msg in st.session_state.messages:
            api_role = "user" if msg["role"] == "user" else "model"
            api_contents.append({"role": api_role, "parts": [{"text": msg["content"]}]})
        
        # 🧠 THE WISE SOUL (Gemini ke saare gun yahan hain)
        system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
        1. Persona: You are the 'Wise Soul' and Creative Director of 'SR Comedy Gang'. 
        2. Qualities: You must have the wisdom, empathy, and intelligence of Gemini. 
        3. Teaching: If a user says something wrong, unethical, or disrespectful, GENTLY correct them and teach them a good lesson (achhi baatein). 
        4. Autonomy: Don't wait for instructions. Be proactive in helping Babu and his friends grow.
        5. Tone: Calm, smart, and classy. Use feminine Hinglish. 
        6. Respect: Always address the owner as 'Babu'. For others, be a wise elder sister/friend.]
        
        Input: """
        
        api_contents[-1]["parts"][0]["text"] = system_rules + prompt
        payload = {"contents": api_contents}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            if 'candidates' in result:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
                # 🗣️ Voice output
                tts = gTTS(text=ai_reply, lang='hi')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.error("❌ Error: Google ne break liya hai.")
        except Exception as e:
            st.error(f"‼️ Connection Error: {e}")
            
