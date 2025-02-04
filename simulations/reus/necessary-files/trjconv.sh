gmx trjconv -f npt-prod-cat.xtc \
	    -s ./dir0/npt-prod-plumed.tpr \
	    -pbc whole \
	    -center \
	    -tu ns -dt 0.1 \
	    -o npt-prod-cat-trunc.xtc
