title="185glu-reus" #Format narg-mol2-reus
n_bs=200
for i in 1 2 3
do

cd run$i
cp ~/virus-stabilization/hydrophobic-polymer/umbrella-sampling-plumed/bootstrapping/necessary-files-bootstrapping/* ./

sed s/AAAA/$n_bs/g run-bootstrapping.sh > temp1.sh
sed s/AABB/$title/g temp1.sh > temp2.sh
sed s/AACC/$i/g temp2.sh > temp3.sh
mv temp3.sh run-bootstrapping.sh

rm *temp*
sbatch submit-bootstrapping.sh

cd ../
done
