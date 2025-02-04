nW=11 # Number of windows
nR=3 # Number of runs
for mol in arg ; do
#for title in 0$mol-reus; do
for title in 47$mol-reus 93$mol-reus 185$mol-reus ; do
#for title in 48$mol-reus 94$mol-reus 186$mol-reus ; do
for ((window=0;window<=nW;window++)); do
for ((run=1;run<=nR;run++)); do

sed s/TITLE/$title/g submit.sh > temp1-submit.sh
sed s/WINDOW/$window/g temp1-submit.sh > temp2-submit.sh
sed s/RUN/$run/g temp2-submit.sh > temp3-submit.sh

sbatch temp3-submit.sh
rm temp1-submit.sh temp2-submit.sh
rm temp3-submit.sh 

done
done
done
done
