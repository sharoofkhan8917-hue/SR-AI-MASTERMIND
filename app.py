import json
import requests

# ✅ Babu, v10.0 Engine Ready Hai!
API_KEY = "AIzaSyCL3e-ZqAvE0uD24zxiFuQUU18tJIS-9TQ"

def sr_ai_mastermind_soul_update():
    print("\n" + "🏴"*20)
    print("🔥 SR-AI MASTERMIND v10.0 (ULTIMATE HINGLISH) ONLINE! 🔥")
    print("Babu, system ab sirf Hinglish mein hi baat karega.")
    print("="*40 + "\n")

    # Fast Gemini 2.0 Engine
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}

    while True:
        user_msg = input("Babu: ")
        
        if user_msg.lower() in ["exit", "bye", "band karo"]:
            print("\nAI: Alvida Babu! Agle viral dhamake ke liye hamesha taiyar. 🏴")
            break

        # 🧠 HINGLISH LOCK PAYLOAD
        payload = {
            "contents": [{
                "parts": [{"text": f"""
                STRICT SYSTEM RULES:
                1. LANGUAGE: Respond ONLY in Hinglish (Hindi language using English script). 
                2. NO ENGLISH: Strictly do NOT use full English sentences. Example: Say 'Kaise ho?' not 'How are you?'.
                3. TONE: High-energy, supportive, and witty creative partner for SR Comedy Gang.
                4. QUALITY: Give only 1 or 2 best 'Viral' ideas. 
                5. TYPO EXPERT: Understand Babu's fast typing instantly.

                Babu's Message: {user_msg}
                """}]
            }]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            if 'candidates' in result:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
                print(f"\n✨ MASTERMIND:\n{ai_reply}\n")
                print("-" * 30)
            else:
                print("\n❌ Error: Net check kijiye ya API key refresh karni hogi.")
        except Exception as e:
            print(f"\n‼️ Connection Error: {e}")

if __name__ == "__main__":
    sr_ai_mastermind_soul_update()
    
