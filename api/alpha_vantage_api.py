import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(symbol):
    """
    Fetches the current stock price for the given symbol from Alpha Vantage.
    :param symbol: Stock ticker symbol (e.g., "AAPL" for Apple)
    :return: Stock price or error message
    """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        try:
            time_series = data["Time Series (1min)"]
            latest_time = list(time_series.keys())[0]
            price = time_series[latest_time]["1. open"]
            return f"The current stock price of {symbol} is ${price}"
        except KeyError:
            return f"Error: {data.get('Note', 'No data found for the symbol.')}"
    else:
        return f"Error: Unable to fetch data. Status Code: {response.status_code}"

if __name__ == "__main__":
    # Test the function
    print(get_stock_price("AAPL"))
