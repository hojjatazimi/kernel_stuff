def give_channels():

    import pandas as pd
    import numpy as np
    from sklearn import preprocessing

    csv = pd.read_csv('./channel_sensitivity_Schaefer100_7networks.csv')
    
    with open('./channels_temporal_lobe.txt') as f:
        lines = f.readlines()
    good_channels = [line[:-1] for line in lines]    
    
    
    # good_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23 ,24, 25, 26, 27, 28, 29, 30, 32, 33, 38, 39, 51, 52, 53, 54, 55, 56, 57, 58, 67, 68, 6, 70, 71, 91, 92, 93]
    # good_channels = csv.columns[good_indexes].values
    csv_values = csv.values [:, 1:]
    csv_values_norm = preprocessing.normalize(csv_values, axis = 1)
    csv_values_norm_mean = np.mean(csv_values_norm, axis = 1)
    csv_values_norm_mean_tile = np.tile(csv_values_norm_mean, (100, 1)).T
    
    dif = csv_values_norm - csv_values_norm_mean_tile
    dif_pos = dif.copy()
    dif_pos[dif_pos < 0] = 0
    
    new_csv = pd.DataFrame(np.hstack((csv.values[:, 0].reshape(2206, 1), dif_pos)), columns=csv.columns)
     
    ls_ls = [new_csv[new_csv[ch] > 0]['Unnamed: 0'].values for ch in good_channels]
    ls = np.unique([item for sublist in ls_ls for item in sublist])
    out = []
    for name in ls:
        name = name[-3:] + '_' + name[:-3]
        name = name.replace('s', 'S')
        out.append(name.replace('m', 'D'))

    return np.array(out)
