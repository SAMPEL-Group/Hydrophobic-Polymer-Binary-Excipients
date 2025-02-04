# What do we want to do?
# Want to calculate the correlation time of water dipole vectors.
# Need water positions, way to compute dipole vector, and correlation.
# Dipole vector is through oxygen hydrogen center of mass.
import numpy as np
from numpy import savetxt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import MDAnalysis as md
from MDAnalysis.analysis.distances import distance_array, contact_matrix
from tqdm import tqdm
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import asyncio
import nest_asyncio
nest_asyncio.apply()
import time
import copy

n_cores=NNNN
title="TTTT"
clust=AAAA
rcut=BBBB
b=0.1

path="../../waterDynamics/mdrun/prod"
gro="{}/{}-cluster-{}-npt-prod.gro".format(path,title,clust)
traj="{}/{}-cluster-{}-npt-prod.xtc".format(path,title,clust)
u=md.Universe(gro, traj)

print("Starting {}, {} analysis".format(title, rcut))
begin = time.monotonic()

threshold = 1e-5

stop = u.trajectory.n_frames // 2

r2 = np.round(rcut, 2) # inner radius
r3 = np.round((r2 + b),2) # inner buffer radius
r4 = np.round((r3 + b),2) # memory-saving outer buffer radius

step = int(np.ceil(stop / n_cores))

# main function
async def calcC(start):
    u=md.Universe(gro, traj, refresh_offsets=True)
    startTime = u.trajectory[start].time
    polymer = u.select_atoms("resname Pol PolE PolB")
    water = u.select_atoms("same residue as name OW and around {} group polymer".format(r2), polymer=polymer)
    waterRes = water.split('residue') # these selections need to be made new for every frame
    wResids = np.unique(water.resids)
    
    # initialize mu0 list
    # ultimately need a list of all mu0 lists
    mu0List = []
    mu0seg = []
    for i in range(len(waterRes)):
        hw = waterRes[i].select_atoms("name HW*").center_of_mass()
        hw = np.reshape(hw, (1,3))
        ow = waterRes[i].select_atoms("name OW").positions
        mu = hw - ow
        mu0seg.append(mu)
    mu0List.append(mu0seg)
    
    allMus=[]
    runningDropWaters=[]
    for ts in u.trajectory[start:(start+stop)]:
        currFrame = ts.frame
        # every 1 ps, check for water exiting hydration shell
        if (ts.time - startTime) % 1 == 0 and ts.time != startTime:
            
            # First check -- how long have waters resided in buffer region?
            bufferWater = u.select_atoms("same residue as name OW and around {} group polymer and not around {} group polymer".format(r3, r2), polymer=polymer)
            bwResids = np.unique(bufferWater.resids)
            exitWaters = np.intersect1d(wResids, bwResids) # find waters that entered the buffer region
            
            ceWaters=[] # initialize
            feWaters=[] # initialize
            # find waters that did not return to hydration shell after additional 1 ps
            if len(exitWaters) > 0 and ts.time != (startTime + 1.0): 
                ceWaters = np.intersect1d(exitWaters, prev_exitWaters) 
            prev_exitWaters = copy.deepcopy(exitWaters)
            
            # Second check -- how far have water molecules traveled?
            outerWater = u.select_atoms("same residue as name OW and around {} group polymer and not around {} group polymer".format(r4, r3), polymer=polymer)
            owResids = np.unique(outerWater.resids)
            feWaters = np.intersect1d(wResids, owResids) # find waters that left even the buffer region
               
            # if there are waters that must be dropped, drop them!
            if len(ceWaters) > 0 or len(feWaters) > 0: 
                dropWaters = np.asarray(np.hstack((ceWaters, feWaters)), dtype=int)
                runningDropWaters = np.asarray(np.unique(np.hstack((dropWaters, runningDropWaters))), dtype=int) # keep track of all waters removed from pool
                dropResids = ' '.join(str(x) for x in runningDropWaters)
                u.trajectory[start] # point trajectory back to start
                water = u.select_atoms("same residue as name OW and around {} group polymer and not resid {}".format(r2, dropResids), polymer=polymer)
                waterRes = water.split('residue')
                wResids = np.unique(water.resids)
                
                # if we dropped water, we need to append to mu0 list
                mu0seg = []
                for i in range(len(waterRes)):
                    hw = waterRes[i].select_atoms("name HW*").center_of_mass()
                    hw = np.reshape(hw, (1,3))
                    ow = waterRes[i].select_atoms("name OW").positions
                    mu = hw - ow
                    mu0seg.append(mu)
                mu0List.append(mu0seg)
                
                #print("Dropped {} waters".format(len(dropWaters)))

        # for these hydration shell waters, compute the dipole vector mu
        muList=[]
        u.trajectory[currFrame] # point back to current frame
        for i in range(len(waterRes)):
            hw = waterRes[i].select_atoms("name HW*").center_of_mass()
            hw = np.reshape(hw, (1,3))
            ow = waterRes[i].select_atoms("name OW").positions
            mu = hw - ow
            muList.append(mu)
        allMus.append(muList)
    
    # now that we have dipole vectors, compute c
    # c = mu0.muT
    # want to append average c for each value of t
    allC=[]
    k=0 # k will be used to index mu0 list
    for i in range(len(allMus)):
        if len(allMus[i]) < len(allMus[i-1]) and i != 0:
            k+=1 # if the number of water drops, shift to next mu list
            # print("Just increased k, i is currently {}".format(i))
        mu0 = mu0List[k]
        muT = allMus[i]
        cList=[]
        for j in range(len(allMus[i])):
            c = np.dot(mu0[j], muT[j].T) / np.dot(mu0[j], mu0[j].T)
            cList.append(float(c))
        allC.append(np.mean(cList))
        # want an option to break the loop if c is below threshold
        if np.mean(cList) < threshold:
            break
    return allC

#Start concurrent tasks
async def query_concurrently(begin_idx: int, end_idx: int):
    tasks = []
    for i in range(begin_idx, end_idx):
        tasks.append(asyncio.create_task(calcC(i)))
    results = await asyncio.gather(*tasks)
    
    return results

# Execute batch tasks in sub processes
def run_batch_tasks(batch_idx: int, step: int):
    # print(r"Batch {}".format(batch_idx))
    
    begin = batch_idx * step
    end = begin + step
    if end > stop:
        end = stop # never exceed frames / 2
    
    results = [result for result in asyncio.run(query_concurrently(begin, end))]

    return results

# Distribute tasks in batches to be executed in sub-processes
async def main():
    begin = time.monotonic()
    
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, run_batch_tasks, batch_idx, step)
                 for batch_idx in range(n_cores)]
                 
    results = [result for sub_list in await asyncio.gather(*tasks) for result in sub_list]
    print(f"Time elapsed: {time.monotonic() - begin:.2f} second(s)")
    
    return results
    

#%% Run Analysis
if __name__ == "__main__":
    results = asyncio.run(main())

    # now we want to average each column, so for each value of t
    cMatrix = pd.DataFrame(results)
    allVals = cMatrix.mean(axis=0)
    
    decayLength = len(allVals)
    step = u.trajectory.dt
    frames=np.arange(0,decayLength*step,step)
    
    finalOutput = np.vstack((frames,allVals)).T
    header="t Cmu(t)"
    savetxt('output/{}-{}-{}-wr.dat'.format(title, clust, r2), finalOutput, header=header, fmt='%.5f', delimiter=' ')
