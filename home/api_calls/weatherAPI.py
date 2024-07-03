import requests

# weather api key
weather_api="0ecd5437269046193ac6acb87f964e0c"

def get_weather_data(latitude,longitude):

    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_api}"

    response = requests.get(api_url)
    weather_data = response.json()
    return weather_data