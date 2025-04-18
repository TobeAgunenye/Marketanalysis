from django.shortcuts import render
from django.http import JsonResponse
# from .lstm_model import train_lstm, predict_stock_price
from .models import StockData
from .serializers import StockDataSerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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