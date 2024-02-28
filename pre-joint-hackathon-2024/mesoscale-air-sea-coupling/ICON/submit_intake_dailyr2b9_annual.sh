#!/bin/bash

#Extracting daily ocean variables on annual terms
#declare -a namevararr=("SST" "WSP" "LHF" "SHF")
declare -a namevararr=("SST" "WSP" "LHF")
#declare -a namevararr=("LHF" "SHF" "LW" "SW")
#declare -a namevararr=("downSSTgrad" "crossSSTgrad" "taudiv" "taucurl")
#declare -a namevararr=("LHF")
#declare -a namevararr=("WSP")
#declare -a namevararr=("SST")

for namevar in "${namevararr[@]}"
do
  for yr in $(seq 2002 2003);  
  do 
    sbatch intake_dailyr2b9_annual.job ${namevar} ${yr} 
  done
done

