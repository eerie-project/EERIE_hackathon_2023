#!/bin/sh
# Submit jobs that low-pass filter the 30-day rolling mean daily means of IFS AMIP output
# Matthias Aengenheyster, March 2024

for yr in $(seq 2010 2020); do 
    for mn in $(seq 1 12); do 
        echo $yr $mn
        varname=sst
        echo $varname
        sbatch compute_filter_year_month.job ${varname} ${yr} ${mn}; 
        varname=speed
        echo $varname
        sbatch compute_filter_year_month.job ${varname} ${yr} ${mn}; 
        varname=winddiv
        echo $varname
        sbatch compute_filter_year_month.job ${varname} ${yr} ${mn}; 
        varname=downT
        echo $varname
        sbatch compute_filter_year_month.job ${varname} ${yr} ${mn}; 
    done
done

