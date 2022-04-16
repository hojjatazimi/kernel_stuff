def give_channels()

import pandas as pd
import numpy as np

csv = pd.read_csv('./channel_sensitivity_Schaefer100_7networks.csv')

good_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23 ,24, 25, 26, 27, 28, 29, 30, 32, 33, 38, 39, 51, 52, 53, 54, 55, 56, 57, 58, 67, 68, 6, 70, 71, 91, 92, 93]
good_channels = csv.columns[good_indexes].values

ls_ls = [csv[csv[ch] > 0]['Unnamed: 0'].values for ch in good_channels]
ls = np.unique([item for sublist in ls_ls for item in sublist])

return ls