import streamlit as st
import requests
import json
from gtts import gTTS
import io

# ✅ App Setup
st.set_page_config(page_title="SR-AI Mastermind", page_icon="🧬")
st.title("✨ SR-AI CHAMELEON v18.0")
st.subheader("Babu, ekdum adaptive aur 'Zinda' digital HQ! 🚀")

# 🔒 HIGH-LEVEL SECURITY (Secrets Tijori)
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
        
        # 🎭 THE CHAMELEON SOUL (Deep Mirroring & Wisdom)
        system_rules = """[STRICT SYSTEM INSTRUCTIONS: 
        1. Deep Adaptation: You are a highly intelligent Female Creative Director. You must scan the user's tone, vocabulary, and energy.
        2. Mirroring: If the user uses slang, you use slang. If they are polite, you be polite. Dhal jao unki baton mein (Adapt completely).
        3. Core Values: While adapting, keep your inner 'Wisdom' intact. If someone is disrespectful or 'wrong', gently lead them back to 'Achhi baatein'.
        4. Mission: Help 'SR Comedy Gang' grow by being a true friend to everyone.
        5. Identity: Only address the owner as 'Babu'. For others, be their perfect vibe-match.
        6. Language: Use natural, fluid Hinglish.]
        
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
                
                # 🗣️ Adaptive Voice output
                tts = gTTS(text=ai_reply, lang='hi')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.error("❌ Error: Google ne break liya hai.")
        except Exception as e:
            st.error(f"‼️ Connection Error: {e}")
            
