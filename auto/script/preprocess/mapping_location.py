import pandas as pd
import requests
import math
import numpy as np

SEARCH_TEXT_URL = 'https://places.googleapis.com/v1/places:searchText'
NEARBY_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
API_KEY = 'AIzaSyBq1Wtzs3oxCnJAZzveUNcnL8MxDa4WDp8'
radius = 2000

def get_lat_long(api_key, address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Geocoding failed for {address}: {data['status']}")
            return None, None
    else:
        print(f"Request failed with status code {response.status_code}")
        return None, None

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0
    return c * r

def get_places_data(lat, lon, radius, place_type):
    url = f"{NEARBY_SEARCH_URL}?location={lat},{lon}&radius={radius}&type={place_type}&key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            return haversine(lat, lon, location['lat'], location['lng'])
        else:
            print(f"No {place_type} found near the location")
            return np.nan
    else:
        print(f"Request failed with status code {response.status_code}")
        return np.nan

def get_places_bytext(lat, lon, radius, text_query):
    request_body = {
        "textQuery": text_query,
        'locationBias': {
            'circle': {
                'center': {"latitude": lat, "longitude": lon},
                'radius': radius
            }
        },
        'pageSize': 1
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.formattedAddress,places.displayName,places.location'
    }

    response = requests.post(SEARCH_TEXT_URL, json=request_body, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'places' in data and len(data['places']) > 0:
            location = data['places'][0]['location']
            return haversine(lat, lon, location['latitude'], location['longitude'])
        else:
            print(f"No {text_query} found near the location")
            return np.nan
    else:
        print(f"Request failed with status code {response.status_code}")
        return np.nan

def add_location_data(df, unique_location):
    unique_location['Latitude'] = None
    unique_location['Longitude'] = None
    
    for i, row in unique_location.iterrows():
        address = f"{row['Kecamatan']}, Surabaya, Indonesia"
        lat, long = get_lat_long(API_KEY, address)
        if lat and long:
            unique_location.at[i, 'Latitude'] = lat
            unique_location.at[i, 'Longitude'] = long

    unique_location['Distance_GerbangTol'] = unique_location.apply(lambda row: get_places_bytext(row['Latitude'], row['Longitude'], radius, 'Gerbang Tol'), axis=1)
    unique_location['Distance_School'] = unique_location.apply(lambda row: get_places_data(row['Latitude'], row['Longitude'], radius, 'school'), axis=1)
    unique_location['Distance_Hospital'] = unique_location.apply(lambda row: get_places_data(row['Latitude'], row['Longitude'], radius, 'hospital'), axis=1)
    unique_location['Distance_TokoObat'] = unique_location.apply(lambda row: get_places_data(row['Latitude'], row['Longitude'], radius, 'drugstore'), axis=1)
    
    unique_location.to_csv('unique_location_with_coordinates.csv', index=False)
    return unique_location
