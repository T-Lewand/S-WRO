from utilities import *

class Dataset:
    def __init__(self):
        self.raw_dir = 'Data\\Raw\\'
        self.clean_dir = 'Data\\Clean\\'
        self.raw_files = list_files(self.raw_dir)
        self.clean_files = list_files(self.clean_dir)
        with open('Data\\header.txt', 'r') as file:
            self.header = file.read().split(', ')

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
            raw_data = pd.read_csv('{}{}'.format(self.raw_dir, i), sep='\t', header=None)
            raw_data.columns = self.header[0:11]  # Tu będzie zmiana jak dojdą dane z akcelerometra i GPS
            raw_data['data'] = raw_data['data'][0][2::]  # Sprząta '>>' przy datach
            if save:
                raw_data.to_csv('{}{}'.format(self.clean_dir, i), sep=';', index=False)

        return raw_data

    def read_data(self, date):
        """
        Czyta dane w folderze Data\Clean
        :param date: Data dla której podczytuje dane w formie: YYYYMMDD
        :return: DataFrame
        """
        self.clean_files = list_files(self.raw_dir, form='.txt')
        try:
            clean_data = pd.read_csv('{}{}.txt'.format(self.clean_dir, date), sep=';')
        except:
            print("Brak danych dla podanej daty")
            exit()

        return clean_data

    def visualize(self, date: int, parameter: str):  # In progress
        data = self.read_data(date)
        fig, ax = plt.subplots()

        plot = ax.plot(data['godz'], data[parameter])

        plt.show()