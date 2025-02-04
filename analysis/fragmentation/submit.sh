#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH -t 04:59:58
#SBATCH --job-name=fragmentation-TITLE-WINDOW-RUN
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH -p msismall
#SBATCH --mem=5g

title=TITLE
window=WINDOW
run=RUN

sed s/AAAA/$title/g fragmentationThreshold.py > fragmentationThreshold-$title-$window-$run-a.py
sed s/BBBB/$window/g fragmentationThreshold-$title-$window-$run-a.py > fragmentationThreshold-$title-$window-$run-b.py 
sed s/CCCC/$run/g fragmentationThreshold-$title-$window-$run-b.py > fragmentationThreshold-$title-$window-$run-c.py

python fragmentationThreshold-$title-$window-$run-c.py
rm fragmentationThreshold-$title-$window-$run-*.py
