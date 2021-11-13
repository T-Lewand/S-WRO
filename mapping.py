import pandas as pd
import folium
from utilities import *
from Rover import Rover
from Dataset import Dataset
import math

"""
Skrypt tworzy mapę w html z wykorzystaniem biblioteki folium
"""

wroclaw_B = 51 + 6/60 + 36/60/60
wroclaw_L = 17 + 1/60 + 57/60/60
rover1 = Rover('1')
rover2 = Rover('2')

dataset = Dataset()

rover1_path = rover1.path('20211006')
rover2_path = rover2.path('20211006')

map = folium.Map(location=[wroclaw_B, wroclaw_L], zoom_start=14)
feature_group1 = folium.FeatureGroup("Rover 1")
feature_group2 = folium.FeatureGroup("Rover 2")

path_rover1 = folium.vector_layers.PolyLine(rover1_path, color='red').add_to(feature_group1)
path_rover2 = folium.vector_layers.PolyLine(rover2_path, color='green').add_to(feature_group2)
feature_group1.add_to(map)
feature_group2.add_to(map)

folium.LayerControl().add_to(map)
map.save('map.html')