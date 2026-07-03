# backend/trips/urls.py
from django.urls import path
from .views import TripAnalysisView

urlpatterns = [
    path('analyze/', TripAnalysisView.as_view(), name='analyze'),
]