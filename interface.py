import datetime as datetime
from utilities import *
from Dataset import Dataset

dataset = Dataset()

date = '20211127'
data = dataset.read(date, selection='main', start_time='10:30:30', end_time='10:35:00')
print(data.shape)
print(data.head())

