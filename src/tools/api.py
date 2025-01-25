# this script uses Open Weather API to get the weather data. The API key is stored in the .env file.
import os
import requests, json
from utility.weather import get_lat_lon

# get open weather api key
def get_api_key():
    if not os.environ.get("OPENWEATHER_API_KEY"):
        raise ValueError("OPENWEATHER_API_KEY is not set")
    return os.environ.get("OPENWEATHER_API_KEY")

def get_weather_data(city: str):

    # get the latitude and longitude of the city
    latitude, longitude = get_lat_lon(city)

    # get Open Weather API key  
    api_key = get_api_key()

    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={latitude}&lon={longitude}&appid={api_key}&units=metric&exclude=minutely"
    )
    response = requests.get(url)
    return response.json()