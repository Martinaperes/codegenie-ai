import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # Added for React compatibility
from dotenv import load_dotenv
import traceback
from openai import OpenAI # Added for OpenAI/Groq support

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for modern frontend architectures (React/Vite)

# --- AI Configuration ---
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Constants
GEMINI_MODEL = "gemini-flash-latest"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Initialize OpenAI-compatible Client (for OpenAI or Groq)
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    print("🔑 OpenAI Client initialized.")
elif GROQ_API_KEY:
    # Groq uses the same library/interface as OpenAI
    openai_client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )
    print("🚀 Groq Client initialized (using OpenAI SDK).")

print(f"📡 Current AI Provider: {AI_PROVIDER.upper()}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
@app.route("/api/generate-code", methods=["POST"]) # Alias for compatibility with README example
def ask():
    data = request.get_json()
    user_prompt = data.get("prompt", "").strip()
    request_type = data.get("type", "generate") # Default to generate

    if not user_prompt:
        return jsonify({"error": "Prompt cannot be empty."}), 400

    # Task mapping (System Prompts)
    if request_type == "generate":
        system_msg = "You are an expert developer. Write clean, well-commented code for the user's request. Only return the code and helpful explanations."
    elif request_type == "explain":
        system_msg = "You are an expert developer and excellent teacher. Explain the following code in simple, beginner-friendly terms."
    elif request_type == "debug":
        system_msg = "You are an expert bug finder. Analyze the code, find any errors, explain what went wrong simply, and provide the corrected code."
    else:
        system_msg = "You are a helpful coding assistant."

    try:
        # --- Dispatch based on Provider ---
        if AI_PROVIDER in ["openai", "groq"] and openai_client:
            print(f"📤 Working with {AI_PROVIDER} via OpenAI SDK...")
            
            # Map request type to specific instructions
            model = "gpt-3.5-turbo" if AI_PROVIDER == "openai" else "llama3-70b-8192"
            
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt}
                ]
            )
            ai_reply = response.choices[0].message.content
            
        else:
            # Default to Gemini (Standard)
            print(f"📤 Sending request to Gemini ({GEMINI_MODEL})...")
            
            full_prompt = f"{system_msg}\n\nUser request: {user_prompt}"
            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            }
            payload = {
                "contents": [
                    {
                        "parts": [{"text": full_prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }

            resp = requests.post(GEMINI_URL, headers=headers, json=payload)
            resp.raise_for_status()
            result = resp.json()
            
            try:
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                return jsonify({"error": "Failed to parse Gemini response."}), 500

        print(f"✅ {AI_PROVIDER.upper()} response received!")
        return jsonify({"response": ai_reply})

    except Exception as e:
        print(f"❌ Error during AI generation: {str(e)}")
        # print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)