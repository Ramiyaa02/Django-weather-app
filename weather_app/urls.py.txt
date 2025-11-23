from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_search, name='weather_search'),
    path('history/', views.search_history, name='search_history'),
    path('delete/<int:search_id>/', views.delete_search, name='delete_search'),
]