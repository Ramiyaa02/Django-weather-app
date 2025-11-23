from django import forms

class WeatherSearchForm(forms.Form):
    city_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter city name...'
        })
    )