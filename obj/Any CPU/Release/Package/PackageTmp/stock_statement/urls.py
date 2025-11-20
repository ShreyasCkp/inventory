from django.urls import path
from .views import stock_statement

urlpatterns = [
    path('stock-statement/', stock_statement, name='stock_statement'),
]
