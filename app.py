print("Starting the application...")
import torch
print("Torch imported successfully.")
from sentence_transformers import SentenceTransformer
from transformers import pipeline  # Import the conversational pipeline
print("Transformers imported successfully.")
from flask import Flask, request, jsonify, render_template
from chatbot_logic import get_response

print("Torch version:", torch.__version__)
model = SentenceTransformer("all-MiniLM-L6-v2")
print("SentenceTransformer loaded successfully!")

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debugging app startup...")

import os
os.environ["OMP_NUM_THREADS"] = "1"

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
    app.run(host="0.0.0.0", port=5000, debug=True)

# Add a simple memory
conversation_history = []

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    global conversation_history
    user_message = request.json.get("message")
    conversation_history.append({"role": "user", "content": user_message})

    # Initialize the conversational pipeline
    conversational_pipeline = pipeline("conversational")

    # Create the conversation object
    conversation = conversational_pipeline(user_message)

    response = get_response(user_message)
    conversation_history.append({"role": "bot", "content": response})
    
    return jsonify({"response": response, "history": conversation_history})
