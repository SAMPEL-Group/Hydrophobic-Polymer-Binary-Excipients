#%% Header
# Bootstrap biases to get average PMF and error estimate

#%% Import Stuff
import numpy as np
import pandas as pd
from numpy import savetxt
import wham

#%% Define Some Variables
k="NNNNKKKK"
z= NNNNRRRR
header = " FIELDS time rg logweights"
T = 300
kBT=T*8.314462618*0.001
n_traj = 12
n_frames = 20 * 1000 * n_traj + n_traj*1
n_bs = NNNNBBBB
path = "/scratch.global/zajac028/bootstrapping/{}/run{}".format(k, z)

#%% Define Some Functions

def open_file(i):
    data = pd.read_table("{}/all-bias/all_bias.{}.dat".format(path, i), skiprows=1, sep=" ", names=['time', 'rg', 'bias'])
    data = data.set_index(np.arange(0, len(data.rg), 1))
    return data

def draw_bootstrap(data):
    subsample_bias =  data.sample(n=data.time.count()-1, replace=True)
    return subsample_bias

initialize_data = open_file(0) #Get first set of data; will be appended to in a sec

for i in range(1, n_traj):
    current_data = open_file(i)
    current_bias = current_data.bias
    initialize_data = pd.concat((initialize_data, current_bias), axis=1)

def do_bootstrapped_wham(data, ndraws):
    for j in range(ndraws):
        subsample_bias = draw_bootstrap(initialize_data) #Get a bootstrapped sample!
        
        time_values = subsample_bias.pop('time') #Pop time, will add back later
        rg_values = subsample_bias.pop('rg') #Pop Rg, will add back later
        
        subsample_bias = np.asarray(subsample_bias)
        time_values = np.asarray(time_values)
        rg_values = np.asarray(rg_values)
        
        w=wham.wham(subsample_bias,T=kBT)
        weights = w["logW"]
        
        output = np.vstack((time_values, rg_values, weights)).T        
        savetxt('temp_bias_{}.dat'.format(j), output, delimiter=' ', header=header, comments='#!')

do_bootstrapped_wham(initialize_data, n_bs)
