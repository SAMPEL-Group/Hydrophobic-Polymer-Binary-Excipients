#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH -t 07:59:58
#SBATCH --job-name=trjconv
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH -p msismall
#SBATCH --mem=5g
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=zajac028@umn.edu

title=185arg-reus
WORKING_DIR=/scratch.global/zajac028/reus/htt
source trjconv-htt.sh
