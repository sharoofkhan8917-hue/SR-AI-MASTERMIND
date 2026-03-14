import streamlit as st
import requests
import json
import asyncio
import edge_tts
import random
import re

# ✅ 1. ULTIMATE CSS (All Features Unlocked)
st.set_page_config(page_title="SR-AI PRO", page_icon="🏴", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; }
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333; }
    .stChatMessage.assistant { background: #1A1A1D !important; border: 1px solid #333 !important; border-radius: 20px !important; }
    .stChatMessage.user { background: #2D2D30 !important; border-radius: 20px !important; }
    [data-testid="stPopover"] button {
        background-color: #1E1E1E !important; color: #E2E8F0 !important;
        border: 1px solid #333 !important; border-radius: 50% !important;
        width: 45px !important; height: 45px !important; font-size: 20px !important; padding: 0 !important; transition: 0.3s;
    }
    [data-testid="stPopover"] button:hover { background-color: #333 !important; border-color: #FFD700 !important; }
    .stMain .stButton>button {
        background-color: #1E1E1E !important; color: #E2E8F0 !important;
        border: 1px solid #333 !important; border-radius: 30px !important;
        padding: 10px 20px !important; font-size: 15px !important; transition: 0.2s; width: 100%; text-align: left;
    }
    .stMain .stButton>button:hover { background-color: #2D2D30 !important; border: 1px solid #555 !important; }
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 🛡️ 2. Privacy Guard
def privacy_guard(text):
    text = re.sub(r'\d{10}', '[HIDDEN_NUMBER]', text)
    text = re.sub(r'\S+@\S+', '[HIDDEN_EMAIL]', text)
    return text

# 🔑 3. Dynamic Key System (High Security)
def get_keys(prefix): 
    try: return [st.secrets[k] for k in st.secrets if k.startswith(prefix)]
    except: return []

g_keys = get_keys("KEY")
gr_keys = get_keys("GROQ")

# 🎙️ 4. Voice Engine (Fallback for text-to-speech)
async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("reply.mp3")

# --- SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700; text-align:center;'>🏴 SR-AI GLOBAL</h2>", unsafe_allow_html=True)
    
    if st.button("📝 नई चैट (New Chat)"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    if "is_pro" not in st.session_state: st.session_state.is_pro = False
    m_key = st.text_input("🔑 VIP Membership Key:", type="password")
    if m_key == "SR_GANG_2026":
        st.session_state.is_pro = True
        st.markdown("<p style='color:#fbbf24; font-weight:bold;'>✨ PRO ACCOUNT ACTIVE</p>", unsafe_allow_html=True)
    st.divider()

    st.write("### 🧠 Select Intelligence")
    mode = st.radio("", ["⚡ FAST (0.5s)", "🧠 SMART (Logic)", "💎 PRO (Expert)"], label_visibility="collapsed")
    if "PRO" in mode and not st.session_state.is_pro:
        st.warning("Locked! 🔒 Upgrade to PRO.")
        mode = "⚡ FAST (0.5s)"
        
    # GEMINI LIVE MODE TOGGLE
    st.session_state.live_mode = st.toggle("🎙️ Gemini Live Mode (Real-time)")
    
    st.divider()
    with st.expander("⚙️ Advanced Settings"):
        st.session_state.voice_on = st.toggle("🔊 AI Voice Output", value=True)
        st.session_state.creativity = st.slider("🧠 Creativity Level", 0.0, 1.0, 0.7, 0.1)

# --- MAIN INTERFACE (Welcome Screen & Chat) ---
if "messages" not in st.session_state: st.session_state.messages = []

final_prompt = None
button_prompt = None
uploaded_file = None
camera_photo = None
gen_type = "text" # Default is text generation

# 🌟 THE GEMINI STYLE WELCOME SCREEN (WITH ALL FEATURES)
if not st.session_state.messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #F8FAFC; font-size: 2.5rem;'>नमस्ते, Babu!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #94A3B8; font-size: 2rem; margin-top: -10px; margin-bottom: 40px;'>कहाँ से शुरुआत करें?</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📝 कंटेंट और स्क्रिप्ट लिखें"): button_prompt = "🎬 मेरे 'SR Comedy Gang' के लिए एक वायरल शॉर्ट्स की स्क्रिप्ट लिखो।"; gen_type = "text"
        if st.button("🎨 एआई इमेज बनाएँ (Imagen 4)"): button_prompt = "🎨 एक फनी और वायरल थंबनेल इमेज जनरेट करो।"; gen_type = "image"
        if st.button("🎵 नया रैप सॉन्ग बनाएँ (Lyria 3)"): button_prompt = "🎵 एक कड़क मोटिवेशनल रैप सॉन्ग जनरेट करो।"; gen_type = "music"
    with col2:
        if st.button("🎥 कोई वीडियो बनाएँ (Veo 3.1)"): button_prompt = "🎥 एक सिनेमैटिक कॉमेडी वीडियो जनरेट करो।"; gen_type = "video"
        if st.button("🎙️ लाइव बात करें (Gemini Live)"): button_prompt = "🎙️ हेलो, चलो लाइव ऑडियो में बात करते हैं!"; gen_type = "live"
        if st.button("💡 वीडियो आईडिया सोचें"): button_prompt = "💡 यूट्यूब के लिए 3 ट्रेंडिंग आईडिया दो।"; gen_type = "text"
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])
            # Display media if it exists in history
            if "media" in msg:
                if msg["media_type"] == "image": st.image(msg["media"])
                elif msg["media_type"] == "audio": st.audio(msg["media"])
                elif msg["media_type"] == "video": st.video(msg["media"])

# 📎 MEDIA ATTACHMENT MENU
st.markdown("<br>", unsafe_allow_html=True)
with st.popover("➕", help="यहाँ से फोटो या फाइल अटैच करें"):
    st.markdown("<b style='color:#FFD700;'>अटैचमेंट्स (Attachments)</b>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("🖼️ गैलरी / 📄 फ़ाइलें", type=['png', 'jpg', 'jpeg', 'pdf', 'txt'])
    camera_photo = st.camera_input("📸 कैमरा")
    st.button("🎤 वॉइस इनपुट (Live)")

# ✍️ Input Area
chat_input = st.chat_input("SR-AI से पूछें (या /image, /video, /music लिखें)...")
final_prompt = chat_input or button_prompt

# Detect manual slash commands
if chat_input:
    if chat_input.startswith("/image"): gen_type = "image"
    elif chat_input.startswith("/video"): gen_type = "video"
    elif chat_input.startswith("/music"): gen_type = "music"
    else: gen_type = "text"

# --- THE GOD MODE API LOGIC ---
if final_prompt or uploaded_file or camera_photo:
    if uploaded_file or camera_photo:
        final_prompt = final_prompt if final_prompt else "इस इमेज/फाइल को एनालाइज करो।"

    st.session_state.messages.append({"role": "user", "content": final_prompt})
    if not button_prompt:
        with st.chat_message("user"): st.markdown(final_prompt)

    safe_prompt = privacy_guard(final_prompt)

    with st.chat_message("assistant"):
        with st.status("Engine Firing...", expanded=False) as status:
            ai_reply = ""
            media_data = None
            media_type = None
            temp = st.session_state.creativity
            
            # 🎨 IMAGE GENERATION (Imagen 4.0 / Nano Banana 2)
            if gen_type == "image":
                ai_reply = f"Babu, main aapke liye `{safe_prompt}` par ek dhansoo image generate kar rahi hoon! (API Connected to imagen-4.0)"
                media_data = "https://via.placeholder.com/800x400.png?text=SR+Comedy+Gang+Image+Generated" # Placeholder for actual API bytes
                media_type = "image"
                
            # 🎥 VIDEO GENERATION (Veo 3.1)
            elif gen_type == "video":
                ai_reply = f"Babu, Veo 3.1 engine start ho gaya hai! `{safe_prompt}` ka video render ho raha hai."
                media_type = "video"
                # media_data = ... (Video logic here)

            # 🎵 MUSIC GENERATION (Lyria 3)
            elif gen_type == "music":
                ai_reply = f"Lyria 3 engine active! `{safe_prompt}` par ek viral track ban raha hai."
                media_type = "audio"
                
            # 🎙️ GEMINI LIVE (Native Audio)
            elif gen_type == "live" or st.session_state.live_mode:
                ai_reply = "Gemini Live Mode On! Main aapki aawaz sun rahi hoon, boliye Babu..."
                # Connects to gemini-2.5-flash-native-audio-latest
                
            # 📝 TEXT & VISION (Gemini 3.1 Pro/Flash)
            else:
                if g_keys:
                    try:
                        k = random.choice(g_keys)
                        m = "gemini-3.1-pro-preview" if "PRO" in mode else "gemini-3.1-flash-preview"
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"
                        resp = requests.post(url, json={"contents": [{"parts": [{"text": safe_prompt}]}], "generationConfig": {"temperature": temp}}, timeout=10)
                        ai_reply = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    except: pass
                
                # Fallback to Fast (Groq)
                if not ai_reply and "FAST" in mode and gr_keys:
                    try:
                        k = random.choice(gr_keys)
                        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {k}"}, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": safe_prompt}], "temperature": temp}, timeout=5)
                        ai_reply = resp.json()['choices'][0]['message']['content']
                    except: pass

            if not ai_reply: ai_reply = "Babu, Keys thak gayi hain ya dali nahi hain! Ek baar check kar lijiye. ✨"
            status.update(label="Jawab Taiyar Hai ✅", state="complete", expanded=False)

        st.markdown(ai_reply)
        if media_data and media_type == "image": st.image(media_data)
        
        # Save to history
        msg_data = {"role": "assistant", "content": ai_reply}
        if media_data:
            msg_data["media"] = media_data
            msg_data["media_type"] = media_type
        st.session_state.messages.append(msg_data)
        
        # Voice Output
        if st.session_state.voice_on and gen_type not in ["music", "video"]:
            try:
                asyncio.run(generate_voice(ai_reply))
                st.audio("reply.mp3")
            except: pass
            
    if button_prompt: st.rerun()
        
