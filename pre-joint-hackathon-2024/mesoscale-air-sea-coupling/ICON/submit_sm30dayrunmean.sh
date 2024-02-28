#!/bin/sh


declare -a varnamearr=("to" "Wind_Speed_10m")
declare -a varnamearr=("taumag" "sfcvort" "windwork")
declare -a varnamearr=("winddiv" "windcurl")
declare -a varnamearr=("downSSTgrad" "taudiv" "crossSSTgrad" "taucurl")
declare -a varnamearr=("Wekcurl" "Wekvortgrad" "Wekstern" "Wekclassic")

for varname in "${varnamearr[@]}"
do
	for yr in $(seq 2002 2008);
	do
		for mth in $(seq 1 12);
		do
			sbatch sm_30dayrunmean_dailyIFS25_yrmth.job ${varname} ${yr} ${mth}
		done
	done
done


