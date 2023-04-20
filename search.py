import tkinter as tk
import googlemaps
import webbrowser

API_KEY = 'AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY'
gmaps = googlemaps.Client(key=API_KEY)

def search_places(area, rating=None):
    query = f"餐廳 {area} 台北市"
    places = gmaps.places(query=query, language='zh-TW', type='restaurant')
    results = []
    for place in places['results']:
        if rating is not None and place.get('rating', None) is not None:
            if place['rating'] < rating:
                continue
        result = {
            'name': place['name'],
            'address': place['formatted_address'],
            'rating': place.get('rating', None),
            'location': place['geometry']['location'],
            'place_id': place['place_id'] # 新增place_id欄位
        }
        results.append(result)
    results.sort(key=lambda x: x['rating'], reverse=True)
    return results