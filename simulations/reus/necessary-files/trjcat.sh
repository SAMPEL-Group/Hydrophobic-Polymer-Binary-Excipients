source /home/sarupria/zajac028/software/load_scripts/load_gromacs-2021.4.sh
source /home/sarupria/zajac028/software/load_scripts/load_plumed-2.8.0.sh

gmx trjcat -cat -f dir[0-9]/npt-prod.xtc dir[0-9][0-9]/npt-prod.xtc -o npt-prod-cat.xtc

mpiexec -np 12 --oversubscribe plumed driver --plumed plumed_get_bias.dat --multi 12 --ixtc npt-prod-cat.xtc

