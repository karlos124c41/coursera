# -*- coding: utf-8 -*-
"""
SpaceX Launch Site Analysis using Folium
Created on Mon Feb 10 12:30:37 2025
"""

import folium
import wget
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians

# Download and read the SpaceX launch data
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df = pd.read_csv(spacex_csv_file)

# Select relevant sub-columns
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

# Initialize the map centered at NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create markers for NASA Johnson Space Center
circle = folium.Circle(
    nasa_coordinate, 
    radius=1000, 
    color='#d35400', 
    fill=True
).add_child(folium.Popup('NASA Johnson Space Center'))

marker = folium.map.Marker(
    nasa_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
    )
)

site_map.add_child(circle)
site_map.add_child(marker)

# Task 2: Mark success/failed launches
# Create a MarkerCluster object
marker_cluster = MarkerCluster()

# Create function to assign marker colors based on launch outcome
def assign_marker_color(launch_outcome):
    return 'green' if launch_outcome == 1 else 'red'

# Add marker_color column to the dataframe
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

# Add markers for each launch site
for index, record in spacex_df.iterrows():
    # Create a marker for each launch record
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color']),
        popup=f"Launch Site: {record['Launch Site']}<br>Success: {'Yes' if record['class'] == 1 else 'No'}"
    )
    marker_cluster.add_child(marker)

# Add marker cluster to map
site_map.add_child(marker_cluster)

# Task 3: Add MousePosition for coordinate tracking
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
site_map.add_child(mouse_position)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on Earth"""
    R = 6373.0  # approximate radius of earth in km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# Example for Kennedy Space Center (LC-39A)
launch_site_lat = 28.5728722
launch_site_lon = -80.6489808

# Closest coastline point (example coordinates)
coastline_lat = 28.56367
coastline_lon = -80.57163

# Calculate distance to coastline
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Add marker for coastline point with distance
coastline_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html=f'<div style="font-size: 12; color:#d35400;"><b>{distance_coastline:.2f} KM</b></div>'
    )
)
site_map.add_child(coastline_marker)

# Draw line between launch site and coastline
coordinates = [
    [launch_site_lat, launch_site_lon],
    [coastline_lat, coastline_lon]
]
lines = folium.PolyLine(locations=coordinates, weight=1, color='red')
site_map.add_child(lines)

# Example for adding closest city (Cape Canaveral)
city_lat = 28.4740556
city_lon = -80.5772778
city_distance = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)

# Add city marker with distance
city_marker = folium.Marker(
    [city_lat, city_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html=f'<div style="font-size: 12; color:#0000ff;"><b>Cape Canaveral<br>{city_distance:.2f} KM</b></div>'
    )
)
site_map.add_child(city_marker)

# Draw line between launch site and city
city_coordinates = [
    [launch_site_lat, launch_site_lon],
    [city_lat, city_lon]
]
city_line = folium.PolyLine(locations=city_coordinates, weight=1, color='blue')
site_map.add_child(city_line)

# Save the map
site_map.save('spacex_launch_site_analysis.html')