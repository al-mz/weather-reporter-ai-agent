from geopy.geocoders import Nominatim

def get_lat_lon(city_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Example usage
city = "Toronto"
latitude, longitude = get_lat_lon(city)
print(f"Latitude: {latitude}, Longitude: {longitude}")