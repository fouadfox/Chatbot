import torch

from sentence_transformers import SentenceTransformer

print("Torch version:", torch.__version__)
model = SentenceTransformer("all-MiniLM-L6-v2")
print("SentenceTransformer loaded successfully!")

from flask import Flask, request, jsonify, render_template
from chatbot_logic import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    user_message = request.json.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

# Add a simple memory
conversation_history = []

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    global conversation_history
    user_message = request.json.get("message")
    conversation_history.append({"role": "user", "content": user_message})

    # Use conversation history for response
    response = get_response(user_message)
    conversation_history.append({"role": "bot", "content": response})
    
    return jsonify({"response": response, "history": conversation_history})
