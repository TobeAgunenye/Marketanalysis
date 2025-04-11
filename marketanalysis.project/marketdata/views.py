from django.shortcuts import render
from django.http import JsonResponse
# from .lstm_model import train_lstm, predict_stock_price
from .models import StockData
from .serializers import StockDataSerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import requests
from textblob import TextBlob
from django.http import JsonResponse
from .models import SentimentAnalysis, StockData
from rest_framework import generics
from rest_framework import generics
from .models import SentimentAnalysis
from .serializers import SentimentAnalysisSerializer
from .lstm_model import process_and_predict
from .models import StockData, MarketPrediction
import pandas as pd


# def train_stock_model(request, stock_symbol):
#     """Train the LSTM model for a stock."""
#     model, _ = train_lstm(stock_symbol)
#     if model:
#         return JsonResponse({"message": f"Model for {stock_symbol} trained successfully."})
#     return JsonResponse({"error": "Failed to train model."}, status=400)

# def get_stock_prediction(request, stock_symbol):
#     """Get stock price predictions."""
#     predictions = predict_stock_price(stock_symbol)
#     if predictions:
#         return JsonResponse({"predictions": predictions})
#     return JsonResponse({"error": "Failed to generate predictions."}, status=400)
# # Create your views here.


class StockDataAPIView(ListAPIView):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['company', 'date']
    ordering_fields = ['date']

    def get_queryset(self):
        company = self.request.query_params.get('company', None)
        if company:
            return StockData.objects.filter(company=company)
        return StockData.objects.none()  # Return no data if company isn't passed

class SentimentAnalysisAPIView(generics.ListCreateAPIView):
    serializer_class = SentimentAnalysisSerializer

    def get_queryset(self):
        # Get the company parameter from the URL
        company_name = self.kwargs['company']  # This grabs the company from the URL
        # Filter the SentimentAnalysis model based on the company
        return SentimentAnalysis.objects.filter(company__company=company_name)  # Ensure 'company' field is used correctly












from django.http import JsonResponse
from .models import StockData, MarketPrediction
import pandas as pd

def update_predictions(request, company):
    try:
        # 1. Query the database
        stock_data_qs = StockData.objects.filter(company=company).order_by('date')
        if not stock_data_qs.exists():
            return JsonResponse({"error": "No stock data found for this company."}, status=404)

        # 2. Convert to DataFrame
        df = pd.DataFrame(list(stock_data_qs.values('date', 'close_price')))
        df.set_index('date', inplace=True)

        # 3. Make prediction using LSTM
        predicted_price, prediction_date = process_and_predict(df)

        # 4. Store prediction
        MarketPrediction.objects.update_or_create(
            company=stock_data_qs.first(),
            prediction_date=prediction_date,
            defaults={
                'predicted_price': predicted_price,
                'confidence_score': 0.9
            }
        )

        return JsonResponse({
            "message": "Prediction successful",
            "company": company,
            "predicted_price": round(float(predicted_price), 2),
            "prediction_date": str(prediction_date),
            })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



















    
NEWS_API_KEY = '4fc2ae96cb50407c86ffdc38779521c8'  # Replace with your NewsAPI key

def fetch_news(company):
    url = f'https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}&language=en'
    response = requests.get(url)
    articles = response.json().get('articles', [])

    print(f"Fetched articles for {company}: {articles}")
    return articles

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Sentiment polarity score (-1 to 1)
    sentiment_label = "neutral"

    if sentiment_score > 0:
        sentiment_label = "positive"
    elif sentiment_score < 0:
        sentiment_label = "negative"

    return sentiment_score, sentiment_label

def store_sentiment_data(company, sentiment_score, sentiment_label, source, article_title):
    # Retrieve the stock data for the company
    stock = StockData.objects.filter(company=company).order_by('-date').first()  # Get the most recent entry for the company
    
    # Store the sentiment data in the SentimentAnalysis model
    sentiment_data = SentimentAnalysis(
        company=stock,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label,
        source=source,  # For example, 'NewsAPI'
        article_title=article_title  # Store the article title
    )
    sentiment_data.save()

def sentiment_analysis(request, company):
    # Step 1: Fetch news articles about the company
    articles = fetch_news(company)

    # Initialize a list to store sentiment data for each article
    sentiment_results = []

    # Step 2: Analyze sentiment for each article
    for article in articles:
        title = article.get('title', 'No title available')  # Default to 'No title available' if None
        description = article.get('description', 'No description available')  # Default if None

        # Safely concatenate title and description to form the text for analysis
        text = f"{str(title)} {str(description)}"  # Ensure both are strings

        sentiment_score, sentiment_label = analyze_sentiment(text)

        # Step 3: Store the sentiment data in the database, including the title
        store_sentiment_data(company, sentiment_score, sentiment_label, article['source']['name'], title)

        sentiment_results.append({
            'title': title,
            'sentiment': sentiment_label,
            'score': sentiment_score,
            'source': article['source']['name']
        })

    # Calculate the average sentiment score
    if sentiment_results:
        avg_score = sum([result['score'] for result in sentiment_results]) / len(sentiment_results)
        avg_sentiment = 'neutral'
        if avg_score > 0:
            avg_sentiment = 'positive'
        elif avg_score < 0:
            avg_sentiment = 'negative'
    else:
        avg_sentiment = 'neutral'
        avg_score = 0

    # Return the sentiment data as a JSON response
    return JsonResponse({
        'company': company,
        'average_sentiment': avg_sentiment,
        'average_score': avg_score,
        'articles': sentiment_results
    })



