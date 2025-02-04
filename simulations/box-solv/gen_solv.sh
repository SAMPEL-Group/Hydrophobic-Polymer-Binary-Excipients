gmx solvate -cp $title-box.gro \
	    -cs tip4p.gro \
	    -o $title-box-solv.gro \
	    -p ../topology/$title.top 
