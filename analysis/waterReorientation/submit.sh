#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH -t 03:59:58
#SBATCH --job-name=SYSTEMTITLE-RCUT
#SBATCH -e stderr
#SBATCH -o stdout
#SBATCH -p msismall
#SBATCH --mem-per-cpu=5g

n_cores=24
title=SYSTEMTITLE
clust=CLUSTER
rcut=RCUT

sed s/TTTT/$title/g waterReorientation-asyncio.py > temp-$title-$rcut-$clust.py
sed s/AAAA/$clust/g temp-$title-$rcut-$clust.py > temp-$title-$rcut-$clust-1.py
sed s/BBBB/$rcut/g temp-$title-$rcut-$clust-1.py > temp-$title-$rcut-$clust-2.py
sed s/NNNN/$n_cores/g temp-$title-$rcut-$clust-2.py > temp-$title-$rcut-$clust-3.py
mv temp-$title-$rcut-$clust-3.py wr-$title-$rcut-$clust.py
rm temp-$title-$rcut-$clust.py temp-$title-$rcut-$clust-1.py temp-$title-$rcut-$clust-2.py
python wr-$title-$rcut-$clust.py
rm wr-$title-$rcut-$clust.py
