import pandas as pd
import folium
from utilities import *
from Rover import Rover
from Dataset import Dataset
import math
raw_dir = 'Data\\Raw\\'
raw_files = list_files(raw_dir)

wroclaw_B = 51 + 6/60 + 36/60/60
wroclaw_L = 17 + 1/60 + 57/60/60
rover1 = Rover('1')
rover2 = Rover('2')

dataset = Dataset()
dataset.visualize('20211006', '1', 'pmy1')
rover1_data = dataset.read_data('20211006', '1')
#rover2 = dataset.read_data('20211006', '2')



