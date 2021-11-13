from utilities import *

class Dataset:
    def __init__(self):
        self.raw_dir = 'Data\\Raw\\'
        self.clean_dir = 'Data\\Clean\\'
        self.raw_files = list_files(self.raw_dir)
        self.clean_files = list_files(self.clean_dir)
        with open('Data\\header.txt', 'r') as file:
            self.header = file.read().split(', ')

    def get_dates(self, as_dict=False):
        dates = [entry.split('.')[0] for entry in self.clean_files]
        dates = [entry.split('_')[0] for entry in dates]
        dates = set(dates)
        dates = list(dates)

        if as_dict:

            string = []
            for i in dates:
                string.append('{}.{}.{}'.format(i[-2::], i[4:6], i[0:4]))

            dates_dict = []
            for i in range(len(dates)):
                dates_dict.append(dict(label=string[i], value=dates[i]))

            return dates_dict

        else:
            return dates

    def clean_raw(self, date: int = None, save: bool = True):
        """
        Czyści surowe dane i zapisuje je w ładnym DataFrame z nagłówkami w folderze Data\Clean
        :param date: Data, której plik chcemy wyczyścić
        :param save: Jeśli True zapisuje DataFrame. False po to żeby nie zaśmiecać folderu Data\Clean
        :return: Przeformatowane surowe dane w DataFrame
        """
        if date is None:
            file = self.raw_files
        else:
            try:
                file = ['{}.txt'.format(date)]
            except:
                print("Brak danych dla podanej daty")
                exit()

        for i in self.raw_files:
            raw_data = pd.read_csv('{}{}'.format(self.raw_dir, i),
                                   names=self.header, sep='\t')
            raw_data['date'] = raw_data['date'][0][2::]  # Sprząta '>>' przy datach
            if save:
                raw_data.to_csv('{}{}'.format(self.clean_dir, i), sep=';', index=False)

        return raw_data

    def read_data(self, date, rover):
        """
        Czyta dane w folderze Data\Clean
        :param date: Data dla której podczytuje dane w formie: YYYYMMDD
        :return: DataFrame
        """
        self.clean_files = list_files(self.clean_dir, form='.txt')
        try:
            clean_data = pd.read_csv('{}{}_{}.txt'.format(self.clean_dir, date, rover), sep=';')
        except:
            print('{}{}_{}.txt'.format(self.clean_dir, date, rover))
            print("Brak danych dla podanej daty")
            exit()

        return clean_data

    def visualize(self, date, rover,  parameter: str):  # In progress
        """
        Funkcja w trakcie tworzenia
        :param date: data danych dla których tworzony będzie wykres
        :param rover: numer rowera
        :param parameter: parametr, który ma być na wykresie
        :return:
        """
        data = self.read_data(date, rover)
        fig, ax = plt.subplots()
        if parameter == 'coord':
            latitude = data['B']
            longitude = data['L']
            print(latitude), print(longitude)
            plot = ax.scatter(longitude, latitude)
        else:
            plot = ax.plot(data['time'], data[parameter])

        fig = plt.xticks(rotation=60)
        plt.show()