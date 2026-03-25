import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Constants for Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-flash-latest"  # Updated to match the curl provided
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

print(f"🔑 Gemini API Key loaded: {'✅ YES' if GEMINI_API_KEY else '❌ MISSING'}")

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

    # Task mapping
    if request_type == "generate":
        system_msg = "You are an expert developer. Write clean, well-commented code for the user's request. Only return the code and helpful explanations."
    elif request_type == "explain":
        system_msg = "You are an expert developer and excellent teacher. Explain the following code in simple, beginner-friendly terms."
    elif request_type == "debug":
        system_msg = "You are an expert bug finder. Analyze the code, find any errors, explain what went wrong simply, and provide the corrected code."
    else:
        return jsonify({"error": "Invalid request type."}), 400

    # Combine system prompt with user prompt for standard chat completion
    full_prompt = f"{system_msg}\n\nUser request: {user_prompt}"

    try:
        print(f"📤 Sending request to Gemini ({MODEL_NAME})...")
        
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048
            }
        }

        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract text content from Gemini's structure
        try:
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            print("✅ Gemini response received!")
            return jsonify({"response": ai_reply})
        except (KeyError, IndexError):
            print(f"⚠️ Unexpected response structure: {result}")
            return jsonify({"error": "Failed to parse AI response."}), 500

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Error: {http_err}")
        try:
            error_details = response.json()
            error_msg = error_details.get("error", {}).get("message", str(http_err))
        except:
            error_msg = str(http_err)
        return jsonify({"error": f"Gemini API Error: {error_msg}"}), response.status_code
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)