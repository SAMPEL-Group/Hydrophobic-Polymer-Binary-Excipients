title=186arg-glu
gmx make_ndx -f ../analysis/preferentialInteraction/traj/$title-reus.tpr \
	     -o ./$title-reus.ndx << EOF
r PolB | r Pol | r PolE
q
EOF
