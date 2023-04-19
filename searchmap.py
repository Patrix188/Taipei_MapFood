import webbrowser
import googlemaps
from googlemaps.places import places_nearby, place

# 設定 Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

def search_places(area):
    # 使用 Google Maps Places API 搜尋指定區域的店家
    response = places_nearby(gmaps, location=area, radius=500, type='restaurant')
    results = response['results']
    # 取得每個店家的詳細資訊
    for result in results:
        place_details = place(gmaps, result['place_id'], fields=['name', 'rating', 'formatted_address', 'reviews'])
        result.update(place_details)
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