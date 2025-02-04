#%% Import Stuff!!
import pandas as pd
import numpy as np
from numpy import savetxt
from tqdm import tqdm
import MDAnalysis as md
import time

begin = time.monotonic()

ionName = "CL"
rThresh = 10 # What is the maximum rcut we will evaluate?
dr = 0.5 # How coarse is the evaluation?

title="AAAA"
window=BBBB
run=CCCC

tpr="../traj/{}-reus.tpr".format(title)
traj="../traj/{}-reus-npt-prod-{}-trunc-{}.xtc".format(title, window, run)

u = md.Universe(tpr, traj)

polymer = u.select_atoms("resname Pol PolE PolB")
water = u.select_atoms("same residue as name OW")
ion = u.select_atoms("name {}".format(ionName))
exc = u.select_atoms("not group polymer and not group water and not group ion", polymer=polymer, water=water, ion=ion)

sigma = 3.73
useSurface = False # Future implementation accounting for vdW surface

bulkWater = len(water.split("residue"))
bulkIon = len(ion.split("residue"))
bulkExc = len(exc.split("residue"))
bulkN = bulkExc + bulkIon

def contactCheck(res):
    output = []
    resCOM = res.center_of_mass()
    for i in range(len(polyPos[:,0])):
        currBead = polyPos[i,:]
        dist = np.sqrt((currBead[0] - resCOM[0])**2 + (currBead[1] - resCOM[1])**2 + (currBead[2] - resCOM[2])**2)
        output.append(dist)
    return output

def residueSelect(resList):
    contacts = []
    for res in resList:
        dist = np.min(contactCheck(res)) # Get minimum distance of res from solute
        resid = np.unique(res.resids)[0]
        contacts.append([resid, dist])
    return np.asarray(contacts)

def countLocals(frame, k):
    if len(frame[k] > 0):
        local = len(np.where(frame[k][:,1] < rcut)[0])
    else:
        local = 0
    return local

allOutputs = []
for ts in u.trajectory:
    polymer = u.select_atoms("resname Pol PolE PolB")
    nearWater = u.select_atoms("same residue as group water and around {} group polymer".format(rThresh), water=water, polymer=polymer)
    nearExc = u.select_atoms("same residue as group exc and around {} group polymer".format(rThresh), exc=exc, polymer=polymer)
    nearIon = u.select_atoms("same residue as group ion and around {} group polymer".format(rThresh), ion=ion, polymer=polymer)
    lwRes = nearWater.split("residue")
    leRes = nearExc.split("residue")
    liRes = nearIon.split("residue")
    polyPos = polymer.positions
    
    wContacts = residueSelect(lwRes)
    eContacts = residueSelect(leRes)
    iContacts = residueSelect(liRes)
    
    output = [ts.frame, wContacts, eContacts, iContacts]
    allOutputs.append(output)

### Gamma Calculations
gammaOutputs = []
for frame in allOutputs:
    for rcut in np.arange(3,rThresh+dr,dr):
        localWater = countLocals(frame, 1)
        localExc = countLocals(frame, 2)
        localIon = countLocals(frame, 3)
        localN = localExc + localIon
        
        gammaExc = localExc - ((bulkExc - localExc)/(bulkWater - localWater))*localWater
        gammaIon = localIon - ((bulkIon - localIon)/(bulkWater - localWater))*localWater
        gammaTot = localN - ((bulkN - localN)/(bulkWater - localWater))*localWater
        
        output = [frame[0], rcut, gammaExc, gammaIon, gammaTot, localExc, localIon, localWater]
        gammaOutputs.append(output)
gammaOutputs = pd.DataFrame(gammaOutputs, columns=["frame", "rcut", "gammaExc", "gammaIon", "gammaTot", "localExc", "localIon", "localWater"])

header = "frame rcut gammaExc gammaIon gammaTot localExc localIon localWat"
savetxt('output/prefInt-{}-{}-{}.dat'.format(title, window, run), gammaOutputs, header=header, delimiter=' ', fmt='%.3f', comments='') 

print(f"Time elapsed: {time.monotonic() - begin:.2f} second(s)")
