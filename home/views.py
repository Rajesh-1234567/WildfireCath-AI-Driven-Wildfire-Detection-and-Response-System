from django.shortcuts import render,redirect
from datetime import datetime
from home.api_calls.weatherAPI import get_weather_data
from django.views.decorators.csrf import csrf_exempt

#----------------------------------------------------------------------------
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def unix_to_human_readable(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# import io
# import requests
# from django.shortcuts import render, redirect
# from .models import Map

# def generate_map_image(latitude, longitude):
#     api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
#     url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=14&size=350x350&maptype=satellite&key={api_key}"
    
#     response = requests.get(url)
#     if response.status_code == 200:
#         image_io = io.BytesIO(response.content)
#         return image_io
#     else:
#         raise Exception("Error fetching map image")

import io
import requests
from django.shortcuts import render, redirect
from .models import Map

def generate_mappls_image(latitude, longitude):
    api_key = '9440dc184957cb68062acbd0187f20f5'
    url = f"https://apis.mapmyindia.com/advancedmaps/v1/{api_key}/still_image?center={latitude},{longitude}&zoom=14&size=350x350&maptype=hybrid"
    
    response = requests.get(url)
    if response.status_code == 200:
        image_io = io.BytesIO(response.content)
        return image_io
    else:
        raise Exception("Error fetching map image")

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------


@csrf_exempt
def loading(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        weather_data=get_weather_data(latitude,longitude)

        map_image_io = generate_mappls_image(latitude, longitude)
            
        # Create and save Map instance
        map_instance = Map()
        map_instance.map_image.save(f"map_{latitude}_{longitude}.png", map_image_io, save=True)
        # print(latitude)
        # print(longitude)
        request.session['weather_data'] = weather_data
        return redirect("home:home")
    else:
        latitude = 22.7179
        longitude = 75.8333
    return render(request,'home/app/loading_page.html')


def home(request):
    weather_data = request.session.get('weather_data')

    # Convert temperatures to Celsius
    weather_data['main']['temp'] = kelvin_to_celsius(weather_data['main']['temp'])
    weather_data['main']['feels_like'] = kelvin_to_celsius(weather_data['main']['feels_like'])

    # Convert Unix time to human-readable format
    weather_data['sys']['sunrise'] = unix_to_human_readable(weather_data['sys']['sunrise'])
    weather_data['sys']['sunset'] = unix_to_human_readable(weather_data['sys']['sunset'])
    
    context={
        'weather_data':weather_data,
    }
    return render(request,'home/app/home.html',context)