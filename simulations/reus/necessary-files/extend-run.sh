for i in {0..11}
do

mv ./dir$i/npt-prod-plumed.tpr ./dir$i/npt-prod-plumed.old.tpr
gmx convert-tpr -s ./dir$i/npt-prod-plumed.old.tpr \
		-o ./dir$i/npt-prod-plumed.tpr \
		-until 25000

done
