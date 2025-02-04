source /home/sarupria/zajac028/software/load_scripts/load_gromacs-2021.4.sh
source /home/sarupria/zajac028/software/load_scripts/load_plumed-2.8.0.sh

common_files=/home/sarupria/zajac028/virus-stabilization/hydrophobic-polymer/reus-plumed
arg_num=185arg

#NPT production

for i in {0..11}; do
	gmx grompp -f $common_files/mdp/npt-prod.mdp \
		   -c dir$i/npt-equil.gro \
		   -r dir$i/npt-equil.gro \
		   -p $common_files/topol/hydr-poly-26n-tip4p05-$arg_num-ua.top \
		   -po dir$i/npt-prod-mdout.mdp -o dir$i/npt-prod-plumed.tpr
done

mpiexec -np 12 --oversubscribe gmx_mpi mdrun -multidir dir? dir?? -plumed ../plumed.dat \
          -s npt-prod-plumed.tpr -cpi npt-prod.cpt -x npt-prod.xtc \
          -v -deffnm npt-prod -replex 200\
