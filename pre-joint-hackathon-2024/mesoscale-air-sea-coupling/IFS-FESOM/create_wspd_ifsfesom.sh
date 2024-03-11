#!/bin/sh

expid='ifs-fesom'
varnamex1='10u'
varnamey1='10v'
namevarxy='wspd'

outdir=/work/bm1344/m300466/native/IFS/${namevarxy}
mkdir -p ${outdir}

for yyyy in $(seq 1971 1972);
do
   ifsdir=/work/bm1344/a270228/EERIE_NextG_Hackathon/IFS-FESOM_CONTROL-1950/tco1279-NG5/${yyyy}/IFS/original/daily
   for mth in $(seq 1 12);
   do 
      echo 'Compute wind speed for yr='${yyyy}', mth='${mth}
      if [ ${mth} -le 9 ]; then
         cdo -P 32 -chname,${varnamex1},${namevarxy} -setgridtype,regular -sqrt -add -sqr ${ifsdir}/${varnamex1}_10_${yyyy}0${mth}01-${yyyy}0${mth}??_daily_origin_grid.nc -sqr ${ifsdir}/${varnamey1}_10_${yyyy}0${mth}01-${yyyy}0${mth}??_daily_origin_grid.nc ${outdir}/${expid}_${namevarxy}_${yyyy}0${mth}_gridded.nc
      else
         cdo -P 32 -chname,${varnamex1},${namevarxy} -setgridtype,regular -sqrt -add -sqr ${ifsdir}/${varnamex1}_10_${yyyy}${mth}01-${yyyy}${mth}??_daily_origin_grid.nc -sqr ${ifsdir}/${varnamey1}_10_${yyyy}${mth}01-${yyyy}${mth}??_daily_origin_grid.nc ${outdir}/${expid}_${namevarxy}_${yyyy}${mth}_gridded.nc
      fi
   done
done 



