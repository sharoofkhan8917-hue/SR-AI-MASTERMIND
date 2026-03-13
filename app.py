import streamlit as st
import requests

st.set_page_config(page_title="SR-AI Mastermind", page_icon="🏴")
st.title("🔥 SR-AI MASTERMIND v11.0")
st.subheader("Babu, SR Comedy Gang ka digital HQ! 🚀")

API_KEY = "AIzaSyCL3e-ZqAvE0uD24zxiFuQUU18tJIS-9TQ"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Babu, kya souch rahe ho?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        payload = {
            "contents": [{
                "parts": [{"text": f"Reply ONLY in Hinglish. You are Babu's creative partner for SR Comedy Gang. User: {prompt}"}]
            }]
        }
        try:
            response = requests.post(URL, json=payload)
            reply = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error("Babu, system garam ho gaya hai! Thodi der baad try karein.")
            
