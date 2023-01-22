import folium

# Create a map centered at (37.7749, -122.4194)
map = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Mark a point on the map at (37.7749, -122.4194)
folium.Marker([37.7749, -122.4194]).add_to(map)

# Create a route between two points
folium.PolyLine([[37.7749, -122.4194], [37.79, -122.4194]], color="red", weight=2.5, opacity=1).add_to(map)

# Show the map
map.show_in_browser()