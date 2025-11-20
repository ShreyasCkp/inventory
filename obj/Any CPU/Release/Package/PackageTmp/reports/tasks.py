
from celery import shared_task
from reports.models import StockStatement

@shared_task
def update_all_stock_statements():
    for stock in StockStatement.objects.all():
        stock.update_stock()
    return "Stock updated successfully!"

from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

@shared_task
def send_stock_alerts():
    low_stock_items = StockStatement.objects.filter(balance__lte=10)  # Change threshold as needed
    for stock in low_stock_items:
        message = f"Low stock alert: {stock.product_name} has only {stock.balance} units left!"

        # Send Email
        send_mail(
            'Low Stock Alert',
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['admin@example.com'],  # Change to actual recipient email
        )

        # Send SMS (using Twilio)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to='+91XXXXXXXXXX'  # Replace with recipient number
        )
