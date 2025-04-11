import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from datetime import timedelta









def process_and_predict(df, look_back=60):
    """
    df: DataFrame with 'close_price' and datetime index (already sorted by date)
    Returns: predicted_price (float), prediction_date (datetime)
    """
    # 1. Prepare Data
    close_prices = df['close_price'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    x_train, y_train = [], []
    for i in range(look_back, len(scaled_data)):
        x_train.append(scaled_data[i - look_back:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # 2. Build Model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 3. Train
    model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)

    # 4. Predict next day
    last_60 = scaled_data[-look_back:]
    last_60 = np.reshape(last_60, (1, look_back, 1))
    predicted_price_scaled = model.predict(last_60, verbose=0)
    predicted_price = scaler.inverse_transform(predicted_price_scaled)[0][0]

    # 5. Set prediction date (day after last date in input)
    last_date = df.index[-1]
    prediction_date = last_date + timedelta(days=1)


    return predicted_price, prediction_date

def backtest_predictions(df, look_back=60, start_date="2019-01-01"):
    """
    Simulates daily predictions from a given start_date using rolling LSTM training.
    Returns a list of dicts with prediction info.
    """
    from datetime import timedelta

    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    predictions = []

    # Start index
    if start_date not in df.index:
        raise ValueError(f"Start date {start_date} not found in data.")

    start_idx = df.index.get_loc(start_date)

    for i in range(start_idx, len(df) - 1):
        window_df = df.iloc[i - look_back:i]
        actual_price = df.iloc[i + 1]['close_price']
        prediction_date = df.index[i + 1]

        try:
            predicted_price, _ = process_and_predict(window_df, look_back=look_back)
        except Exception as e:
            print(f"Skipping {prediction_date} due to error: {e}")
            continue

        predictions.append({
            "date": prediction_date,
            "predicted": predicted_price,
            "actual": actual_price
        })

    return predictions