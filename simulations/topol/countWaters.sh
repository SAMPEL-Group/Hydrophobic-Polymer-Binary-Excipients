#for n in 79 157 236 314; do
for n in 47 93 139 185; do
for mol in arg gly gdm; do

grep 'SOL' hydr-poly-26n-tip4p05-$n$mol-ua.top > waterCounts/$n$mol-wat.dat
grep 'SOL' hydr-poly-26n-tip4p05-$n$mol-ua.top

done
done
