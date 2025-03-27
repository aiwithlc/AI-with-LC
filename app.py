# ✅ CORS fix for production deployment

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)

# ✅ CORRECT WAY: Allow lcacosta.com + localhost for dev
CORS(app, resources={r"/chat": {"origins": [
    "https://lcacosta.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]}})

# ✅ Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are LC's warm, helpful, expert AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
