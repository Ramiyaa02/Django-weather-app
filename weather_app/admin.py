from django.contrib import admin
from .models import WeatherSearch

@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ['city', 'country', 'temperature', 'user', 'searched_at']
    list_filter = ['searched_at', 'country']
    search_fields = ['city', 'country']