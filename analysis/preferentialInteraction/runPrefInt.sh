nW=11 # Number of windows
nR=3 # Number of runs
specifier=arglys # Variant of code to use
for title in 186arg-lys ; do
for ((window=0;window<=nW;window++)); do
for ((run=1;run<=nR;run++)); do

sed s/TITLE/$title/g submit.sh > temp1-submit.sh
sed s/WINDOW/$window/g temp1-submit.sh > temp2-submit.sh
sed s/RUN/$run/g temp2-submit.sh > temp3-submit.sh
sed s/SPECS/$specifier/g temp3-submit.sh > temp4-submit.sh

sbatch temp4-submit.sh
rm temp1-submit.sh temp2-submit.sh
rm temp3-submit.sh temp4-submit.sh

done
done
done
