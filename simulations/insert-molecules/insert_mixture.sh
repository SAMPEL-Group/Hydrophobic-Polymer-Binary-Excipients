#24/48, 47/94, 70/140, 93/186

gmx insert-molecules -f tip4p05-26n-box.gro \
	  	     -o temp.gro \
		     -ci ../pdb_gro/lys.gro \
		     -replace water \
		     -nmol 70

gmx insert-molecules -f temp.gro \
                     -o tip4p05-26n-box-solv-lys-glu-140.gro \
                     -ci ../pdb_gro/glu.gro \
                     -replace water \
                     -nmol 70

rm temp.gro
