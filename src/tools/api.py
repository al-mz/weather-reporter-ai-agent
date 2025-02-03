# this script uses Open Weather API to get the weather data. The API key is stored in the .env file.
import os
from datetime import datetime
import requests, json
from utility.weather import get_lat_lon
from utility.utils import is_valid_timestamp
from langchain_core.tools import tool

# get open weather api key
def get_api_key():
    if not os.environ.get("OPENWEATHER_API_KEY"):
        raise ValueError("OPENWEATHER_API_KEY is not set")
    return os.environ.get("OPENWEATHER_API_KEY")

@tool
def get_current_and_forecast_weather_data(city_name: str) -> dict:

    """
    Get the current weather and forecast for a given city.
    Current weather and forecasts:
        - minute forecast for 1 hour
        - hourly forecast for 48 hours
        - daily forecast for 8 days
    
    Args:
        city_name: The name of the city for which the weather data is requested.
    
    Returns:
        A dictionary containing the weather data.
    """

    # get the latitude and longitude of the city
    latitude, longitude = get_lat_lon(city_name)

    # get Open Weather API key  
    api_key = get_api_key()

    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={latitude}&lon={longitude}&appid={api_key}&units=metric&exclude=minutely"
    )
    response = requests.get(url)
    return response.json()

@tool
def get_timestamp_weather_data(city_name: str, dates: list) -> dict:
    
    """
    Get access to weather data for any timestamp from 1st January 1979 till 4 days ahead forecast
    for a given city.

    Args:
        city_name: The name of the city for which the weather data is requested.
        dates: A list of timestamps for which the weather data is requested. e.g. [1630000000, 1630000000, 1630000000]
    """
    # https://openweathermap.org/api/one-call-3#history

    # get the latitude and longitude of the city
    latitude, longitude = get_lat_lon(city_name)

    # get Open Weather API key  
    api_key = get_api_key()

    # check if all dates are a timestamp
    for date in dates:
        if not is_valid_timestamp(date):
            raise ValueError("Invalid timestamp, it has to be a Unix timestamp")

    # make sure date is no longer than 4 days ahead
    for date in dates:
        if date > datetime.now().timestamp() + 4 * 24 * 60 * 60:
            raise ValueError("Date is too far in the future, it has to be within 4 days")
        
    responses = {}
    for date in dates:
        url = (
            f"https://api.openweathermap.org/data/3.0/onecall/timemachine?"
            f"lat={latitude}&lon={longitude}&dt={date}&appid={api_key}&units=metric"
        )
        response = requests.get(url)
        responses[date] = response.json()

    return responses