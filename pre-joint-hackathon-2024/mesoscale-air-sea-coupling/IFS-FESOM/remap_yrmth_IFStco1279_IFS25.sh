#!/bin/sh

expid='ifs-fesom'
varname='wspd'

srcgrid=/work/mh0256/m300466/ifsfesomgrids/variable_on_tco1279gridpoint.nc
wghtfile=/work/mh0256/m300466/ifsfesomgrids/tco1279gridpoint_to_IFS25invertlat_conremapweights.nc
targetgrid=/work/mh0256/m300466/DPP/grid/temp_IFS25invertlat_MR_gridexample.nc
datadir=/work/bm1344/m300466/native/IFS/${varname}

outdir=/work/bm1344/m300466/reg25/ifsfesom/${varname}
mkdir -p ${outdir}


for yyyy in $(seq 1971 1972);
do
   for mth in $(seq 1 12);
   do
      echo 'Remap '${varname}' for yr='${yyyy}', mth='${mth}
      if [ ${mth} -le 9 ]; then
	  cdo -P 32 -remap,${targetgrid},${wghtfile} ${datadir}/${expid}_${varname}_${yyyy}0${mth}_gridded.nc ${outdir}/${expid}_${varname}_${yyyy}0${mth}_IFS25.nc
      else
          cdo -P 32 -remap,${targetgrid},${wghtfile} ${datadir}/${expid}_${varname}_${yyyy}${mth}_gridded.nc ${outdir}/${expid}_${varname}_${yyyy}${mth}_IFS25.nc
      fi
   done
done


