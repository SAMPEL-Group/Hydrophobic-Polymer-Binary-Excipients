#%% Header
# Bootstrap biases to get average PMF and error estimate

#%% Import Stuff
import numpy as np
import pandas as pd
from numpy import savetxt
import wham
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
from scipy.stats import wasserstein_distance
from scipy.special import softmax, rel_entr
from scipy.stats import kstest
import matplotlib.pylab as pl

#%% Define Some Variables
header = " FIELDS time rg logweights"
T = 300
kBT=T*8.314462618*0.001
n_traj = 12
n_frames = 20 * 1000 * n_traj + n_traj*1
n_bs = NNNNBBBB
font = "Helvetica"
hfont = {'fontname':'Helvetica'}
big = 22
medium = 18
small = 14
xsmall = 10

#%% Define Some Functions

def open_file(i):
    data = pd.read_table("temp_fes_rg_{}.dat".format(i), skiprows=6, sep=" ", names=['rg', 'ffrg', 'dffrg'])
    data = data.set_index(np.arange(0, len(data.rg), 1))
    return data

initialize_data = open_file(0) #Get first set of data; will be appended to in a sec
initialize_data = initialize_data.drop('dffrg', axis=1)

for i in range(1, n_bs):
    current_data = open_file(i)
    current_ffrg = current_data.ffrg
    initialize_data = pd.concat((initialize_data, current_ffrg), axis=1)

rg_values = initialize_data.pop('rg')
ffrg_mean = initialize_data.mean(axis=1)/kBT
ffrg_std = initialize_data.std(axis=1)/kBT

fig, ax = plt.subplots()
ax.plot(rg_values, ffrg_mean, color='darkcyan', alpha=0.8, ls='-', lw=3)
plt.fill_between(rg_values, (ffrg_mean + ffrg_std), (ffrg_mean - ffrg_std), alpha=0.3, color='darkcyan')
plt.autoscale()
ax.xaxis.set_major_locator(ticker.AutoLocator())
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_major_locator(ticker.AutoLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
plt.xlim(0.35, 0.9)
# plt.ylim(0, 4)
plt.xticks(fontsize=small)
plt.yticks(fontsize=small)
plt.title("Hydrophobic Polymer PMF ({}Arg)".format(k), **hfont, fontsize=medium)
plt.xlabel("rg [nm]", **hfont, fontsize=big)
plt.ylabel("w(rg) [kT]", **hfont, fontsize=big)
# ax.legend(prop=font_manager.FontProperties(family=font), loc="best")
plt.tight_layout()
plt.savefig('PMF-from-bootstrap.svg', transparent=True)
plt.show()
