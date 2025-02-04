for title in 0arg 47arg 47lys 47glu 48arg-glu 48arg-lys 48lys-glu 93arg 93lys 93glu 94arg-glu 94arg-lys 94lys-glu 185arg 185lys 185glu 186arg-glu 186arg-lys 186lys-glu ; do
for clust in {0..4..1} ; do
for rcut in 7.0 ; do

sed s/SYSTEMTITLE/$title/g submit.sh > temp1-submit-$title-$rcut-$clust.sh
sed s/CLUSTER/$clust/g temp1-submit-$title-$rcut-$clust.sh > temp2-submit-$title-$rcut-$clust.sh
sed s/RCUT/$rcut/g temp2-submit-$title-$rcut-$clust.sh > temp3-submit-$title-$rcut-$clust.sh

sbatch temp3-submit-$title-$rcut-$clust.sh
rm temp1-submit-$title-$rcut-$clust.sh temp2-submit-$title-$rcut-$clust.sh temp3-submit-$title-$rcut-$clust.sh

done
done
done
