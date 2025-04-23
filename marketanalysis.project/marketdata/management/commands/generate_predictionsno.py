from django.core.management.base import BaseCommand
from marketdata.models import StockData, MarketPrediction
from marketdata.lstm_model import backtest_predictions
import pandas as pd

class Command(BaseCommand):
    help = 'Generate LSTM predictions from 2019 to 2021 and save to MarketPrediction table'

    def add_arguments(self, parser):
        parser.add_argument('company', type=str, help='Stock ticker (e.g. AAPL, AMZN, GOOG, TSLA)')

    def handle(self, *args, **kwargs):
        company = kwargs['company'].upper()

        # Load stock data
        stock_qs = StockData.objects.filter(company=company).order_by('date')
        if not stock_qs.exists():
            self.stdout.write(self.style.ERROR(f"No stock data found for {company}"))
            return

        df = pd.DataFrame(list(stock_qs.values('date', 'close_price')))
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
        df = df[df.index <= pd.to_datetime("2021-12-31")]

        # Run backtest
        self.stdout.write(f"Running LSTM backtest for {company} from 2019 onward...")
        results = backtest_predictions(df, start_date="2019-01-01")

        # Save predictions
        count = 0
        for row in results:
            stock_entry = stock_qs.filter(date=row['date']).first()
            if not stock_entry:
                continue

            MarketPrediction.objects.update_or_create(
                company=stock_entry,
                prediction_date=row['date'],
                defaults={
                    'predicted_price': row['predicted'],
                    'confidence_score': 0.9
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Saved {count} predictions for {company} from 2019 to 2021."))
