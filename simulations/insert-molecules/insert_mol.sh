gmx insert-molecules -f hydr-poly-26n-ua-box-solv.gro \
	  	     -o hydr-poly-26n-ua-box-solv-gly-185.gro \
		     -ci ../emin/gly-emin.gro \
		     -replace water \
		     -nmol 185
