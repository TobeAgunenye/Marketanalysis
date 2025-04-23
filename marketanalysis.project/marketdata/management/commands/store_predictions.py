from django.core.management.base import BaseCommand
from marketdata.models import StockData, MarketPrediction
from marketdata.lstm_model import process_and_predict
import pandas as pd

class Command(BaseCommand):
    help = 'Store predictions for multiple companies'

    def handle(self, *args, **kwargs):
        companies = ['AAPL', 'AMZN', 'TSLA', 'GOOG']
        
        for company in companies:
            stock_data = StockData.objects.filter(company=company).order_by('date')
            
            if stock_data.exists():
                df = pd.DataFrame(list(stock_data.values('date', 'close_price')))
                df.set_index('date', inplace=True)
                
                predicted_prices, prediction_dates = process_and_predict(df)

                for predicted_price, prediction_date in zip(predicted_prices, prediction_dates):
                    # Use the first stock data entry for the company (or modify as needed)
                    company_instance = stock_data.first()  # Use first entry, or modify based on your needs
                    
                    # Replace or create a new prediction entry
                    MarketPrediction.objects.update_or_create(
                        company=company_instance,
                        prediction_date=prediction_date,
                        defaults={'predicted_price': predicted_price, 'confidence_score': 0.9}
                    )
                self.stdout.write(self.style.SUCCESS(f"Predictions for {company} stored successfully."))
            else:
                self.stdout.write(self.style.WARNING(f"No stock data found for {company}."))