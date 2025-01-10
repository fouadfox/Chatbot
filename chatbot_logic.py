import random
#from transformers import pipeline, Conversation
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from api.finance_api import get_stock_price

# Section 1: Basic Keyword Matching
basic_responses = {
    "hello": ["Hi there!", "Hello! How can I help you?"],
    "how are you": ["I'm just a program, but I'm here to help!", "I'm good, thanks for asking!"],
    "bye": ["Goodbye!", "See you later!"]
}

def basic_response(user_input):
    """
    Match user input with basic keywords and return a random response.
    """
    for keyword, replies in basic_responses.items():
        if keyword in user_input.lower():
            return random.choice(replies)
    return None

# Section 2: Pre-trained Conversational Model
# Load the conversational model (DialoGPT)
# <-- 
# chat_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

# def conversational_response(user_input):
#     """
#     Generate a response using a conversational model.
#     """
#     conversation = chat_pipeline(user_input)
#     return conversation[0]["generated_text"]
# -->
# Set up the text-generation pipeline
chat_pipeline = pipeline(task="text-generation", model="microsoft/DialoGPT-medium")

def get_response(user_input):
    # Create a Conversation object to manage context
    conversation = Conversation(user_input)
    result = chat_pipeline(conversation)
    return result.generated_responses[0]
# Section 3: Intent Detection with Sentence Transformers
# Load sentence transformer model
intent_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define intents and responses
intents = {
    "greeting": ["hello", "hi", "hey"],
    "farewell": ["bye", "goodbye", "see you later"],
    "thanks": ["thank you", "thanks", "appreciate it"]
}

intent_responses = {
    "greeting": "Hello! How can I assist you today?",
    "farewell": "Goodbye! Have a great day!",
    "thanks": "You're welcome!"
}

def detect_intent(user_input):
    """
    Detect the intent of user input using similarity scoring.
    """
    max_similarity = 0
    best_intent = None
    user_embedding = intent_model.encode(user_input)

    for intent, examples in intents.items():
        example_embeddings = intent_model.encode(examples)
        similarity = util.pytorch_cos_sim(user_embedding, example_embeddings).max().item()
        if similarity > max_similarity:
            max_similarity = similarity
            best_intent = intent

    return best_intent if max_similarity > 0.5 else None

def intent_response(user_input):
    """
    Generate a response based on detected intent.
    """
    intent = detect_intent(user_input)
    if intent:
        return intent_responses[intent]
    return None

# Section 4: Stock Price Query with Alpha Vantage
def stock_price_response(user_input):
    """
    Check for stock price queries and fetch data.
    """
    if "stock" in user_input.lower():
        symbol = user_input.split()[-1]  # Extract stock symbol
        return get_stock_price(symbol)
    return None

# Unified `get_response` Function
def get_response(user_input):
    """
    Determine the appropriate response method for the user input.
    """
    # Check for basic responses
    response = basic_response(user_input)
    if response:
        return response

    # Check for intent-based responses
    response = intent_response(user_input)
    if response:
        return response

    # Check for stock price queries
    response = stock_price_response(user_input)
    if response:
        return response

    # Fall back to conversational model
    return conversational_response(user_input)
