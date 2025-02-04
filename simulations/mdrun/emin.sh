#Energy minimization
gmx grompp -f emin.mdp \
	   -c ../box_solv/hydr-poly-26n-ua-box-solv-gly-47.gro \
	   -p ../topology/hydr-poly-26n-47gly-ua.top \
	   -o hydr-poly-26n-ua-box-solv-gly-47-emin.tpr

export OMP_NUM_THREADS=6
gmx mdrun -v -deffnm hydr-poly-26n-ua-box-solv-gly-47-emin \
	  -nb gpu -ntomp 6 -ntmpi 4
