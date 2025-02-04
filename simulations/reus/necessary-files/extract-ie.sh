i=18

for h in pol wat arg cl
do

j=$((i+1))
k=$((j+1))
l=$((k+1))

gmx energy -f ./components/poly-wat-arg-rerun.edr -o ./components/185arg-reus-pol-$h-ie.xvg << EOF
$i
$j
$k
$l
EOF

((i+=4))

done
