#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=64
#SBATCH -t 23:59:58
#SBATCH --job-name=plumed
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH  --gres=gpu:a100:1
#SBATCH  -p a100-4
#SBATCH --mem=123g
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=zajac028@umn.edu

source make-directories.sh
source run_mdrun.sh
source do-analysis.sh
