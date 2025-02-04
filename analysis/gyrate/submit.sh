#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH -t 01:59:58
#SBATCH --job-name=polystat
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH -p msismall
#SBATCH --mem=5g

title=0arg-reus
source gmx-gyrate.sh
