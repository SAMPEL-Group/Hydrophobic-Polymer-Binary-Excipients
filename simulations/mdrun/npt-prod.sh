gmx grompp \
 -f ../mdp-files/npt-prod.mdp \
 -c ../../equil/$loc/$title-$i-npt-equil.gro \
 -r ../../equil/$loc/$title-$i-npt-equil.gro \
 -t ../../equil/$loc/$title-$i-npt-equil.cpt \
 -p ../../topology/$top.top \
 -o ../$loc/$title-$i-npt-prod.tpr

export OMP_NUM_THREADS=6
gmx mdrun -s ../$loc/$title-$i-npt-prod.tpr \
	  -v -deffnm ../$loc/$title-$i-npt-prod \
	  -nb gpu -ntomp 6 -ntmpi 4

gmx trjconv \
 -f ../$loc/$title-$i-npt-prod.xtc \
 -s ../$loc/$title-$i-npt-prod.tpr \
 -o ../$loc/$title-$i-npt-prod.xtc -pbc whole << EOF
0
0
EOF

