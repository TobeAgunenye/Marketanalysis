import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from datetime import timedelta

def process_and_predict(df, look_back=60, forecast_days=365):
    """
    df: DataFrame with 'close_price' and datetime index (already sorted by date)
    forecast_days: Number of days to predict into the future (set to 365 for a year)
    Returns: predicted_prices (list of floats), prediction_dates (list of datetimes)
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

    # 4. Predict next 'forecast_days' days
    predictions = []
    last_60 = scaled_data[-look_back:]
    last_60 = np.reshape(last_60, (1, look_back, 1))

    for _ in range(forecast_days):
        predicted_price_scaled = model.predict(last_60, verbose=0)
        predicted_price = scaler.inverse_transform(predicted_price_scaled)[0][0]
        predictions.append(predicted_price)
        
        # Update the input for the next day by appending the predicted value
        last_60 = np.append(last_60[:, 1:, :], predicted_price_scaled.reshape(1, 1, 1), axis=1)

    # 5. Set prediction dates (the next 'forecast_days' days after the last date in input)
    last_date = df.index[-1]
    prediction_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]

    return predictions, prediction_dates