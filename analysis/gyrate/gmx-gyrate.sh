nW=11 # Number of windows
nR=3 # Number of runs
#for title in 47lys-reus 93lys-reus 185lys-reus ; do
for ((window=0;window<=nW;window++)); do
for ((run=1;run<=nR;run++)); do

gmx gyrate   -f ../preferentialInteraction/traj/$title-npt-prod-$window-trunc-$run.xtc \
	     -s ../preferentialInteraction/traj/$title.tpr \
	     -n ../../ndx/$title.ndx \
	     -o gyrate-$title-$window-$run.xvg << EOF
PolB_Pol_PolE
EOF

done
done
