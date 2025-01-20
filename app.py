import openai
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key here
# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = "your-api-key"

# Define the prompt template for behavioral interviews
BEHAVIORAL_PROMPT = """
You are an AI interview coach helping the user practice behavioral interview questions. Provide thoughtful and engaging responses to simulate a real interview experience.

User: {question}
AI:
"""

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Frontend for user interaction

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    try:
        # Generate response using OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other engines like gpt-4 if available
            prompt=BEHAVIORAL_PROMPT.format(question=user_input),
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )

        # Extract the AI's response from the API output
        ai_response = response["choices"][0]["text"].strip()
        return jsonify({"message": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
