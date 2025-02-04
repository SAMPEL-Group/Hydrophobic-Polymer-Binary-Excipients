mkdir traj
mkdir files-to-save

mv npt-prod-cat.xtc ./traj/npt-prod-cat.xtc

for i in {0..11..1}
do

cd dir$i
mv npt-prod.xtc ../traj/npt-prod-$i.xtc
mv npt-equil.xtc ../traj/npt-equil-$i.xtc
mv nvt-equil.xtc ../traj/nvt-equil-$i.xtc
cd ../

done

mv !(traj) files-to-save
