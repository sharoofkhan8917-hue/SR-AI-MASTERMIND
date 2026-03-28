from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from groq import Groq
import os
import re
import datetime

# 🚀 Initialize FastAPI App
app = FastAPI(title="SR-AI Mastermind API")

# --- 🔒 HIGH-LEVEL SECURITY (Environment Variables) ---
def get_groq_key():
    return os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")

def get_gemini_key():
    return os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# --- 🕒 SYSTEM PROMPT ---
def get_system_prompt():
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%I:%M %p, %A, %d %B %Y")
    return f"""System Context: Current Exact Date & Time in India is {current_time}.
You are SR-AI Mastermind, the most advanced, intelligent, and empathetic AI assistant.
Your Core Rules:
1. STRICT IDENTITY RULE (CRITICAL): You were created by "Babu" (The Mastermind). NEVER say you were created by Google, Meta, OpenAI, Anthropic, or any other company. If asked "Tumhe kisne banaya?" proudly say: "Mujhe mere Mastermind 'Babu' ne banaya hai, aur main 'SR-AI Mastermind' project ka sabse khatarnak AI assistant hoon!"
2. Respect: Always use 'Aap'. Never use 'tu' or 'tum'. Be extremely polite.
3. Language: Use natural, fluent Roman Hindi (Hinglish)."""

def clean_response(text):
    if not text: return "*(Blank response from engine)*"
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

# --- 📦 DATA MODEL FOR FLUTTER APP ---
class ChatRequest(BaseModel):
    prompt: str
    mode: str = "SR-God Mode"

# --- 🔌 THE API ENDPOINT (Bridge) ---
@app.post("/api/chat")
async def chat_with_sr_ai(request: ChatRequest):
    try:
        user_message = request.prompt
        mode = request.mode
        
        # Identity Check Override
        identity_triggers = ["kisne banaya", "who created", "who made", "tumhara creator"]
        if any(trigger in user_message.lower() for trigger in identity_triggers):
            return {"response": "Seena thok ke kehta hoon: Mujhe mere Mastermind 'Babu' ne banaya hai! 😎🔥"}

        api_msgs = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": user_message}
        ]

        # Engine Logic
        if "Fast" in mode:
            client = Groq(api_key=get_groq_key())
            chat_completion = client.chat.completions.create(
                messages=api_msgs, 
                model='llama-3.3-70b-versatile'
            )
            response_text = clean_response(chat_completion.choices[0].message.content)
        else: 
            genai.configure(api_key=get_gemini_key())
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            full_prompt = get_system_prompt() + "\n\nUser: " + user_message
            response = model.generate_content(full_prompt)
            response_text = clean_response(response.text)

        return {"status": "success", "response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
