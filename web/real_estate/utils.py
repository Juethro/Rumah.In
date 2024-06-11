import folium

def make_markers_and_add_to_map(map, house):
    folium.Marker(
            location = [house.latitude, house.longitude],
            popup = house.description,
            tooltip = house.title,
            icon = folium.Icon(icon='fa-home', prefix='fa')
        ).add_to(map)