#User input: select the window number for cluster analysis
n=6 #User input: select the index number for group of interest
title="0arg"
common_files=/home/sarupria/zajac028/virus-stabilization/hydrophobic-polymer/reus-plumed

mkdir components

#Create an index file so we can select the group of interest
gmx make_ndx -f ./dir0/npt-prod.gro -o ./components/poly-wat.ndx << EOF
r PolB | r Pol | r PolE | r water
q
EOF


#First, extract only the group of interest from the trajectory
gmx trjconv -f ./npt-prod-cat.xtc \
            -s ./dir0/npt-prod-plumed.tpr \
            -n ./components/poly-wat.ndx \
	    -pbc whole \
            -o ./components/poly-wat.xtc << EOF
$n
EOF

gmx trjconv -f ./npt-prod-cat.xtc \
            -s ./dir0/npt-prod-plumed.tpr \
            -n ./components/poly-wat.ndx \
	    -pbc whole \
            -tu ps -b 0 -e 0 \
            -o ./components/poly-wat.gro << EOF
$n
EOF

#Now make a new index to get energy groups
gmx make_ndx -f ./components/poly-wat.gro -o ./components/poly-wat.ndx << EOF
r PolB | r Pol | r PolE
r water
q
EOF

#We also need a .tpr for the group of interest
gmx grompp -f $common_files/mdp/energy-groups.mdp \
           -c ./components/poly-wat.gro \
	   -n ./components/poly-wat.ndx \
           -p $common_files/topol/hydr-poly-26n-tip4p05-$title-ua.top \
           -o ./components/poly-wat.tpr

#Lastly, rerun the trajectory
gmx mdrun -s ./components/poly-wat.tpr \
          -deffnm ./components/poly-wat-rerun -v \
          -rerun ./components/poly-wat.xtc

#And extract energy
gmx energy -f poly-wat-rerun.edr \
	   -o $title-reus-ie.xvg << EOF
15
16
17
18
19
20
21
22
23
24
25
26
EOF
