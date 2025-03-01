import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from .models import MarketData

def load_stock_data(stock_symbol, look_back=60):
    """Load historical stock data from the database."""
    data = MarketData.objects.filter(stock_symbol=stock_symbol).order_by("date_collected").values("stock_price")
    df = pd.DataFrame(data)
    
    if df.empty:
        print(f"No data found for {stock_symbol}")
        return None, None

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)

    x_train, y_train = [], []
    for i in range(look_back, len(scaled_data)):
        x_train.append(scaled_data[i - look_back:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return x_train, y_train, scaler

def train_lstm(stock_symbol):
    """Train an LSTM model on a given stock."""
    x_train, y_train, scaler = load_stock_data(stock_symbol)

    if x_train is None:
        return None

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=10)

    model.save(f"marketanalysis/marketdata/models/{stock_symbol}_lstm.h5")
    return model, scaler

def predict_stock_price(stock_symbol, days_ahead=30):
    """Use the trained LSTM model to predict stock prices."""
    from tensorflow.keras.models import load_model
    import datetime

    try:
        model = load_model(f"marketanalysis/marketdata/models/{stock_symbol}_lstm.h5")
    except:
        print("Model not found. Training new model...")
        model, scaler = train_lstm(stock_symbol)

    x_train, _, scaler = load_stock_data(stock_symbol)

    if x_train is None:
        return None

    last_lookback = x_train[-1].reshape(1, x_train.shape[1], 1)
    predictions = []

    for _ in range(days_ahead):
        predicted_price = model.predict(last_lookback)
        predictions.append(predicted_price[0][0])
        last_lookback = np.append(last_lookback[:, 1:, :], [[predicted_price]], axis=1)

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    return [(datetime.date.today() + datetime.timedelta(days=i), price[0]) for i, price in enumerate(predictions)]