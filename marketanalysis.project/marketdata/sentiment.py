import requests
from datetime import datetime


NEWS_API_KEY = '4fc2ae96cb50407c86ffdc38779521c8'  # Your NewsAPI key

def fetch_news(company):
    url = f'https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}&language=en'
    response = requests.get(url)
    articles = response.json().get('articles', [])

    return articles  # List of articles