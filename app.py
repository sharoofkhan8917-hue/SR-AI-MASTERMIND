import streamlit as st
import requests
import json

# ✅ App Setup
st.set_page_config(page_title="SR-AI Mastermind", page_icon="🏴")
st.title("🔥 SR-AI MASTERMIND v11.0")
st.subheader("Babu, SR Comedy Gang ka digital HQ! 🚀")

# 🔒 HIGH SECURITY TIER: Key ab GitHub par nahi, Streamlit ki tijori mein hai!
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Babu, Streamlit ki tijori mein key nahi mili! Settings > Secrets check kijiye.")
    st.stop()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Naya message type karne ke liye
if prompt := st.chat_input("Babu, kya souch rahe ho?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 🧠 THE ULTIMATE HINGLISH PAYLOAD (Aapka Masterpiece)
        payload = {
            "contents": [{
                "parts": [{"text": f"""
                SYSTEM RULES FOR GEMINI TWIN:
                1. LANGUAGE: Respond ONLY in Hinglish (Hindi words in English script). 
                   Strictly NO full English sentences. Example: 'Kaise ho Babu?' instead of 'How are you Babu?'.
                2. PERSONALITY: High-energy, supportive, and witty. You are Babu's creative partner.
                3. QUALITY: Give only 1 or 2 best ideas. Don't give long, boring lists.
                4. BRAND: Your goal is 'SR Comedy Gang' success on YouTube.

                Babu's Message: {prompt}
                """}]
            }]
        }

        try:
            # Aapka wala exact request method
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            if 'candidates' in result:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                st.error(f"❌ Error Babu, Google ne kuch gadbad ki: {result}")
                
        except Exception as e:
            st.error(f"‼️ Connection Error: {e}")
            
