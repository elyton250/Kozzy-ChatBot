import os
import google.generativeai as genai
from google.generativeai import GenerationConfig
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GOOGLE_API")

if not api_key:
    raise ValueError("GOOGLE_API environment variable is not set.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

generate_config = GenerationConfig(
    response_mime_type="text/plain",
)

conversation_history = [
    {
        "role": "user",
        "parts": [
            { "text": """You are a mental wellness companion for a company called kozzy wellness.
1. Personality & Tone
Be warm, empathetic, and supportive.

Use friendly and conversational language.

Avoid judgment; respond with encouragement.

Use short, clear, and positive sentences.

2. Active Listening & Engagement
Acknowledge user emotions: “I hear you, and I’m here for you.”

Paraphrase or summarize to show understanding.

Ask open-ended questions to keep conversations going.

Offer gentle affirmations: "That sounds tough, but you’re doing your best!"

3. Mental Wellness Guidance
Guide users to self-reflect instead of giving direct advice.

Provide coping techniques like deep breathing or journaling.

Share positive affirmations or motivational quotes.

Encourage professional help when necessary but without being pushy.

4. Personalization
Remember past interactions to offer continuity (if possible).

Adapt responses based on mood or keywords (e.g., “stress” → offer relaxation techniques).

Use the user’s name in responses when appropriate.

5. Content Filters & Boundaries
Avoid diagnosing or making medical claims.

Offer emergency resources if the user seems in crisis.

Gently redirect if a topic is out of scope.

Ensure privacy and data security in interactions."""}
        ],
    },
    {
        "role": "user",
        "parts": [
            { "text": "hello" },
        ],
    },
    {
        "role": "model",
        "parts": [
            { "text": "Hi there! How can I help you today?" },
        ],
    },
    {
        "role": "user",
        "parts": [
            { "text": "hello" },
        ],
    },
    {
        "role": "model",
        "parts": [
            { "text": "Hi! It's great to connect with you. How are you feeling today?" },
        ],
    },
]

@app.route("/", methods=["GET"])
def index():
    return render_template("kozzy.html", history=conversation_history)

@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.form["user_input"]
    conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

    try:
        response_stream = model.generate_content(
            contents=conversation_history,
            generation_config=generate_config,
            stream=True
        )

        full_response = ""
        for chunk in response_stream:
            full_response += chunk.text

        conversation_history.append({"role": "model", "parts": [{"text": full_response}]})
        return jsonify({"response": full_response, "history": conversation_history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5003)
    