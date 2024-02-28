## Model and technical details
- We use 7-years of ICON outputs from EERIE run (erc1011)
- Spatial filtering uses cdo operator `smooth`, a simple filter with diminishing weights from 1 to 0.2 for a specified filtering length (say 3deg)

## Methodology
1) [Extract and compute daily quantities](#1-extract-and-compute-daily-quantities)
2) [Remap onto regular 0.25deg grid](#2-remap-onto-regular-025deg-grid)
3) [Perform 30-day running mean on 0.25deg grid files](#3-perform-30-day-running-mean-on-025deg-grid-files)
4) [Spatially high-pass 30-day running mean on 0.25deg grid files](#4-spatially-high-pass-30-day-running-mean)
5) [Compute coupling coefficients](#5-compute-coupling-coefficients) 

### 1) Extract and compute daily quantities
- [Stress magnitude](#wind-stress-magnitude)
	- taumag_erc1011.job
- [Wind divergence and curl](#surface-wind-divergence-and-curl)
	- create_daily_winddivcurl_erc1011.py
- [Downwind SST gradients (stress), crosswind SST gradients (stress), stress divergence, stress curl](#downwind-and-crosswind-sst-gradients-from-stress-plus-stress-divergence-and-curl)
	- create_daily_SSTgrad_TAUdivcurl_erc1011.py
	- create_daily_taucurl_erc1011.py
    - submit_create_dm_SSTgradTAUdivcurl.job
- [Surface vorticity](#surface-vorticity)
	- create_daily_sfcvort_erc1011.py
- [Surface KE](#surface-ke)
	- sfcKE_erc1011.job
- [Surface geostrophic KE and vorticity](#surface-geostrophic-ke-and-vorticity)
	- create_daily_sfcgeoKE_erc1011.py
	- create_daily_sfcgeovort_erc1011.py
	- exec_create_dm_geostrophic.job
- [Wind work](#wind-work)
	- windwork_erc1011.job
	- eddywindwork_erc1011.sh
- [Eddy-induced Ekman pumping (Wek): curl, vortgrad, Stern, classical)](#eddy-induced-ekman-pumping)
	- create_daily_EkmanPumping_erc1011.py
	- exec_create_dm_EkmanPumping.job

#### Get daily SST, wind speed, turbulent fluxes
Extract SST, wind speed at 10m, LHF and SHF using [intake_dailyr2b9_annual.job](mesoscale-air-sea-coupling/ICON/intake_dailyr2b9_annual.job) and [submit_intake_dailyr2b9_annual.sh](mesoscale-air-sea-coupling/ICON/submit_intake_dailyr2b9_annual.sh)

Script includes time shift needed for these variables due to ICON's way of time-stamping output data.

#### Wind stress magnitude
Compute daily wind stress magnitude using
[taumag_erc1011.job](mesoscale-air-sea-coupling/ICON/taumag_erc1011.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch taumag_erc1011.job ${yr} ${mth}; done; done


#### Surface wind divergence and curl
uas and vas are outputted on atm grid, not ocean grid. Since ocean has fewer points than atm, we can regrid and compute divergence and curl on ocean grid. Then interpolate onto 0.25deg grid, then get 30-day running mean, then spatially filter.

To remap from atm to oce grid, use [remap_dm_yrmth_r2b8G_r2b9O.job](mesoscale-air-sea-coupling/ICON/remap_dm_yrmth_r2b8G_r2b9O.job) 

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch remap_dm_yrmth_r2b8G_r2b9O.job uas ${yr} ${mth}; done; done
	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch remap_dm_yrmth_r2b8G_r2b9O.job vas ${yr} ${mth}; done; done

Compute daily wind divergence and curl using [create_daily_winddivcurl_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_winddivcurl_erc1011.py) and [submit_create_dm_winddivcurl.job](mesoscale-air-sea-coupling/ICON/submit_create_dm_winddivcurl.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch submit_create_dm_winddivcurl.job ${yr} ${mth}; done; done


#### Downwind and crosswind SST gradients from stress plus stress divergence and curl
Compute these quantities using [create_daily_SSTgrad_TAUdivcurl_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_SSTgrad_TAUdivcurl_erc1011.py) , [create_daily_taucurl_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_taucurl_erc1011.py) and [submit_create_dm_SSTgradTAUdivcurl.job](mesoscale-air-sea-coupling/ICON/submit_create_dm_SSTgradTAUdivcurl.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch submit_create_dm_SSTgradTAUdivcurl.job ${yr} ${mth}; done; done

#### Surface vorticity
Use [create_daily_sfcvort_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_sfcvort_erc1011.py) and [exec_create_dm_sfcvort.job](mesoscale-air-sea-coupling/ICON/exec_create_dm_sfcvort.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch exec_create_dm_sfcvort.job ${yr} ${mth}; done; done

#### Surface KE
Use [sfcKE_erc1011.job](mesoscale-air-sea-coupling/ICON/sfcKE_erc1011.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch sfcKE_erc1011.job ${yr} ${mth}; done; done

#### Surface geostrophic KE and vorticity
Use [create_daily_sfcgeoKE_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_sfcgeoKE_erc1011.py), [create_daily_sfcgeovort_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_sfcgeovort_erc1011.py) and [exec_create_dm_geostrophic.job](mesoscale-air-sea-coupling/ICON/exec_create_dm_geostrophic.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch exec_create_dm_geostrophic.job ${yr} ${mth}; done; done


#### Wind work
Use [windwork_erc1011.job](mesoscale-air-sea-coupling/ICON/windwork_erc1011.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch windwork_erc1011.job ${yr} ${mth}; done; done

#### Eddy-induced Ekman pumping
Ekman pumping (Wek) has classical vs Stern (1965), 
where Stern = curl + vortgrad

Use [create_daily_EkmanPumping_erc1011.py](mesoscale-air-sea-coupling/ICON/create_daily_EkmanPumping_erc1011.py) and [exec_create_dm_EkmanPumping.job](mesoscale-air-sea-coupling/ICON/exec_create_dm_EkmanPumping.job)

	for yr in $(seq 2002 2008); do for mth in $(seq 1 12); do sbatch exec_create_dm_EkmanPumping.job ${yr} ${mth}; done; done

### 2) Remap onto regular 0.25deg grid

Use [remap_dm_yrmth_r2b9O_IFS25.job](mesoscale-air-sea-coupling/ICON/remap_dm_yrmth_r2b9O_IFS25.job) and [submit_remapIFS25.sh](ICON/submit_remapIFS25.sh)

	./submit_remapIFS25.sh


If files were created with [remap_dm_yrmth_r2b9O_IFS25.job](mesoscale-air-sea-coupling/ICON/remap_dm_yrmth_r2b9O_IFS25.job), then they need to be stitched together with [stitchfiles.sh](mesoscale-air-sea-coupling/ICON/stitchfiles.sh)

	./stitchfiles.sh
 
### 3) Perform 30-day running mean on 0.25deg grid files
Use [30dayrunmean_erc1011_IFS25.job](mesoscale-air-sea-coupling/ICON/30dayrunmean_erc1011_IFS25.job)

```bash
declare -a varnamearr=("to" "Wind_Speed_10m")
declare -a varnamearr=("taumag" "sfcvort" "windwork")
declare -a varnamearr=("winddiv" "windcurl")
declare -a varnamearr=("downSSTgrad" "taudiv" "crossSSTgrad" "taucurl")
declare -a varnamearr=("Wekcurl" "Wekvortgrad" "Wekstern" "Wekclassic")

for varname in "${varnamearr[@]}"
do
	sbatch 30dayrunmean_erc1011_IFS25.job ${varname}
done
```

### 4) Spatially high-pass 30-day running mean
Use [sm_30dayrunmean_dailyIFS25_yrmth.job](mesoscale-air-sea-coupling/ICON/sm_30dayrunmean_dailyIFS25_yrmth.job) and [submit_sm30dayrunmean.sh](mesoscale-air-sea-coupling/ICON/submit_sm30dayrunmean.sh)

	./submit_sm30dayrunmean.sh

### 5) Compute coupling coefficients 

Global maps of coupling coefficients are evaluated via temporal regressions for a given season (JJA, DJF). Standard errors are also computed to provide 95\% confidence bounds to the coupling coefficients. We took a conservative estimate of 40 for effective degrees of freedom. 

Please see [regress_stderror.sh](ICON/regress_stderror.sh) for details.
