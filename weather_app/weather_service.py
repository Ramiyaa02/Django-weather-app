import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    @classmethod
    def get_weather_data(cls, city_name):
        # First try OpenWeatherMap
        owm_result = cls._try_openweathermap(city_name)
        if 'error' not in owm_result:
            return owm_result
        
        # If OpenWeatherMap fails, try alternative API
        return cls._try_alternative_api(city_name)
    
    @classmethod
    def _try_openweathermap(cls, city_name):
        """Try to get data from OpenWeatherMap"""
        try:
            params = {
                'q': city_name,
                'appid': cls.API_KEY,
                'units': 'metric'
            }
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return cls._parse_weather_data(response.json())
        except requests.exceptions.RequestException:
            return {'error': 'OpenWeatherMap not available yet'}
        except KeyError:
            return {'error': 'City not found'}
    
    @classmethod
    def _try_alternative_api(cls, city_name):
        """Use alternative API while OpenWeatherMap activates"""
        try:
            # Using wttr.in API as backup (no API key needed)
            url = f"http://wttr.in/{city_name}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': city_name,
                    'country': 'N/A',
                    'temperature': data['current_condition'][0]['temp_C'],
                    'feels_like': data['current_condition'][0]['FeelsLikeC'],
                    'description': data['current_condition'][0]['weatherDesc'][0]['value'],
                    'humidity': data['current_condition'][0]['humidity'],
                    'wind_speed': data['current_condition'][0]['windspeedKmph'],
                    'icon': cls._get_weather_icon(data['current_condition'][0]['weatherDesc'][0]['value'])
                }
            else:
                return {'error': 'Failed to fetch weather data from alternative source'}
                
        except Exception as e:
            return {'error': f'Alternative API failed: {str(e)}'}
    
    @classmethod
    def _parse_weather_data(cls, data):
        """Parse OpenWeatherMap data (will be used when API key activates)"""
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }
    
    @classmethod
    def _get_weather_icon(cls, description):
        """Convert weather description to emoji icon"""
        description = description.lower()
        if 'sun' in description or 'clear' in description:
            return '☀️'
        elif 'cloud' in description:
            return '☁️'
        elif 'rain' in description:
            return '🌧️'
        elif 'snow' in description:
            return '❄️'
        elif 'storm' in description or 'thunder' in description:
            return '⛈️'
        else:
            return '🌤️'