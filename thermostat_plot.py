import numpy as np
import pandas as pd

DATA_DIR = 'data'
DATA_FILENAME = 'CampoHome_20190529174959.csv'
DATA_FILE_PATH = DATA_DIR + '/' + DATA_FILENAME

data = pd.read_csv(DATA_FILE_PATH, quotechar='"', skipinitialspace=True)
