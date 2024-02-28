#!/bin/sh

expid='ifs-fesom'

#for yyyy in $(seq 1971 1972);
for yyyy in $(seq 1972 1972);
do
   ifsdir=/work/bm1344/a270228/EERIE_NextG_Hackathon/IFS-FESOM_CONTROL-1950/tco1279-NG5/${yyyy}/IFS/original/daily
   for mth in $(seq 9 12);
   do 
      echo 'Compute wind div curl for yr='${yyyy}', mth='${mth}
      if [ ${mth} -le 9 ]; then
         cdo -P 32 -sp2gp,cubic -uv2dv,cubic -setgridtype,regular -chvar,10u,u,10v,v -select,month=${mth} -merge ${ifsdir}/10u_10_${yyyy}0${mth}01-${yyyy}0${mth}??_daily_origin_grid.nc ${ifsdir}/10v_10_${yyyy}0${mth}01-${yyyy}0${mth}??_daily_origin_grid.nc /work/bm1344/m300466/native/IFS/${expid}_wind_divcurl_${yyyy}0${mth}_gridded.nc
      else
         cdo -P 32 -sp2gp,cubic -uv2dv,cubic -setgridtype,regular -chvar,10u,u,10v,v -select,month=${mth} -merge ${ifsdir}/10u_10_${yyyy}${mth}01-${yyyy}${mth}??_daily_origin_grid.nc ${ifsdir}/10v_10_${yyyy}${mth}01-${yyyy}${mth}??_daily_origin_grid.nc /work/bm1344/m300466/native/IFS/${expid}_wind_divcurl_${yyyy}${mth}_gridded.nc
      fi
   done
done 



