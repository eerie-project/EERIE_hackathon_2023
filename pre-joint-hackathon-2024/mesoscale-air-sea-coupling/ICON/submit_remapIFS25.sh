#!/bin/bash

##ocean variables using remap_dm_r2b9O_IFS25.job
#declare -a varnamearr=("ssh" "to" "so" "mlotst10") # "mlotst")
#declare -a varnamearr=("Wind_Speed_10m" "sea_level_pressure")
#declare -a varnamearr=("atmos_fluxes_HeatFlux_Latent" "atmos_fluxes_HeatFlux_Sensible" "atmos_fluxes_FrshFlux_Precipitation" "atmos_fluxes_FrshFlux_Evaporation")
#declare -a varnamearr=("conc" "hi" "hs" "ice_u" "ice_v")

#for varname in "${varnamearr[@]}"
#do
#  #for yr in $(seq 2002 2006);  
#  for yr in $(seq 2002 2008);  
#  do 
#    sbatch remap_dm_r2b9O_IFS25.job ${varname} ${yr} 
#  done
#done

#declare -a varnamearr=("downSSTgrad" "taudiv")
#declare -a varnamearr=("crossSSTgrad" "taucurl")
#declare -a varnamearr=("crossSSTgrad")
#declare -a varnamearr=("taucurl")
#declare -a varnamearr=("Wekcurl" "Wekvortgrad")
#declare -a varnamearr=("Wekstern" "Wekclassic")
#declare -a varnamearr=("Wekstern")
#declare -a varnamearr=("Wekclassic")
#declare -a varnamearr=("sfcvort")
#declare -a varnamearr=("taumag")
#declare -a varnamearr=("windcurl")
#declare -a varnamearr=("winddiv")
#declare -a varnamearr=("windwork")
#declare -a varnamearr=("Wind_Speed_10m")
#declare -a varnamearr=("u" "v")
declare -a varnamearr=("u" "v" "atmos_fluxes_stress_xw" "atmos_fluxes_stress_yw")

for varname in "${varnamearr[@]}"
do
  #for yr in $(seq 2002 2008);  
  for yr in $(seq 2008 2008);  
  do 
    #for mth in $(seq 1 12);  
    for mth in $(seq 1 12);  
    do 
      sbatch remap_dm_yrmth_r2b9O_IFS25.job ${varname} ${yr} ${mth} 
    done
  done
done

##atmos variables using remap_dm_r2b8G_IFS25.job
#declare -a varnamearr=("tas" "uas" "vas" "psl" "sfcwind")
#declare -a varnamearr=("pr" "evspsbl" "clt" "prw")
#declare -a varnamearr=("prw" "sfcwind")
#declare -a varnamearr=("hfls" "hfss")
#declare -a varnamearr=("rlds" "rlus" "rsds" "rsus" "rsdt" "rsut" "rlut")
#declare -a varnamearr=("rlds" "rlus" "rsds" "rsus")
#declare -a varnamearr=("rsdt" "rsut" "rlut")
#declare -a varnamearr=("hfls" "sfcwind" "pr")
#declare -a varnamearr=("clt")

#for varname in "${varnamearr[@]}"
#do
#  for yr in $(seq 2002 2003);  
#   for yr in $(seq 2004 2008);  
#  do 
#    sbatch remap_dm_r2b8G_IFS25.job ${varname} ${yr} 
#  done
#done


#declare -a varnamearr=("SST")
#declare -a varnamearr=("WSP")
#for varname in "${varnamearr[@]}"
#do
#  for yr in $(seq 2002 2003);  
##   for yr in $(seq 2004 2008);  
#  do
#    for smdeg in $(seq 2 2 10);
#    do
#      echo $smdeg
#      sbatch remap_dm_r2b9Osm_IFS25.job ${varname} ${yr} ${smdeg}
#    done
#  done
#done




#######################################################################
#subdomains=("PacW" "PacE" "IndW" "IndE" "AtlW" "AtlE" "NAtl" "SO" "IndSO" "PacSO" "AtlSO" "AtlIndSO")
#for irgn in $(seq 0 `expr ${#subdomains[@]} - 1`);
#do
#  echo ${subdomains[$irgn]}
#  rgn=${subdomains[$irgn]}
#  sbatch exec_getspatialspec_r2b8.job rthk001 ${rgn}
#done

###For daily fields
##figdatearr=("202001-202006" "202007-202012" "202101-202106" "202107-202112" "202201-202202")
###For monthly fields
#figdatearr=("202002-202202")
#
#  for idate in $(seq 0 `expr ${#figdatearr[@]} - 1`);
#  do
#    figdate=${figdatearr[$idate]}
#    echo 'rgn='${rgn}', date='${figdate}
#    sbatch execFFT.job Wind_Speed_10m WSP ${figdate}
#  done
#done
##sbatch execFFT.job Wind_Speed_10m WSP 202001-202006 NAtl


#while [ $YYYYint -le $YYYYe ]; do
#  if [ $YYYYint -eq $YYYYs ]; then
#     MMint=$MMs
#  else
#     MMint=1
#  fi
#  if [ $YYYYint -eq $YYYYe ]; then
#     MMend=$MMe
#  else
#     MMend=12
#  fi
#  while [ $MMint -le $MMend ]; do
#     if [ $MMint -le 9 ]; then
#        MMint=`eval echo "0$MMint"`
#     fi
#     montharr+=( "${YYYYint}${MMint}" )
#     MMint=`expr $MMint + 01`
#  done
#  YYYYint=`expr $YYYYint + 01`
#done
##array length
#echo ${#montharr[@]}
###array list
##echo ${montharr[@]}
#
#for tidx in $(seq 0 ${#montharr[@]});
#do
#  echo "fdate="${montharr[$tidx]}
#  fdate=${montharr[$tidx]}
#  sbatch sm_monthly_r2b8.job ${varname} ${namevar} ${smdeg} ${fdate}
#done
#
