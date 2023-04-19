import tkinter as tk
from tkinter import ttk
import googlemaps
import webbrowser
from datetime import datetime

API_KEY = 'AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY'
gmaps = googlemaps.Client(key=API_KEY)

def show_results():
    global start, page, total_pages

    text.delete('1.0', tk.END)
    for i in range(start, start + display_count):
        if i >= len(results):
            break
        result = results[i]
        text.insert(tk.END, f"{result['name']}\n")
        text.insert(tk.END, f"{result['address']}\n")
        text.insert(tk.END, f"評分: {result['rating']}\n\n")

        # 顯示地圖及大頭針
        if 'geometry' in result:
            location = result['geometry']['location']
            lat, lng = location['lat'], location['lng']
            html = f"""
                <!DOCTYPE html>
                <html>
                  <head>
                    <title>Map</title>
                    <meta name="viewport" content="initial-scale=1.0">
                    <meta charset="utf-8">
                    <style>
                      #map {{
                        height: 400px;
                        width: 100%;
                      }}
                    </style>
                    <script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}"></script>
                    <script>
                      function initMap() {{
                        var location = {{lat: {lat}, lng: {lng}}};
                        var map = new google.maps.Map(document.getElementById('map'), {{
                          zoom: 15,
                          center: location
                        }});
                        var marker = new google.maps.Marker({{
                          position: location,
                          map: map
                        }});
                      }}
                    </script>
                  </head>
                  <body>
                    <div id="map"></div>
                    <script>initMap();</script>
                  </body>
                </html>
            """
            filename = 'map.html'
            with open(filename, 'w') as f:
                f.write(html)
            webbrowser.open_new_tab(filename)