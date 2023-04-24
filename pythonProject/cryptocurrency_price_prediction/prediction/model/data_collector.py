import datetime
from typing import Union, List, Dict

import numpy as np
import pandas as pd
import requests

Timestamp = Union[datetime.datetime, datetime.date, int, float]

api_key = '53f1b0c88b99983eb9655c0465be9c77e817ad7f0cbe3995234cb96e8601bfd7'


def get_historical_data(symbol, start_date, end_date):
    # api_key = '53f1b0c88b99983eb9655c0465be9c77e817ad7f0cbe3995234cb96e8601bfd7'
    url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym=USD&limit=2000&api_key={api_key}&toTs={end_date}&extraParams=crypto_price_prediction'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx HTTP status codes
        data = response.json()['Data']['Data']
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[['time', 'close', 'open']]
        df.columns = ['Date', 'Price', 'Open']
        df = df.set_index('Date')
        date = datetime.datetime.fromtimestamp(start_date).strftime('%Y-%m-%d')
        return df.loc[df.index >= date]
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing data: {e}")
        return None


def preprocess_data(data):
    data['Return'] = (data['Price'] - data['Open']) / data['Open']
    data = data.dropna()
    data = data.drop(['Open'], axis=1)
    return data


def add_features(data):
    data['MA7'] = data['Price'].rolling(window=7).mean()
    data['MA21'] = data['Price'].rolling(window=21).mean()
    data['MA50'] = data['Price'].rolling(window=50).mean()
    data['EMA'] = data['Price'].ewm(com=0.5).mean()
    data['Momentum'] = data['Price'] / data['Price'].shift(7)
    data['Log_Ret'] = np.log(data['Price'] / data['Price'].shift(1))
    data['Volatility'] = data['Log_Ret'].rolling(window=7).std()
    data['RSI'] = compute_RSI(data['Price'], window=14)
    return data


def compute_RSI(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    RS = avg_gain / avg_loss
    RSI = 100 - (100 / (1 + RS))
    return RSI


def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    headers = {'authorization': api_key}
    response = requests.get(url, headers=headers)
    news_data = response.json()['Data']
    return news_data


def get_coin_list():
    important_coins = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH'] # List of important coins

    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    response = requests.get(url)
    data = response.json()

    coin_list = []
    for coin, coin_data in data['Data'].items():
        if coin in important_coins:
            coin_list.append((coin, coin_data['FullName']))

    return coin_list
