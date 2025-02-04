for i in {0..NNNNBBBB..1}
do

plumed --no-mpi driver --noatoms --plumed plumed_wham_$i.dat --kt 2.4943387854

done
