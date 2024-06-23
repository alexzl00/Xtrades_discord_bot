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


def fetch_kline(from_user_message=True) -> str:

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
        # print(prices)

        bar_times = [(datetime.fromtimestamp(int(time[0])/1000)).strftime('%Y-%m-%d %H:%M:%S') for time in response.json()['result']['list']]
        # print(bar_times)

        rsi = count_RSI(prices)

        if rsi >= 70:
            return f'Hurry up not to miss the chance to SELL!\nRSI is {rsi}!'

        if rsi <= 30:
            return f'Hurry up not to miss the chance to BUY!\nRSI is {rsi}!'
        
        if from_user_message:
            return f'No sense to make new ORDER!\nRSI is only {rsi}'
    else:
        print(f"Error: {response.status_code} - {response.text}")