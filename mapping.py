import pandas as pd
import folium
from utilities import *
from Rover import Rover
from Dataset import Dataset
import math

wroclaw_B = 51 + 6/60 + 36/60/60
wroclaw_L = 17 + 1/60 + 57/60/60
rover1 = Rover('1')
rover2 = Rover('2')

dataset = Dataset()
#dataset.visualize('20211006_1', 'coord')
#rover1 = dataset.read_data('20211006', '1')
#rover2 = dataset.read_data('20211006', '2')

rover1_path = rover1.path('20211006')
rover2_path = rover2.path('20211006')

map = folium.Map(location=[wroclaw_B, wroclaw_L], zoom_start=14)
feature_group1 = folium.FeatureGroup("Rover 1")
feature_group2 = folium.FeatureGroup("Rover 2")

path_rover1 = folium.vector_layers.PolyLine(rover1_path, color='red').add_to(feature_group1)
path_rover2 = folium.vector_layers.PolyLine(rover2_path, color='green').add_to(feature_group2)
feature_group1.add_to(map)
feature_group2.add_to(map)


def hex_coord(center, radius):
    x0, y0 = center[1], center[0]
    radius = radius/6378137.0
    y1 = y0 + radius
    x1 = x0

    y2 = y0 + radius * math.cos(60 * math.pi / 180)
    x2 = x0 + radius * math.sin(60 * math.pi / 180)

    y3 = y0 + radius * math.cos(120 * math.pi / 180)
    x3 = x2

    y4 = y0 - radius
    x4 = x0
    y5 = y0 + radius * math.cos(240 * math.pi / 180)
    x5 = x0 + radius * math.sin(240 * math.pi / 180)

    y6 = y0 + radius * math.cos(300 * math.pi / 180)
    x6 = x5

    return [[y1, x1], [y2, x2], [y3, x3], [y4, x4], [y5, x5], [y6, x6]]

hex_wroc = hex_coord([wroclaw_B, wroclaw_L], 500)
feature_group3 = folium.FeatureGroup('Hex')

hex = folium.vector_layers.Polygon(hex_wroc, color='red').add_to(feature_group3)
feature_group3.add_to(map)
folium.LayerControl().add_to(map)
map.save('map.html')