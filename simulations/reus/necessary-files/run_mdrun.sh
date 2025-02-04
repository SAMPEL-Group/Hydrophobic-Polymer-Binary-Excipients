source /home/sarupria/zajac028/software/load_scripts/load_gromacs-2021.4.sh
source /home/sarupria/zajac028/software/load_scripts/load_plumed-2.8.0.sh

common_files=/home/sarupria/zajac028/virus-stabilization/hydrophobic-polymer/reus-plumed
arg_num=139arg

#Energy minimization

for i in {0..11}; do
	gmx grompp -f $common_files/mdp/emin.mdp \
		   -c $common_files/conf/hydr-poly-26n-tip4p05-$arg_num-ua.gro \
		   -r $common_files/conf/hydr-poly-26n-tip4p05-$arg_num-ua.gro \
		   -p $common_files/topol/hydr-poly-26n-tip4p05-$arg_num-ua.top \
		   -po dir$i/emin_$i-mdout.mdp -o dir$i/plumed.tpr
done



mpiexec -np 12 --oversubscribe gmx_mpi mdrun -multidir dir? dir?? -plumed ../plumed.dat \
          -s plumed.tpr \
          -v -deffnm emin \

#NVT Equilibration

for i in {0..11}; do
	gmx grompp -f $common_files/mdp/nvt-equil.mdp \
		   -c dir$i/emin.gro \
		   -r dir$i/emin.gro \
		   -p $common_files/topol/hydr-poly-26n-tip4p05-$arg_num-ua.top \
		   -po dir$i/nvt-equil-mdout.mdp -o dir$i/nvt-equil-plumed.tpr
done

mpiexec -np 12 --oversubscribe gmx_mpi mdrun -multidir dir? dir?? -plumed ../plumed.dat \
          -s nvt-equil-plumed.tpr -x nvt-equil.xtc \
          -v -deffnm nvt-equil \

#NPT Equilibration

for i in {0..11}; do
	gmx grompp -f $common_files/mdp/npt-equil.mdp \
		   -c dir$i/nvt-equil.gro \
		   -r dir$i/nvt-equil.gro \
		   -p $common_files/topol/hydr-poly-26n-tip4p05-$arg_num-ua.top \
		   -po dir$i/npt-equil-mdout.mdp -o dir$i/npt-equil-plumed.tpr
done

mpiexec -np 12 --oversubscribe gmx_mpi mdrun -multidir dir? dir?? -plumed ../plumed.dat \
          -s npt-equil-plumed.tpr -x npt-equil.xtc \
          -v -deffnm npt-equil \

#NPT production

for i in {0..11}; do
	gmx grompp -f $common_files/mdp/npt-prod.mdp \
		   -c dir$i/npt-equil.gro \
		   -r dir$i/npt-equil.gro \
		   -p $common_files/topol/hydr-poly-26n-tip4p05-$arg_num-ua.top \
		   -po dir$i/npt-prod-mdout.mdp -o dir$i/npt-prod-plumed.tpr
done

mpiexec -np 12 --oversubscribe gmx_mpi mdrun -multidir dir? dir?? -plumed ../plumed.dat \
          -s npt-prod-plumed.tpr -x npt-prod.xtc \
          -v -deffnm npt-prod -replex 200\
