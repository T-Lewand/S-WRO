import datetime as datetime

start = datetime.datetime.now()
from utilities import *
from Dataset import Dataset

import_time = datetime.datetime.now()
print('Import time', import_time - start)
raw_dir = 'Data\\Raw\\'
raw_files = list_files(raw_dir)

wroclaw_B = 51 + 6/60 + 36/60/60
wroclaw_L = 17 + 1/60 + 57/60/60
dataset = Dataset()
print(dataset.dates)
print(dataset.header)
date = '2021-11-27'
dataset.visualize(date='20211127', stop=datetime.datetime.strptime('{} 11:30:00'.format(date), '%Y-%m-%d% %H:%M:%S'))

stop = datetime.datetime.now()
print("Exec time=", stop - start)