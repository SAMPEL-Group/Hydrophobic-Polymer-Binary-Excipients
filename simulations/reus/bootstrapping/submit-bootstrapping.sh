#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=12
#SBATCH -t 01:59:59
#SBATCH --job-name=bootstrap
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH -p k40
#SBATCH --gres=gpu:k40:1
#SBATCH --mem=60g
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=zajac028@umn.edu

source run-bootstrapping.sh
