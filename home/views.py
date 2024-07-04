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

# def generate_mappls_image(latitude, longitude):
#     api_key = '9440dc184957cb68062acbd0187f20f5'
#     url = f"https://apis.mapmyindia.com/advancedmaps/v1/{api_key}/still_image?center={latitude},{longitude}&zoom=14&size=350x350&maptype=hybrid"
    
#     response = requests.get(url)
#     if response.status_code == 200:
#         image_io = io.BytesIO(response.content)
#         return image_io
#     else:
#         raise Exception("Error fetching map image")
import io
import math
import requests
from PIL import Image
from django.shortcuts import render, redirect
from .models import Map

def get_map_tile_url(x, y, z, api_key):
    url = f"https://api.maptiler.com/maps/hybrid/{z}/{x}/{y}.jpg?key={api_key}"
    print(f"Fetching tile from URL: {url}")
    return url

def get_tile_coordinates(lat, lon, zoom):
    lat = float(lat)
    lon = float(lon)
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    
    print(f"Tile coordinates for lat={lat}, lon={lon}, zoom={zoom}: x={x_tile}, y={y_tile}")
    return x_tile, y_tile

def fetch_tile_image(x, y, z, api_key):
    url = get_map_tile_url(x, y, z, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        raise Exception(f"Error fetching map tile from URL: {url}, Status Code: {response.status_code}")

def generate_map_image(lat, lon, api_key):
    zoom = 14
    x_tile, y_tile = get_tile_coordinates(lat, lon, zoom)
    
    # Fetch the central tile
    tile = fetch_tile_image(x_tile, y_tile, zoom, api_key)
    
    # Crop the image to 256x256 (it should already be 256x256 but this is to ensure the correct size)
    tile = tile.crop((0, 0, 256, 256))
    
    # Save image to a BytesIO object
    image_io = io.BytesIO()
    tile.save(image_io, format='PNG')
    image_io.seek(0)
    
    return image_io

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------


@csrf_exempt
def loading(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        weather_data=get_weather_data(latitude,longitude)

        api_key = 'WeDkOLJgAzvafGXb9MVB'
        map_image_io = generate_map_image(latitude, longitude, api_key)
        
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