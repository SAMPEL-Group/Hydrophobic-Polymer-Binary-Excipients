#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH -t 12:59:58
#SBATCH --job-name=lys-glu-prod
#SBATCH -e stderr-name
#SBATCH -o stdout-name
#SBATCH  --gres=gpu:k40:2
#SBATCH  -p k40
#SBATCH --mem=20g
#SBATCH --mail-type=begin
#SBATCH --mail-typ=end
#SBATCH --mail-user=zajac028@umn.edu

module purge
module use /home/sarupria/shared/software/ModuleFiles/modules/linux-centos7-haswell
module load gromacs/2021.3-gcc/8.2.0-nompi-openmp-cuda10_2

title=tip4p05-26n-box-solv-lys-cl-glu-na
top=186lys-glu
i=186
loc=lysine-glutamate

source npt-prod.sh
