source ~/software/load_scripts/load_plumed-2.8.0.sh 

n_bs=200 #USER INPUT: Set the Number of Bootstraps
k="0arg-reus" #USER INPUT: Set the Number of Arginine
r=1 #USER INPUT: Set the replication number

sed s/NNNNBBBB/$n_bs/g update-wham-dat.sh > temp1.sh
sed s/NNNNBBBB/$n_bs/g bootstrap_biases.py > temp2a.py
sed s/NNNNKKKK/$k/g temp2a.py > temp2b.py
sed s/NNNNRRRR/$r/g temp2b.py > temp2c.py
sed s/NNNNBBBB/$n_bs/g plumed-wham.sh > temp3.sh
sed s/NNNNBBBB/$n_bs/g get-average-fes-from-bootstrap.py > temp4a.py
sed s/NNNNKKKK/$k/g temp4a.py > temp4b.py

source temp1.sh
python temp2c.py
source temp3.sh
python temp4b.py

mkdir temp-fes
mv *temp_fes* ./temp-fes
#rm *
