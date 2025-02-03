from geopy.geocoders import Nominatim
from datetime import datetime

def get_lat_lon(city_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_historical_dates(years_number: int=5):
    
    # create a list of timestamps for the last 5 years relative to today
    # in Timestamp (Unix time, UTC time zone) format
    timestamps = []
    for i in range(1, years_number+1):
        date = datetime.now().replace(year=datetime.now().year-i).timestamp()
        timestamps.append(date)

    return timestamps

# Example usage
# city = "Toronto"
# latitude, longitude = get_lat_lon(city)
# print(f"Latitude: {latitude}, Longitude: {longitude}")