"""
What do we want to do?
Aim is to apply network analysis/percolation theory principles to excipient analysis.
Specifically, I hypothesize there is a connection between the percolation threshold of excipients
in the local domain of the polymer, and polymer stability. This may be related to the cavitation
energy associated with polymer folding/unfolding and solvation thermodynamics.
"""

### Import our trusty trajectory analysis modules
import numpy as np
from numpy import savetxt
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import MDAnalysis as md
from MDAnalysis.analysis.distances import distance_array, contact_matrix
from MDAnalysis.analysis import contacts
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis as HBA
from tqdm import tqdm
import pandas as pd
import time

begin = time.monotonic()

### Initialize the universe for analysis
title="AAAA"
window=BBBB
run=CCCC
gro="../preferentialInteraction/traj/{}.tpr".format(title)
traj="../preferentialInteraction/traj/{}-npt-prod-{}-trunc-{}.xtc".format(title, window, run)
u=md.Universe(gro, traj, refresh_offsets=True)

### Obtain all atoms in the local domain of the polymer
### Local domain can either be user-defined, or estimated from a method such as RDF or Pref Int
### Don't include the polymer or hydrogens
rCut = 7.0
allOutputs = []
for ts in tqdm(u.trajectory[::]):
    
    ### Make relevant selections
    polymer = u.select_atoms("resname PolE Pol PolB")
    local = u.select_atoms("same residue as (not group polymer) and around {} group polymer".format(rCut), polymer=polymer)
    # local = u.select_atoms("resname ARG and around {} group polymer".format(rCut), polymer=polymer)
    localHeavy = u.select_atoms("group local and not name H* MW", local=local)
    localHeavyExc = u.select_atoms("group local and not name H* and not resname water", local=local)
    rest = u.select_atoms("not group polymer and not group local", polymer=polymer, local=local)
    
    # Store positions
    restPos = rest.positions
    localHeavyPos = localHeavy.positions
    polymerPos = polymer.positions
    
    # Split into atoms and residues for indexing
    localHeavyAtoms = localHeavy.split("atom")
    localHeavyResidues = localHeavy.split("residue")
    localHeavyResids = localHeavy.resids
    localHeavyExcResids = localHeavyExc.resids
    n=len(localHeavyResidues)

    ### Next, find contacts to assemble a graph.    
    rThresh = 3.5
    
    localHeavyCOM = []
    for x in range(len(localHeavyResidues)):
        localHeavyCOM.append(localHeavyResidues[x].center_of_mass())
    localHeavyCOM = np.vstack((localHeavyCOM))
    
    edges = []
    nodes = []
    excNodes = []
    watNodes = []
    for i in range(n):
        # iRes = localHeavyResids[i]
        nodes.append(i)
        if localHeavyResids[i] in localHeavyExcResids:
            excNodes.append(i)
        else:
            watNodes.append(i)
        for j in range(n):
            if i != j:
                distMatrix = contacts.distance_array(localHeavyResidues[i], localHeavyResidues[j]) # Calc distance between all atoms belonging to i and j
                for x in range(len(localHeavyResidues[i])):
                    for y in range(len(localHeavyResidues[j])):
                        dist = distMatrix[x,y]
                        if dist < rThresh:
                            edges.append([i,j])
    
    # Keep only unique edges (i.e., order does not matter)
    uniqueEdges = set(tuple(sorted(t)) for t in edges)
    
    # Construct graph
    import networkx as nx
    G = nx.Graph() # Initialize graph
    G.add_nodes_from(nodes) # Add nodes
    G.add_edges_from(uniqueEdges) # Add edges for a given cut-off
        
    # Visualize graph
    # fig, ax = plt.subplots(figsize=(9,6))
    # pos = localHeavyCOM[:,0:2]
    # nx.draw(G, pos, ax=ax, node_size=20, node_color="maroon")
    # plt.tight_layout()
    # plt.show()
    
    closeness = nx.closeness_centrality(G)
    excCloseness = [closeness[x] for x in excNodes]
    watCloseness = [closeness[x] for x in watNodes]
    
    betweenness = nx.betweenness_centrality(G)
    excBetweenness = [betweenness[x] for x in excNodes]
    watBetweenness = [betweenness[x] for x in watNodes]
    
    meanExcClose = np.mean(excCloseness)
    meanWatClose = np.mean(watCloseness)
    meanExcBetween = np.mean(excBetweenness)
    meanWatBetween = np.mean(watBetweenness)
    
    output = [meanExcClose, meanWatClose, meanExcBetween, meanWatBetween]
    allOutputs.append(output)
    
finalOutput = np.vstack((allOutputs))

header = "excClose watClose excBetween watBetween"
savetxt('output/centrality-{}-{}-{}-r{}.dat'.format(title, window, run, rCut), finalOutput, header=header, delimiter=' ', fmt='%.3f', comments='') 

###
print(f"Time elapsed: {time.monotonic() - begin:.2f} second(s)")
