#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH -t 01:59:58
#SBATCH --job-name=centrality-TITLE-WINDOW-RUN
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH -p msismall
#SBATCH --mem=5g

title=TITLE
window=WINDOW
run=RUN

sed s/AAAA/$title/g closenessCentrality.py > closenessCentrality-$title-$window-$run-a.py
sed s/BBBB/$window/g closenessCentrality-$title-$window-$run-a.py > closenessCentrality-$title-$window-$run-b.py 
sed s/CCCC/$run/g closenessCentrality-$title-$window-$run-b.py > closenessCentrality-$title-$window-$run-c.py

python closenessCentrality-$title-$window-$run-c.py
rm closenessCentrality-$title-$window-$run-*.py
