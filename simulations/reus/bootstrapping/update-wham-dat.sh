#!/bin/bash

for i in {0..NNNNBBBB..1} #Number of bootstrapped samples
do
    sed -e "s/AAAA/$i/g" plumed_wham.dat > plumed_wham_$i.dat
done
