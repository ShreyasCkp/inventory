
from django.urls import path
from . import views


urlpatterns = [
    # Your other URL patterns...
    path('dashboard/', views.dashboard_view, name='dashboard'),
]