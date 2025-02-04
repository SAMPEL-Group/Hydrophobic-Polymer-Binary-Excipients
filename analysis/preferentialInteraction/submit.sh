#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH -t 01:59:58
#SBATCH --job-name=prefInt-TITLE-WINDOW-RUN
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH -p msismall
#SBATCH --mem=5g

title=TITLE
window=WINDOW
run=RUN

specifier=SPECS

sed s/AAAA/$title/g prefInt-$specifier.py > prefInt-$title-$window-$run-a.py
sed s/BBBB/$window/g prefInt-$title-$window-$run-a.py > prefInt-$title-$window-$run-b.py 
sed s/CCCC/$run/g prefInt-$title-$window-$run-b.py > prefInt-$title-$window-$run-c.py

python prefInt-$title-$window-$run-c.py
rm prefInt-$title-$window-$run-*.py
