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

def show_map(location):
    # 建立地圖
    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
        <meta charset="utf-8">
        <title>地圖</title>
        <style>
          /* 設定地圖大小 */
          #map {{
            height: 100%;
          }}
          /* 設定資訊視窗 */
          .info-window {{
            width: 300px;
          }}
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>
        <script>
          function initMap() {{
            var location = {{lat: {location['lat']}, lng: {location['lng']}}};
            var map = new google.maps.Map(document.getElementById('map'), {{
              zoom: 15,
              center: location
            }});
            var marker = new google.maps.Marker({{
              position: location,
              map: map
            }});
            var content = '<div class="info-window"><h2>{location['name']}</h2><p>{location['formatted_address']}</p><p>評分：{location['rating']}</p></div>';
            var infoWindow = new google.maps.InfoWindow({{
              content: content
            }});
            marker.addListener('click', function() {{
              infoWindow.open(map, marker);
            }});
          }}
        </script>
      </head>
      <body onload="initMap()">
        <div id="map"></div>
      </body>
    </html>
    """
    # 在瀏覽器中開啟地圖
    with open('map.html', 'w') as f:
        f.write(html)
    webbrowser.open_new_tab('map.html')