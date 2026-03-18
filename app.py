import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import traceback

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# DEBUG: Print API key status
api_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 API Key loaded: {'✅ YES ({len(api_key)} chars)' if api_key else '❌ MISSING'}")

client = OpenAI(api_key=api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_prompt = data.get("prompt", "").strip()
    request_type = data.get("type", "")

    if not user_prompt:
        return jsonify({"error": "Prompt cannot be empty."}), 400

    # System messages (same as yours)
    if request_type == "generate":
        system_msg = "You are an expert developer. Write clean, well-commented code for the user's request. Only return the code and helpful explanations."
        full_prompt = f"Write clean, well-commented code for: {user_prompt}"
    elif request_type == "explain":
        system_msg = "You are an expert developer and excellent teacher. Explain the following code in simple, beginner-friendly terms."
        full_prompt = f"Explain this code in simple terms:\n\n{user_prompt}"
    elif request_type == "debug":
        system_msg = "You are an expert bug finder. Analyze the code, find any errors, explain what went wrong simply, and provide the corrected code."
        full_prompt = f"Find and fix errors in this code and explain:\n\n{user_prompt}"
    else:
        return jsonify({"error": "Invalid request type."}), 400

    try:
        print(f"📤 Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=2000  # Add this to prevent truncation
        )
        
        ai_reply = response.choices[0].message.content
        print("✅ OpenAI response received!")
        return jsonify({"response": ai_reply})

    except Exception as e:
        error_msg = str(e)
        print(f"❌ OpenAI Error: {error_msg}")
        print(f"Full traceback: {traceback.format_exc()}")
        
        if "Invalid API key" in error_msg:
            return jsonify({"error": "❌ Invalid API key. Get a new one at https://platform.openai.com/api-keys"}), 401
        elif "insufficient_quota" in error_msg:
            return jsonify({"error": "❌ No credits left. Add payment method at https://platform.openai.com/account/billing"}), 402
        elif "rate_limit" in error_msg:
            return jsonify({"error": "⏳ Rate limit hit. Wait a moment and try again."}), 429
        else:
            return jsonify({"error": f"API Error: {error_msg}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)