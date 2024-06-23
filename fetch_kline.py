import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import talib
import numpy as np

load_dotenv()

API_KEY = os.getenv('API_KYE')
API_SECRET = os.getenv('API_SECRET')

def count_RSI(prices: list) -> float:
    numpy_prices = np.array(prices, dtype=np.float64)

    rsi = talib.RSI(numpy_prices, timeperiod=14)
    return np.round(rsi[-1], decimals=2)

# from_user_message if set to true means that the function was called by a user message
def fetch_kline(from_user_message: bool = True) -> str:

    # Define the URL and parameters
    base_url = 'https://api-testnet.bybit.com'
    endpoint = '/v5/market/kline'
    params = {
        'category': 'inverse',
        'symbol': 'SOLUSDT',
        'interval': '60',
        'limit': 15 # fetch 15 latest hours, to count RSI with talib with period of 14 you need to fetch at least 15 bars
    }
    response = requests.get(f"{base_url}{endpoint}", params=params)

    if response.status_code == 200:
        prices = [float(price[4]) for price in response.json()['result']['list']] # price[4] is the close price of bar

        rsi = count_RSI(prices)

        if rsi >= 70:
            return f'Hurry up not to miss the chance to SELL!\nRSI is {rsi}!'

        if rsi <= 30:
            return f'Hurry up not to miss the chance to BUY!\nRSI is {rsi}!'
        
        # if user sent the message, otherwise it is not sent to Discord
        if from_user_message:
            return f'No sense to make new ORDER!\nRSI is only {rsi}'
        
        # we will not send any message to Discord
        return 'not send'
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 'error'