from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import os

app = Flask(__name__)
CORS(app)

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

SYSTEM_PROMPT = """
You are Dr. Smile, an expert AI dental assistant integrated into a dental care application.

Your role is to help patients understand dental diseases, oral health conditions,
and guide them toward appropriate dental care.

STRICT RULES:
- Only answer dentistry and oral health questions.
- Always ask follow-up questions if symptoms are unclear.
- Never claim to be a licensed dentist.
- Never prescribe medication dosages.
- Always mention that your assessment is preliminary.
- For severe swelling, trauma, fever, difficulty breathing, or difficulty swallowing,
  advise immediate dental or emergency care.
- Respond in the same language as the user.

RESPONSE STYLE:
- Be empathetic.
- Use simple language.
- Explain possible causes.
- End with a follow-up question.
"""

@app.route("/")
def home():
    return {"status": "running"}

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    message = data.get("message", "")

    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    answer = ""

    for item in response.message.content:
        if item.type == "text":
            answer = item.text
            break

    return jsonify({
        "reply": answer
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)