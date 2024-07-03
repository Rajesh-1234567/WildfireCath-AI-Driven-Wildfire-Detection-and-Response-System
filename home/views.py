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


@csrf_exempt
def loading(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        weather_data=get_weather_data(latitude,longitude)
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