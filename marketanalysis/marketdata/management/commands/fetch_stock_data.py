import yfinance as yf
import pandas as pd
from django.core.management.base import BaseCommand
from marketdata.models import MarketData
from django.db import connection, IntegrityError

# Define the stock symbols to fetch
STOCK_SYMBOLS = ["AAPL", "GOOGL", "TSLA", "MSFT"]

# Define the date range
START_DATE = "2020-01-01"
END_DATE = "2025-03-01"

class Command(BaseCommand):
    help = "Fetch stock data from Yahoo Finance and store in the database"

    def handle(self, *args, **kwargs):
        self.clear_existing_data()  # Clears existing data
        self.fetch_and_store_stock_data()

    def clear_existing_data(self):
        """Delete all previous stock data."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM marketdata_marketdata;")
        print("✅ Existing stock data cleared.")

    def fetch_and_store_stock_data(self):
        """Fetch stock data for each symbol and store it in the database."""

        all_data = []

        for symbol in STOCK_SYMBOLS:
            print(f"🔄 Fetching {symbol} stock data from Yahoo Finance...")

            try:
                # Fetch stock data from Yahoo Finance
                stock_info = yf.Ticker(symbol)  # Get company info
                stock_data = stock_info.history(start=START_DATE, end=END_DATE)

                if stock_data.empty:
                    print(f"❌ No data found for {symbol}")
                    continue

                # Fetch additional metadata
                company_name = stock_info.info.get("longName", "Unknown Company")
                market_cap = stock_info.info.get("marketCap", None)

                # Reset index to move 'Date' into a column
                stock_data.reset_index(inplace=True)

                # Keep only the necessary columns
                stock_data["stock_symbol"] = symbol
                stock_data["company_name"] = company_name
                stock_data["market_cap"] = market_cap
                stock_data = stock_data[['Date', 'Close', 'stock_symbol', 'company_name', 'market_cap']]
                stock_data.rename(columns={"Date": "date_collected", "Close": "stock_price"}, inplace=True)

                # Append fetched data
                all_data.extend(stock_data.values.tolist())

            except Exception as e:
                print(f"❌ Error fetching data for {symbol}: {e}")

        # Convert to DataFrame and sort by date
        df = pd.DataFrame(all_data, columns=["date_collected", "stock_price", "stock_symbol", "company_name", "market_cap"])
        df["date_collected"] = pd.to_datetime(df["date_collected"])
        df.sort_values(by=["date_collected", "stock_symbol"], inplace=True)  # Sort by date first, then stock symbol

        # Store in the database
        self.store_in_database(df)

        print("✅ Stock data successfully stored!")

    def store_in_database(self, df):
        """Insert stock data into the database while avoiding duplicates."""
        for _, row in df.iterrows():
            try:
                MarketData.objects.create(
                    stock_symbol=row["stock_symbol"],
                    company_name=row["company_name"],
                    market_cap=row["market_cap"],
                    date_collected=row["date_collected"],
                    stock_price=row["stock_price"]
                )
            except IntegrityError:
                print(f"⚠️ Duplicate entry skipped for {row['stock_symbol']} on {row['date_collected']}")








                                        #Alpha Vantage API details (daily limit of 5 requests)

# class Command(BaseCommand):
#     """           
#     Django management command to fetch real-time stock prices and company details from Alpha Vantage.
#     The script saves the data into MySQL, updating records if the stock symbol already exists.
#     """
#     help = "Fetch stock prices and company names from Alpha Vantage and store in MySQL"

#     # Alpha Vantage API details
#     API_KEY = settings.ALPHA_VANTAGE_API_KEY
#     BASE_URL_PRICE = "https://www.alphavantage.co/query"  # API endpoint for stock prices
#     BASE_URL_COMPANY = "https://www.alphavantage.co/query"  # API endpoint for company info

#     def fetch_stock_data(self, symbol):
#         """
#         Fetches stock price and company details for a given symbol from Alpha Vantage API.
#         If the stock exists in the database, updates its price; otherwise, creates a new entry.
#         """

#         # Step 1: Fetch Stock Price
#         price_params = {
#             "function": "TIME_SERIES_INTRADAY",
#             "symbol": symbol,
#             "interval": "5min",
#             "apikey": self.API_KEY
#         }
#         price_response = requests.get(self.BASE_URL_PRICE, params=price_params)
#         price_data = price_response.json()

#         if "Time Series (5min)" in price_data:
#             latest_time = list(price_data["Time Series (5min)"].keys())[0]  # Get latest timestamp
#             latest_data = price_data["Time Series (5min)"][latest_time]  # Extract latest stock data
#             stock_price = float(latest_data["1. open"])  # Convert stock price to float
#         else:
#             self.stdout.write(self.style.ERROR(f"Error fetching stock price for {symbol}: {price_data}"))
#             return  # Stop execution if price data is missing

#         # Step 2: Fetch Company Name & Market Capitalization
#         company_params = {
#             "function": "OVERVIEW",  # API function to get company details
#             "symbol": symbol,
#             "apikey": self.API_KEY
#         }
#         company_response = requests.get(self.BASE_URL_COMPANY, params=company_params)
#         company_data = company_response.json()

#         company_name = company_data.get("Name", "Unknown")  # Get company name (default: "Unknown")
#         market_cap = company_data.get("MarketCapitalization", None)  # Get market cap (None if missing)

#         # Step 3: Check If Stock Already Exists & Log Changes
#         existing_entry = MarketData.objects.filter(stock_symbol=symbol).first()

#         if existing_entry:
#             old_price = existing_entry.stock_price
#             self.stdout.write(self.style.WARNING(
#                 f"Updating {symbol}: Old Price: ${old_price} → New Price: ${stock_price}"
#             ))
#         else:
#             self.stdout.write(self.style.SUCCESS(f"New Stock Added: {symbol} - {company_name}: ${stock_price}"))

#         # Step 4: Save Data to MySQL (Update Existing Entries)
#         try:
#             stock_entry, created = MarketData.objects.update_or_create(
#                 stock_symbol=symbol,
#                 defaults={
#                     "stock_price": stock_price,
#                     "company_name": company_name,
#                     "market_cap": market_cap
#                 }
#             )
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f"Successfully added {symbol} - {company_name}: ${stock_price}"))
#             else:
#                 self.stdout.write(self.style.SUCCESS(f"Successfully updated {symbol} - {company_name}: ${stock_price}"))

#         except IntegrityError:
#             self.stdout.write(self.style.ERROR(f"Failed to update {symbol}"))

#     def handle(self, *args, **kwargs):
#         """
#         Runs the script for multiple stock symbols.
#         Modify the stock list based on your needs.
#         """
#         stock_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]  # List of stocks to track
#         for symbol in stock_symbols:
#             self.fetch_stock_data(symbol)  # Fetch and store data for each stock
    




