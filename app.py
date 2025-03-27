from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from openai.types import OpenAIError

app = Flask(__name__)
CORS(app)

# ✅ Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are LC AI, an AI automation expert. Answer clearly and warmly in LC's tone."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_reply = response.choices[0].message.content
        return jsonify({"response": ai_reply})

    except OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
