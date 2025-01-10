import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("YAHOO_FINANCE_API_KEY")
BASE_URL = "https://yahoo-finance-api-endpoint"

def get_stock_price(symbol):
    url = f"{BASE_URL}/stock/{symbol}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["price"]
    else:
        return f"Error: {response.status_code} - {response.text}"
