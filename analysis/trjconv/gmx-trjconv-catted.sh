#title=47lys-reus
WORKING_DIR=/scratch.global/zajac028/$title
for r in 1 2 3 ; do
gmx trjconv -f $WORKING_DIR/run$r/npt-prod-cat-whole.xtc \
	    -s $WORKING_DIR/run$r/npt-prod-plumed.tpr \
	    -tu ns -dt 0.1 -split 100 \
	    -center -pbc whole \
	    -o ./test/$title-npt-prod-trunc-$r-.xtc << EOF
0
0
EOF

done
