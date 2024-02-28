
#!/bin/bash

declare -a varnamearr=("to" "Wind_Speed_10m")
declare -a varnamearr=("taumag" "sfcvort" "windwork")
declare -a varnamearr=("winddiv" "windcurl")
declare -a varnamearr=("downSSTgrad" "taudiv" "crossSSTgrad" "taucurl")
declare -a varnamearr=("Wekcurl" "Wekvortgrad" "Wekstern" "Wekclassic")


for varname in "${varnamearr[@]}"2
do
  cd /work/bm1344/k203123/reg25/erc1011/${varname}
  for yr in $(seq 2002 2008);
  do
     cdo -mergetime [ erc1011_${varname}_dm_${yr}??_IFS25.nc ] erc1011_${varname}_dm_${yr}0101-${yr}1231_IFS25.nc; 
  done
done

