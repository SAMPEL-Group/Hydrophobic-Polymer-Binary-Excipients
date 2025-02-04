###README
The contents of this directory include the following:

=== update-dat.sh ===
Generate the plumed_$i.dat files for umbrella sampling. Set force constant and number of windows in this script.

=== mdrun.sh ===
Run a biased simulation along the radius of gyration.
Consists of energy minimization, NVT equilibration, NPT equilibration, and NPT production for each window.
MDP files are found in ../mdp/

=== submit.sh ===
Batch submission script to submit mdrun.sh to the cluster.

=== trjcat.sh ===
Combine the trajectories of each window.
Combine the colvar files from each window.

=== plumed-analysis.py ===
Plots the time series of the collective variable (radius of gyration).
Generates logweights for biases using WHAM.

=== plumed-wham.sh ===
Runs WHAM using PLUMED. Generates free energy surface.

=== plot-wham.sh ===
Plots results of WHAM / free energy surface. 
