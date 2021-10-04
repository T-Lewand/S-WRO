from utilities import *
from Dataset import Dataset
raw_dir = 'Data\\Raw\\'
raw_files = list_files(raw_dir)


dataset = Dataset()
#print(dataset.read_data('20210912'))
dataset.visualize(20210912, 'temp')

