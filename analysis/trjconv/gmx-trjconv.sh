for i in {0..11..1}; do
for r in 1 ; do
gmx trjconv -f $WORKING_DIR/dir$i/npt-prod.xtc \
	    -s $WORKING_DIR/dir$i/npt-prod-plumed.tpr \
	    -tu ns -dt 0.1 \
	    -center -pbc whole \
	    -o ./traj/$title-npt-prod-$i-trunc-$r.xtc << EOF
0
0
EOF

done
done
