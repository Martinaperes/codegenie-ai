import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client 
# It automatically picks up the OPENAI_API_KEY environment variable if it is set in .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    """Render the main UI page."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Handle incoming requests from the frontend."""
    # Get the JSON data sent from the frontend
    data = request.get_json()
    
    # Extract the user input and the type of request (generate, explain, debug)
    user_prompt = data.get("prompt", "").strip()
    request_type = data.get("type", "")

    # Basic validation: ensure the prompt is not empty
    if not user_prompt:
        return jsonify({"error": "Prompt cannot be empty."}), 400

    # Determine the system instruction based on the button clicked
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
        # Call the OpenAI API using the latest client syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # We use gpt-3.5-turbo as a default fast and cost-effective model
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )
        
        # Extract the AI's reply from the response
        ai_reply = response.choices[0].message.content
        
        # Return the response as JSON to the frontend
        return jsonify({"response": ai_reply})

    except Exception as e:
        # Handle errors gracefully (e.g., missing API key, network issues)
        print(f"Error calling OpenAI API: {e}")
        return jsonify({"error": "An error occurred while generating the response. Please check your API key (.env) and try again."}), 500

if __name__ == "__main__":
    # Run the application in debug mode on port 5000
    app.run(debug=True, port=5000)
