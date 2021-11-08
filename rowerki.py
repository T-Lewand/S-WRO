# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:18:24 2021

@author: filip

ROWERKI
"""

import pandas as pd

file = "F:\\Projekt_S-WRO\\Data\\Raw\\20210912.txt"
log = pd.read_csv(file,
                  names=('date','DOY','HH:MM:SS',
                         'TEMP.[st.C]','PRESSURE[PA]',
                         'HUMIDITY[%]','PM1','PM2','PM3','PM4','PM5'),
                  sep='\t',
                  skipfooter=2)

log['date'] = log['date'].str.replace('>>', '')
log["date"] = log["date"] + " " + log["HH:MM:SS"]
log['date'] = pd.to_datetime(log['date'])
log = log.set_index(['date'])
log = log.drop('HH:MM:SS', 1)
print(log.dtypes)
