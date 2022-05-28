import numpy as np
import matplotlib.pyplot as plt
from mne.io.snirf import read_raw_snirf
import mne
from get_events_from_snirf import get_events_from_snirf
import itertools

path_1 = '../data_hojjat/2021_08-Finger_Tapping-Hb.snirf'

snirf = read_raw_snirf(path_1);

# mne.viz.plot_montage(snirf.get_montage(), kind='3d');
# plt.show();

# %matplotlib inline
# %matplotlib widget

tstart = snirf.annotations.onset[(snirf.annotations.description) == 'StartBlock']
snirf.plot(n_channels=10, duration=120, show_scrollbars=True, scalings='auto', clipping=None, start=tstart);
