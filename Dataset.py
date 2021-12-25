import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import seaborn as sns
from utilities import *


class Dataset:
    def __init__(self):
        self.raw_dir = 'Data\\Raw\\'
        self.clean_dir = 'Data\\Clean\\'
        self.raw_files = list_files(self.raw_dir)
        self.raw_files.sort()
        self.clean_files = list_files(self.clean_dir)
        self.clean_files.sort()
        with open('Data\\header.txt', 'r') as file:
            self.header = file.read().split(', ')

    def get_dates(self):
        """
        Converts list of dates to dictionary in format {DD.MM.YYYY: YYYYMMDD}
        :return: dictionary of dates
        """
        self.dates = list(set([entry[0:8] for entry in self.clean_files]))
        self.dates.sort()
        string = []
        for i in self.dates:
            string.append('{}.{}.{}'.format(i[-2::], i[4:6], i[0:4]))

        dates_dict = []
        for i in range(len(self.dates)):
            dates_dict.append(dict(label=string[i], value=self.dates[i]))

        return dates_dict

    def read_raw(self, raw_file):
        """
        Reads raw files into DataFrame.
        :param raw_file: directory of single file
        :return: dataframe of uncleaned data
        """
        raw_data = pd.read_csv('{}{}'.format(self.raw_dir, raw_file),
                               names=self.header, sep='\t', true_values=['>']).reset_index()
        return raw_data

    def pm_correction(self, raw_pm, humidity, pm_parameter: str):
        """
        Corrects pm values due to humidity
        :param raw_pm: Series of raw Pm values
        :param humidity: Series of humidity
        :param pm_parameter: Name of Pm for correction. 'Pm2.5' and 'Pm10' supported
        :return: Series of corrected Pm 10
        """
        if '2.5' in pm_parameter:
            A, B, C = 1.00123, 1.96141, 1
        elif '10' in pm_parameter:
            A, B, C = 1.15866, 3.16930, 0.7

        factor = C + A * (humidity.values/100)**B
        pm_corrected = raw_pm/factor
        return pd.Series(pm_corrected)

    def clean_raw(self, date: str = None, save: bool = True):
        """
        Czyści surowe dane i zapisuje je w ładnym DataFrame z nagłówkami w folderze Data\Clean
        :param date: Data, której plik chcemy wyczyścić
        :param save: Jeśli True zapisuje DataFrame. False po to żeby nie zaśmiecać folderu Data\Clean
        :return: Przeformatowane surowe dane w DataFrame
        """
        if date is None:
            file = self.dates
        else:
            try:
                file = ['{}'.format(date)]
            except:
                print("Brak danych dla podanej daty")
                exit()

        for j in file:
            day_log = pd.DataFrame(np.zeros((1, 13)), columns=self.header).reset_index()
            for k in self.raw_files:
                if j not in k:
                    continue
                day = "{}-{}-{}".format(k[0:4], k[4:6], k[6:8])
                raw_data = self.read_raw(k)

                nans = pd.isna(raw_data['index'])
                second_index = raw_data.index[~nans]
                entry_index = raw_data.index[nans]

                #raw_data.iloc[entry_index] = raw_data.iloc[entry_index].shift(axis=1)  # use only with old version of logs

                for i in second_index:
                    raw_data.iloc[i, 1] = datetime.strptime("{} {}".format(day, raw_data.iloc[i, 1]),
                                                                     '%Y-%m-%d %H:%M:%S')

                for i in range(raw_data.shape[0]):
                    if pd.isna(raw_data.iloc[i, 1]):
                        if raw_data.iloc[i-1, 0] is True:
                            raw_data.iloc[i, 1] = raw_data.iloc[i - 1, 1]
                        else:
                            raw_data.iloc[i, 1] = raw_data.iloc[i - 1, 1] + timedelta(milliseconds=40)

                day_log = pd.concat([day_log, raw_data], axis=0)


            day_log = day_log.iloc[1:]
            day_log.reset_index(inplace=True)

            # recalculating Pm 2.5 and Pm 10
            nans = pd.isna(day_log['index'])
            second_index2 = day_log.index[~nans]

            day_log.loc[second_index2, 'Pm2.5'] = self.pm_correction(day_log.loc[second_index2, 'Pm2.5'],
                                                                       day_log.loc[second_index2, 'RH'], 'Pm2.5')
            day_log.loc[second_index2, 'Pm10'] = self.pm_correction(day_log.loc[second_index2, 'Pm10'],
                                                                      day_log.loc[second_index2, 'RH'], 'Pm10')
            day_log.loc[pd.isna(day_log['index']), 'index'] = False
            #accels = day_log.loc[:, ['index', 'Time', 'Latitude', 'Longitude', 'aX', 'aY', 'aZ']]
            d_accel = self.displacement(day_log)

            if save:
                day_log.to_csv('{}{}.txt'.format(self.clean_dir, j), sep=';', index=False)

    def displacement(self, data):
        """
        Calculates relative changes in accelerations and appends new columns to existing DataFrame with data
        :param data: DataFrame to process
        :return: None
        """

        for i in range(data.shape[0]-1):
            data.loc[i + 1, 'd_aX'] = data.loc[i + 1, 'aX'] - data.loc[i, 'aX']
            data.loc[i + 1, 'd_aY'] = data.loc[i + 1, 'aY'] - data.loc[i, 'aY']
            data.loc[i + 1, 'd_aZ'] = data.loc[i + 1, 'aZ'] - data.loc[i, 'aZ']

        data.loc[0, ['d_aX', 'd_aY', 'd_aZ']] = 0

    def acceleration_positioning(self, date, save=True):
        """
        Calculates position for accelerometer entries in log
        :param date: date of data to process
        :param save: if True saves file
        :return: None
        """
        data_main = self.read(date, selection='main')
        data_accel = self.read(date, selection='accel')
        main_index = list(data_main.index.values)

        k = 0
        for i in range(data_accel.shape[0]):
            if data_accel.loc[i, 'index']:
                if k == len(main_index) - 1:
                    break

                lat_0 = data_main.loc[main_index[k], 'Latitude']
                lon_0 = data_main.loc[main_index[k], 'Longitude']

                lat_next = data_main.loc[main_index[k + 1], 'Latitude']
                lon_next = data_main.loc[main_index[k + 1], 'Longitude']

                interval = main_index[k + 1] - main_index[k]
                lat_step = (lat_next - lat_0) / interval
                lon_step = (lon_next - lon_0) / interval
                k += 1
            else:
                data_accel.loc[i, 'Latitude'] = data_accel.loc[i - 1, 'Latitude'] + lat_step
                data_accel.loc[i, 'Longitude'] = data_accel.loc[i - 1, 'Longitude'] + lon_step

        if save:
            data_accel.to_csv('{}{}_accel.txt'.format(self.clean_dir, date), sep=';', index=False)

    def read_all(self, date):
        """
        Reads clean data file
        :param date: date of data to read
        :return:
        """
        data = pd.read_csv('{}\\{}.txt'.format(self.clean_dir, date), sep=';').drop(columns=['level_0'])
        data['Time'] = pd.to_datetime(data.loc[:, 'Time'], format='%Y-%m-%d %H:%M:%S')
        return data

    def read(self, date, selection='main', start_time=None, end_time=None):
        """
        Reads clean data into dataframe
        :param date: date of data to read
        :param selection: type of data to read. 'main' reads only full entries, 'accel' read only accelerations
        :param start_time: starting time for data selection in format HH:MM:SS
        :param end_time: end time for data selection in format HH:MM:SS
        :return: dataframe
        """

        data = self.read_all(date)
        if start_time is None:
            start_time = data['Time'][0]
        else:
            start_time = "{}-{}-{} {}".format(date[0:4], date[4:6], date[6:], start_time)
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

        delta = 0
        if end_time is None:
            delta = 1
            end_time = data.iloc[-1, 1]

        else:
            end_time = "{}-{}-{} {}".format(date[0:4], date[4:6], date[6:], end_time)
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=delta)

        if selection == 'main':
            data = data[data['index']]

        elif selection == 'accel':
            data = data.loc[:, ['index', 'Time', 'Latitude', 'Longitude', 'aX', 'aY', 'aZ', 'd_aX', 'd_aY', 'd_aZ']]

        data = data[(data["Time"] >= start_time) & (data["Time"] <= end_time)]
        return data

    def outliner(self, data, scale):
        """
        Removes outline values
        :param data: Series
        :param scale: scale to increase tresholds
        :return: Series
        """
        median = data.quantile(.5)
        q1 = data.quantile(.25)
        q3 = data.quantile(.75)
        iqr = q3 - q1
        low_treshold = median - scale*iqr
        high_treshold = median + scale*iqr

        data = data[(data > low_treshold) & (data < high_treshold)]

        return data

    def visualize(self, date,  parameters=None, start=0, stop=None):  # In progress
        import matplotlib.ticker as ticker
        all = self.read(date=date)
        if parameters is None:
            parameters = self.header[-3:-2]
        if start == 0:
            start = all.iloc[0, 1]

        if stop is None:
            stop = all.iloc[-1, 1]

        print(stop)

        all = all[(all["Time"] > start)]
        all = all[(all["Time"] < stop)]
        sns.set_style("whitegrid")
        fig, ax = plt.subplots(nrows=len(parameters), ncols=1, figsize=(15, 9))

        for i in range(len(parameters)):
            print(parameters[i])
            param = all.loc[:, ["Time", parameters[i]]]

            for j in range(param.shape[0]):
                param.iloc[j, 0] = param.iloc[j, 0].time()
                param.iloc[j, 0] = param.iloc[j, 0].strftime("%H:%M:%S")

            axes = ax
            plt.sca(axes)
            sns.lineplot(data=param, x='Time', y=parameters[i])
            axes.xaxis.set_major_locator(ticker.AutoLocator())
            axes.locator_params(nbins=30, axis='x')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.subplots_adjust(wspace=0.37, hspace=0.40, top=0.90, bottom=0.2)

        plt.savefig('aX.tiff', dpi=200)
        #plt.show()

    def data_center(self, data=None, date=None):
        """
        Calculates geographical coordinates of center of dataset
        :param data: DataFrame of selected data. If not provided data is read and date is required
        :param date: date of data. Not required if data is provided
        :return: list [lat_center, lon_center]
        """
        if data is None:
            data = self.read(date)

        max_lat = max(data['Latitude'])
        min_lat = min(data['Latitude'])
        max_lon = max(data['Longitude'])
        min_lon = min(data['Longitude'])

        center = [(max_lat+min_lat)/2, (max_lon+min_lon)/2]

        return center
