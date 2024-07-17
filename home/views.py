from django.shortcuts import render,redirect
from datetime import datetime
from home.api_calls.weatherAPI import get_weather_data
from django.views.decorators.csrf import csrf_exempt
from home.AI_Model.ai_train import predict_fire

from django.conf import settings
import os

from .forms import ImageUploadForm

#----------------------------------------------------------------------------
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def unix_to_human_readable(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
#----------------------------------------------------------------------------

@csrf_exempt
def loading(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        weather_data = get_weather_data(latitude, longitude)
        
        request.session['weather_data'] = weather_data
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        return redirect("home:home")
    else:
        latitude = 22.7179
        longitude = 75.8333
    return render(request, 'home/app/loading_page.html')

def home(request):
    weather_data = request.session.get('weather_data')
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    # Convert temperatures to Celsius
    weather_data['main']['temp'] = kelvin_to_celsius(weather_data['main']['temp'])
    weather_data['main']['feels_like'] = kelvin_to_celsius(weather_data['main']['feels_like'])

    # Convert Unix time to human-readable format
    weather_data['sys']['sunrise'] = unix_to_human_readable(weather_data['sys']['sunrise'])
    weather_data['sys']['sunset'] = unix_to_human_readable(weather_data['sys']['sunset'])

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            result = predict_fire(image_path)
            return render(request, 'result.html', {'result': result, 'image_path': image_path})
    else:
        form = ImageUploadForm()

    context = {
        'form':form,
        'weather_data': weather_data,
        'longitude': longitude,
        'latitude': latitude,
    }
    return render(request, 'home/app/home.html', context)

def mapview(request):
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    api_key = 'WeDkOLJgAzvafGXb9MVB'
    context = {
        'longitude': longitude,
        'latitude': latitude,
        'api_key_map': api_key,
    }
    return render(request, 'home/app/map.html', context)


