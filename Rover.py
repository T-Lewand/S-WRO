from utilities import *

class Rover():
    def __init__(self, name):
        """
        Tworzy obiekt Rover
        :param name: numer rowera
        """
        self.rover = name
        self.data_dir = 'Data\\Clean\\'
        data_files = list_files(self.data_dir)
        self.rover_files = []
        for i in data_files:
            if '_{}'.format(name) in i:
                self.rover_files.append(i)

    def read_data(self, date):
        """
        Czyta dane w folderze Data\Clean
        :param date: Data dla której podczytuje dane w formie: YYYYMMDD
        :return: DataFrame
        """
        try:
            data = pd.read_csv('{}{}_{}.txt'.format(self.data_dir, date, self.rover), sep=';')
        except:
            print("Brak danych dla podanej daty")
            exit()

        return data

    def path(self, date):
        """
        Zwraca listę par współrzędnych punktów, dla których zebrano dane.
        :param date: data danych
        :return: lista par współrzędnych
        """
        data = self.read_data(date)
        path = zip(data['B'], data['L'])

        return path



