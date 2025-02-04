source /home/sarupria/zajac028/software/load_scripts/load_gromacs-2021.4.sh
source /home/sarupria/zajac028/software/load_scripts/load_plumed-2.8.0.sh

source trjcat.sh
python plumed-analysis.py
source plumed-wham.sh
python plot-wham.py 
