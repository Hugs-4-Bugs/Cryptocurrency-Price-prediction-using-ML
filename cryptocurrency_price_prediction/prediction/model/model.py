from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import pandas as pd


def train_model(data):
    print(data)
    df = pd.DataFrame(data)
    df = df.dropna()
    X = df.drop(['Price', 'Return'], axis=1)
    y_price = df['Price']
    y_return = df['Return']

    X_train, X_test, y_price_train, y_price_test, y_return_train, y_return_test = train_test_split(X, y_price, y_return, test_size=0.2, shuffle=False)

    # Train price prediction model
    model_price = LinearRegression()
    model_price.fit(X_train, y_price_train)

    # Train return prediction model
    model_return = LinearRegression()
    model_return.fit(X_train, y_return_train)

    actual_prices = model_price.predict(X_test)

    return actual_prices, model_price, model_return, X_test, y_price_test, y_return_test
