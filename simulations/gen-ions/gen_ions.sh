j=1 # Number of ions to add

#Add chloride ions
gmx make_ndx -f $title-solv.gro \
	     -o $title-solv.ndx << EOF
q
EOF

gmx grompp -maxwarn 3 \
	   -f ions.mdp \
	   -c $title-solv.gro \
	   -p ../topology/$title.top \
	   -o temp.tpr

gmx genion -s temp.tpr \
	   -n $title-solv.ndx \
	   -o $title-nacl.gro \
	   -rmin 0.5 \
	   -pname NA -np $j << EOF 
SOL
EOF
