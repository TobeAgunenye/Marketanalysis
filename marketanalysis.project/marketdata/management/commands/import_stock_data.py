import pandas as pd
from django.core.management.base import BaseCommand
from marketdata.models import StockData

class Command(BaseCommand):
    help = 'Bulk import stock data from CSV files'

    def handle(self, *args, **kwargs):
        files = {
            'AAPL': 'cleaned_data/AAPL_final.csv',
            'AMZN': 'cleaned_data/AMZN_final.csv',
            'GOOG': 'cleaned_data/google.csv',
            'TSLA': 'cleaned_data/TSLA_fixed.csv'
        }

        for company, file_path in files.items():
            self.stdout.write(self.style.NOTICE(f'Importing {company} stock data...'))
            df = pd.read_csv(file_path, parse_dates=['Date'])

            stock_entries = []
            for _, row in df.iterrows():
                stock_entries.append(StockData(
                    company=company,
                    date=row['Date'],
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                ))

            # Bulk insert all rows at once (super fast)
            StockData.objects.bulk_create(stock_entries, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {company} stock data!'))
