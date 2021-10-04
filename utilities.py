import os
import pandas as pd
from matplotlib import pyplot as plt


def list_files(data_directory: str, form: str = None):
    """
    Zwraca nazwy plików znajdujących się w danym folderze data_directory jako listę stringów
    data_directory: scieżka do folderu z danymi
    form: format szukanych plików, jeśli None zwraca nazwy wszystkich plików w folderze
    """
    if form is None:
        files = os.listdir(data_directory)
    else:
        files = []
        all_files = os.listdir(data_directory)
        for i in all_files:
            if '.{}.'.format(form) in i:
                pass
            else:
                if '.{}'.format(form) in i:
                    files.append(i)

    return files