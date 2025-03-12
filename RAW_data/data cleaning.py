import pandas as pd

# Load TSLA dataset
tsla_df = pd.read_csv("TSLA.csv", parse_dates=["Date"])
tsla_df.set_index("Date", inplace=True)

# Load GOOGL dataset (used as a reference for trading days)
googl_df = pd.read_csv("google.csv", parse_dates=["Date"])
googl_df.set_index("Date", inplace=True)

# Creating a full trading calendar from the GOOGL dataset
full_dates = googl_df.index

# Reindex TSLA to match GOOGL's trading days
tsla_fixed = tsla_df.reindex(full_dates)

# Fill missing values using forward-fill method (propagating the last known price)
tsla_fixed.fillna(method="ffill", inplace=True)

# Ensure all values have consistent 2 decimal places
tsla_fixed = tsla_fixed.round(2)

# Save the corrected TSLA dataset
tsla_fixed.to_csv("TSLA_fixed.csv")

print("TSLA dataset has been fixed and saved as 'TSLA_fixed.csv'")
