## Model and technical details
- For SST-wind speed coupling, we use 21-years (1950-1970) IFS/FESOM or 11-years (2010-2020) of IFS-AMIP
- Coupling with current feedback and/or wind stress can only be computed from 1971 onwards
- Spatial filtering uses GCM filter (Gaussian filter with spatial scales 30*R where R is the Rossby radius)
- IFS-FESOM uses tco1279 (9km) /NG5 (4-5km) while IFS-AMIP uses tco399 (28km) resolution.

## Methodology
1) [Extract and/or compute daily quantities](#1-extract-and-compute-daily-quantities) needed for getting coupling coefficient.
   - Compute wind divergence and curl on IFS grid via cdo operators. If IFS-AMIP have outputs of windstress on IFS grid, then compute div/curl. 
   - For some ocean data (ocu,ocv,tx_sur,ty_sur): compute gradients and div/curl on native grid. IFS-FESOM only has windstress (tx_sur,ty_sur) on ocean grid.
   - Regrid SST gradients onto IFS gridded grid. 
    (dSST/dx, dSST/dy) are needed to compute crosswind and downwind SST gradients (multiply gradients with sine/cosine angle of wind). Do this for IFS-AMIP runs. For IFS/FESOM, since windstress are on ocean native grid, then we can compute crosswind/downwind SST gradients on ocean native grid. 

2) [Remap onto regular 0.25deg grid](#2-remap-onto-regular-025deg-grid). Regrid SST, vorticity of surface currents and (ocu,ocv), and windstress div/curl onto 0.25deg grid. 
   - SST is meant for coupling with wind speed, LHF, SHF, precip, cloud cover.  
   - Surface current vorticity to be coupled with windstress and wind curl. 
   - Surface current velocity components (ocu,ocv) dot product with (taux,tauy) gives wind work.
 
3) [Perform 30-day running mean on 0.25deg grid files](#3-perform-30-day-running-mean-on-025deg-grid-files) 
4) [Spatially high-pass 30-day running mean on 0.25deg grid files](#4-spatially-high-pass-30-day-running-mean) (GCM filter: constant value vs 30*R)
5) [Compute coupling coefficients](#5-compute-coupling-coefficients) by taking their regressions per given season.

## Example for SST-wind speed coupling
We will first go through how it is done with SST and wind speeds as they are somewhat readily available outputs. Wind speeds are computed from 10m (u,v) winds on IFS grids.  



### 1) Extract and compute daily quantities
- [10m wind speeds](#wind-speeds-at-10m)
	- [create_wspd_ifsfesom.sh](mesoscale-air-sea-coupling/IFS-FESOM/create_wspd_ifsfesom.sh)
	- [create_wspd_ifsfesom_remapto_IFS25.job](mesoscale-air-sea-coupling/IFS-FESOM/create_wspd_ifsfesom_remapto_IFS25.job)
- [Wind divergence and curl](#surface-wind-divergence-and-curl) on IFS grid via cdo operators.  
	- [create_winddivcurl_ifsfesom.sh](mesoscale-air-sea-coupling/IFS-FESOM/create_winddivcurl_ifsfesom.sh)
   - [create_winddivcurl_ifsamip_tco399.job](mesoscale-air-sea-coupling/IFS-FESOM/create_winddivcurl_ifsamip_tco399.job)
- [Windstress divergence and curl](#windstress-divergence-and-curl) on IFS grid via cdo operators. IFS-AMIP has outputs of windstress on IFS grid, while IFS-FESOM does not.
   - [create_taudivcurl_ifsamip_tco399.job](mesoscale-air-sea-coupling/IFS-FESOM/create_taudivcurl_ifsamip_tco399.job)

- Compute gradients, divergence, curl of ocean variables on native ocean grid (skipped in this example). Since wind stress will also be on FESOM native grid, we will need to compute stress div/curl on FESOM grid.
   - [ calculate gradient of SST (dSST/dX and dSST/dY) on fesom native grid](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/IFS-FESOM/grad_SST_fesom.ipynb)
- Compute SST gradients for OSTIA SSTs, then regrid to IFS gridded grid (skipped for SST-wind speed coupling)
   - Matthias will take care of this
- Downwind/crosswind SST calculations by multiplying SST gradients with angle of wind or stress (mostly on IFS original/gridded grid or FESOM native grid)
   - Dian will take care of this
- Compute wind work for IFS/FESOM (windstress * ocean_currents)
   Can only be done where wind stress is available (likely FESOM native grid)

#### Wind speeds at 10m
Compute daily wind speeds using
[create_wspd_ifsfesom.sh](mesoscale-air-sea-coupling/IFS-FESOM/create_wspd_ifsfesom.sh) or combine wind speed calculation with remapping to 0.25deg grid with [create_wspd_ifsfesom_remapto_IFS25.job](mesoscale-air-sea-coupling/IFS-FESOM/create_wspd_ifsfesom_remapto_IFS25.job)
```bash
./create_wspd_ifsfesom.sh
```
OR:
```bash
for yr in $(seq 1950 1970); do sbatch create_wspd_ifsfesom_remapto_IFS25.job ${yr}; done
```
After which perform get 30-day running mean, and then spatially filter.

#### Surface wind divergence and curl
10u and 10v are outputted on IFS grid. There's no land mass to deal with for atm variables, so we can compute divergence and curl with cdo operators. Then interpolate onto 0.25deg grid, then get 30-day running mean, then spatially filter.

Compute daily wind divergence and curl for:
   - IFS-FESOM using [create_winddivcurl_ifsfesom.sh](mesoscale-air-sea-coupling/IFS-FESOM/create_winddivcurl_ifsfesom.sh)
      ```bash
      ./create_wspd_ifsfesom.sh
      ```

   - IFS-AMIP using [create_winddivcurl_ifsamip_tco399.job](mesoscale-air-sea-coupling/IFS-FESOM/create_winddivcurl_ifsamip_tco399.job) 
      ```bash
      for yr in $(seq 2010 2020); do sbatch create_winddivcurl_ifsamip_tco399.job 'OSTIA_c_LR30_a_LR30' ${yr}; done
      ```


#### Windstress divergence and curl
ewss and nsss are outputted on IFS grid for IFS-AMIP, but not for IFS/FESOM. Instead, IFS-FESOM will output some stress (tx_sur,ty_sur) from 1972-1980 on FESOM native grid. So we compute wind stress curl and divergence on native FESOM grid with pyfesom2, then interpolate onto 0.25deg grid, then get 30-day running mean, then spatially filter.

Compute daily windstress divergence and curl for IFS-AMIP using [create_taudivcurl_ifsamip_tco399.job](mesoscale-air-sea-coupling/IFS-FESOM/create_taudivcurl_ifsamip_tco399.job)

```bash
for yr in $(seq 2010 2020); do sbatch create_taudivcurl_ifsamip_tco399.job 'OSTIA_c_LR30_a_LR30' ${yr}; done
```

### 2) Remap onto regular 0.25deg grid
When regridding, it is good practise to compute the remapping weights.
	
   - [remapping_weights.sh](mesoscale-air-sea-coupling/IFS-FESOM/remapping_weights.sh)

To remap from IFS (tco1279) grid to 0.25deg grid, use [remap_yrmth_IFStco1279_IFS25.sh](mesoscale-air-sea-coupling/IFS-FESOM/remap_yrmth_IFStco1279_IFS25.sh)

To remap from FESOM grid to 0.25deg grid, use [remap_yrmth_fesomNG5_IFS25.job](mesoscale-air-sea-coupling/IFS-FESOM/remap_yrmth_fesomNG5_IFS25.job)

```bash
	for yr in $(seq 1950 1970); do sbatch remap_yrmth_fesomNG5_IFS25.job ${yr}; done
```

To remap from IFS-AMIP (tco399) grid to 0.25deg grid, use [remap_yrmth_IFStco399_IFS25.job](mesoscale-air-sea-coupling/IFS-FESOM/remap_yrmth_IFStco399_IFS25.job)

```bash
   sbatch remap_yrmth_IFStco399_IFS25.job 'OSTIA_c_LR30_a_LR30' 'wind_divcurl' 'sd'
   sbatch remap_yrmth_IFStco399_IFS25.job 'OSTIA_c_LR30_a_LR30' 'wind_divcurl' 'svo'
   sbatch remap_yrmth_IFStco399_IFS25.job 'OSTIA_c_LR30_a_LR30' 'tau_divcurl' 'sd'
   sbatch remap_yrmth_IFStco399_IFS25.job 'OSTIA_c_LR30_a_LR30' 'tau_divcurl' 'svo'
```

### 3) Perform 30-day running mean on 0.25deg grid files
Use [30dayrunmean_ifsfesom_IFS25.job](mesoscale-air-sea-coupling/IFS-FESOM/30dayrunmean_ifsfesom_IFS25.job)

```bash
declare -a varnamearr=("wspd" "sst")

for varname in "${varnamearr[@]}"
do
	sbatch 30dayrunmean_ifsfesom_IFS25.job ${varname}
done
```

### 4) Spatially high-pass 30-day running mean
Use [gcmfilt_30dayrunmean_yrly_ifsfesom.py](mesoscale-air-sea-coupling/IFS-FESOM/gcmfilt_30dayrunmean_yrly_ifsfesom.py) and [exec_gcmfilt_30dayrunmean_ifsfesom.job](mesoscale-air-sea-coupling/IFS-FESOM/exec_gcmfilt_30dayrunmean_ifsfesom.job)

```bash
declare -a varnamearr=("wspd" "sst")

for varname in "${varnamearr[@]}"
do
   for yr in $(seq 1950 1970); 
   do 
      sbatch exec_gcmfilt_30dayrunmean_ifsfesom.job ${varname} ${yr}; 
   done
done
```

### 5) Compute coupling coefficients 



