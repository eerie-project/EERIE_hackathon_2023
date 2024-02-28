#!/bin/sh

for yr in $(seq 2008 2008);
do
   #for mth in $(seq 1 12);
   for mth in $(seq 1 12);
   do
     echo 'Computing Ekman pumping for '${yr}${mth}
     #sbatch exec_create_dm_EkmanPumping.job $yr $mth
     sbatch exec_create_dm_geostrophic.job $yr $mth
   done
done

