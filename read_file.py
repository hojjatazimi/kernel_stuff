import numpy as np
import matplotlib.pyplot as plt
from mne.io.snirf import read_raw_snirf

# %% Reading the file
path_to_snirf = "./data_hojjat/test_001_S001_f6cb9a6_5.snirf"
snirf = read_raw_snirf(path_to_snirf)

# %% Obtaining general information
# you can query snirf.info for measurement data/time
# information about the channels (their names and locations) can also be accessed in snirf.info as follows:
channel_names = [x['ch_name'] for x in snirf.info['chs']]
is_hbo = np.array([1 if channel_name.endswith(
    'HbO') else 0 for channel_name in channel_names], dtype=bool)
channel_locations_3d = [x['loc'][:3] for x in snirf.info['chs']]

# %% Obtaining NIRS data
data = snirf.get_data()


# %% Plotting
_, ax = plt.subplots(ncols=2, figsize=(10, 5))
ax[0].pcolor(snirf.times, np.arange(np.sum(is_hbo)),
             data[is_hbo, :], shading='nearest')
ax[0].set_title('HbO')
ax[0].set_xlabel('Time [s]')
ax[0].set_ylabel('Channel number')
ax[1].pcolor(snirf.times, np.arange(np.sum(~is_hbo)),
             data[~is_hbo, :], shading='nearest')
ax[1].set_title('HbR')
ax[1].set_xlabel('Time [s]')
plt.show()
