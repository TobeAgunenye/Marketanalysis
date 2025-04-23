import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from datetime import timedelta
import pandas as pd

def process_and_predict(df, look_back=60):
    """
    df: DataFrame with 'Close' and datetime index (already sorted by date)
    Returns: predicted_price (float), prediction_date (datetime)
    """
    # 1. Prepare Data
    close_prices = df['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    x_train, y_train = [], []
    for i in range(look_back, len(scaled_data)):
        x_train.append(scaled_data[i - look_back:i, 0])
        y_train.append(scaled_data[i, 0])

    # Print the number of sequences created and the first few sequences for debugging
    print(f"🔍 Number of sequences created: {len(x_train)}")
    if len(x_train) > 0:
        print(f"🔍 First few sequences (x_train): {x_train[:5]}")

    # 2. Check if we have enough data for the model
    if len(x_train) == 0:
        print("❌ No valid training sequences created. Check the dataset or look_back value.")
        return None

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # 3. Build Model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 4. Train the model
    model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)

    # 5. Predict next day
    last_60 = scaled_data[-look_back:]
    last_60 = np.reshape(last_60, (1, look_back, 1))
    predicted_price_scaled = model.predict(last_60, verbose=0)
    predicted_price = scaler.inverse_transform(predicted_price_scaled)[0][0]

    # 6. Set prediction date (day after last date in input)
    last_date = df.index[-1]
    prediction_date = last_date + timedelta(days=1)

    return predicted_price, prediction_date


# Load the dataset
file_path = '/Users/tobeagunenye/Downloads/untitled folder 2/Uni Development project/Project and video resources/MarketAnalysis/marketanalysis.project/cleaned_data/AAPL_final.csv'  # Update the file path if needed
df = pd.read_csv(file_path)

# Ensure 'Date' is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Use the 'Close' column for prediction
df_subset = df[['Close']]

# Ensure df_subset has enough rows (at least 60)
if df_subset.shape[0] < 60:
    print("❌ Not enough data for prediction.")
else:
    # Predict for the last date in the dataset (last available date)
    result = process_and_predict(df_subset.tail(60), look_back=60)

    # If the result is valid, print it
    if result:
        pred, date = result
        print(f"Predicted price for {date}: {pred}")
    else:
        print("❌ Prediction failed. Check the data.")