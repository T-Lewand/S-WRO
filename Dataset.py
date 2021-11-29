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
        self.dates = list(set([entry[0:8] for entry in self.raw_files]))
        self.dates.sort()
        self.clean_files = list_files(self.clean_dir)
        with open('Data\\header.txt', 'r') as file:
            self.header = file.read().split(', ')

    def get_dates(self):
        """
        Converts list of dates to dictionary in format {DD.MM.YYYY: YYYYMMDD}
        :return: dictionary of dates
        """
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

    def clean_raw(self, date: int = None, save: bool = True):
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

                raw_data.iloc[entry_index] = raw_data.iloc[entry_index].shift(axis=1)

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
            if save:
                day_log.to_csv('{}{}.txt'.format(self.clean_dir, j), sep=';', index=False)

    def read_all(self, date):
        """
        Reads clean data file
        :param date: date of data to read
        :return:
        """
        data = pd.read_csv('{}\\{}.txt'.format(self.clean_dir, date), sep=';')
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
            end_time = data.iloc[-1, 1][0:-7]
        else:
            end_time = "{}-{}-{} {}".format(date[0:4], date[4:6], date[6:], end_time)

        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=delta)

        nans = pd.isna(data['index'])
        second_index = data.index[~nans]

        if selection == 'main':
            data = data.iloc[second_index]
            for i in range(data.shape[0]):
                data.iloc[i, 1] = datetime.strptime(data.iloc[i, 1], '%Y-%m-%d %H:%M:%S')
        elif selection == 'accel':
            data = data.loc[:, ['index', 'Time', 'aX', 'aY', 'aZ']]
            for i in range(data.shape[0]):
                try:
                    data.iloc[i, 1] = datetime.strptime(data.iloc[i, 1], '%Y-%m-%d %H:%M:%S')
                except:
                    data.iloc[i, 1] = datetime.strptime(data.iloc[i, 1], '%Y-%m-%d %H:%M:%S.%f')

        data = data[(data["Time"] > start_time) & (data["Time"] < end_time)]
        return data

    def visualize(self, date,  parameters=None, start=0, stop=None):  # In progress
        all = self.read(date=date)
        if parameters is None:
            parameters = self.header[4:]
        if start == 0:
            start = all.iloc[0, 1]

        if stop is None:
            stop = all.iloc[-1, 1]

        print(stop)

        all = all[(all["Time"] > start)]
        all = all[(all["Time"] < stop)]
        exit()
        fig, ax = plt.subplots(nrows=len(parameters), ncols=1)

        for i in range(len(parameters)):
            print(parameters[i])
            param = all.loc[:, ["Time", parameters[i]]]

            for j in range(param.shape[0]):
                param.iloc[j, 0] = param.iloc[j, 0].time()
                param.iloc[j, 0] = param.iloc[j, 0].strftime("%H:%M:%S")

            plt.sca(ax[i])
            sns.lineplot(data=param, x='Time', y=parameters[i])

        plt.show()
