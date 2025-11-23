from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WeatherSearch
from .weather_service import WeatherService
from .forms import WeatherSearchForm

def weather_search(request):
    weather_data = None
    error = None
    
    if request.method == 'POST':
        form = WeatherSearchForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            
            # Get weather data from API
            weather_data = WeatherService.get_weather_data(city_name)
            
            if 'error' not in weather_data:
                # Save search to database (if user is logged in)
                if request.user.is_authenticated:
                    WeatherSearch.objects.create(
                        user=request.user,
                        city=weather_data['city'],
                        country=weather_data['country'],
                        temperature=weather_data['temperature'],
                        description=weather_data['description']
                    )
            else:
                error = weather_data['error']
    else:
        form = WeatherSearchForm()
    
    return render(request, 'weather_app/search.html', {
        'form': form,
        'weather_data': weather_data,
        'error': error
    })

@login_required
def search_history(request):
    searches = WeatherSearch.objects.filter(user=request.user).order_by('-searched_at')
    return render(request, 'weather_app/history.html', {'searches': searches})

@login_required
def delete_search(request, search_id):
    search = get_object_or_404(WeatherSearch, id=search_id, user=request.user)
    if request.method == 'POST':
        search.delete()
        return redirect('search_history')
    return render(request, 'weather_app/confirm_delete.html', {'search': search})