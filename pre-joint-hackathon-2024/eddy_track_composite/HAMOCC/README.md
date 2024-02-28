# Building eddy composites of BGC properties

Here, we apply py-eddy-tracker on HAMOCC fields and build eddy composites. This is our workflow.
   1) [Remap ssh and HAMOCC fields onto 0.25deg grid](#remap-ssh-and-hamocc-fields-onto-025deg-grid)
   2) [Perform eddy identification](#perform-eddy-identification)
   3) [High-pass all fields](#high-pass-all-fields)
   4) [Track the eddies](#track-the-eddies)
   5) [Composite HAMOCC fields along tracked eddies](#composite-hamocc-fields-along-tracked-eddies)
   6) [Quick plot of composites](#quick-plot-of-composites)

## Remap ssh and HAMOCC fields onto 0.25deg grid
To remap fields onto 0.25deg grid, use [ngc_72lev_HAM_prod_remap_dm_r2b9O_IFS25.job](eddy_track_composite/HAMOCC/ngc_72lev_HAM_prod_remap_dm_r2b9O_IFS25.job)

For sea surface height ('zos' in ICON) and other ocean variables:
```
sbatch ngc_72lev_HAM_prod_remap_dm_r2b9O_IFS25.job zos

#ocean variables
declare -a varnamearr=("to" "so" "mlotst" "Wind_Speed_10m" "sea_level_pressure" "atmos_fluxes_HeatFlux_Latent" "atmos_fluxes_HeatFlux_Sensible" "atmos_fluxes_FrshFlux_Precipitation")
for varname in "${varnamearr[@]}"; do sbatch ngc_72lev_HAM_prod_remap_dm_r2b9O_IFS25.job ${varname}; done
```

For HAMOCC variables:
```bash
declare -a varnamearr=("co2flux" "o2flux" "coex90" "pco2" "NPP" "dissic" "dissoc" "phyp" "phydiaz" "det" "talk" "no3" "po4" "o2" "delcar" "delsil" "calex90" "opex90" "wpoc" "remin" "hi")
for varname in "${varnamearr[@]}"; do sbatch ngc_72lev_HAM_prod_remap_dm_r2b9O_IFS25.job ${varname}; done
```

## Perform eddy identification
Eddies are identified and grouped into cyclonic and anticylonic eddies based on geostrophic relative vorticity. 

The example here uses manual parallelisation, in that we use the fact that eddy identification is independent of time, so we can do batch jobs on every year/month. Use the scripts [IDeddy_dm_hamocc.py](eddy_track_composite/HAMOCC/IDeddy_dm_hamocc.py) and [submit_IDeddy_dm-hamocc.job](eddy_track_composite/HAMOCC/submit_IDeddy_dm-hamocc.job)

```bash
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 1 ${dd}; done
for dd in $(seq 1 29); do sbatch submit_IDeddy_dm-hamocc.job 2020 2 ${dd}; done
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 3 ${dd}; done
for dd in $(seq 1 30); do sbatch submit_IDeddy_dm-hamocc.job 2020 4 ${dd}; done
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 5 ${dd}; done
for dd in $(seq 1 30); do sbatch submit_IDeddy_dm-hamocc.job 2020 6 ${dd}; done
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 7 ${dd}; done
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 8 ${dd}; done
for dd in $(seq 1 30); do sbatch submit_IDeddy_dm-hamocc.job 2020 9 ${dd}; done
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 10 ${dd}; done
for dd in $(seq 1 30); do sbatch submit_IDeddy_dm-hamocc.job 2020 11 ${dd}; done
for dd in $(seq 1 31); do sbatch submit_IDeddy_dm-hamocc.job 2020 12 ${dd}; done
```

## High-pass all fields
We use a 400km filter length scale with the Bessel filter that is a built-in function for py-eddy-tracker. We have examples where you can use [other filters](mesoscale-air-sea-coupling/Spatial_Filters/README.md) too. 

Here, we submit scripts for each year using [submit_highpass_dm_hamocc.job](eddy_track_composite/HAMOCC/submit_highpass_dm_hamocc.job), which in turn submits [highpass_dm_400km_hamocc.py](eddy_track_composite/HAMOCC/submits highpass_dm_400km_hamocc.py) script

For ssh and ocean fields:
```bash
sbatch submit_highpass_dm_hamocc.job zos 400
#ocean variables
declare -a varnamearr=("to" "so" "mlotst" "Wind_Speed_10m" "sea_level_pressure" "atmos_fluxes_HeatFlux_Latent" "atmos_fluxes_HeatFlux_Sensible" "atmos_fluxes_FrshFlux_Precipitation")
for varname in "${varnamearr[@]}"; do sbatch submit_highpass_dm_hamocc.job ${varname} 400; done
```

For HAMOCC fields:
```bash
declare -a varnamearr=("co2flux" "o2flux" "pco2" "coex90" "NPP" "dissic" "dissoc" "phyp" "phydiaz" "det" "talk" "no3" "po4" "o2" "delcar" "delsil" "calex90" "opex90" "wpoc" "remin" "hi")
for varname in "${varnamearr[@]}"; do sbatch submit_highpass_dm_hamocc.job ${varname} 400; done
```

## Track the eddies
Track the eddies with [eddytracking_dm_hamocc.py](eddy_track_composite/HAMOCC/eddytracking_dm_hamocc.py) and save data that allows continuation of tracking later on, with correspondance files. Additional grouping into files of untracked, tracks and short. 
```bash
python eddytracking_dm_hamocc.py
```

## Composite HAMOCC fields along tracked eddies
Use the ssh of tracked eddies, get track IDs where eddy last more than 60 days. Along the identified tracks, gather 2.5x2.5deg around eddy center and save ([eddy_fromfile_alongtrack_dm_hamocc.py](eddy_track_composite/HAMOCC/eddy_fromfile_alongtrack_dm_hamocc.py)). No normalisation by eddy radius yet. 

Submit this script for each region of interest using [compositefields_hamocc.job](eddy_track_composite/HAMOCC/compositefields_hamocc.job), once for cyclonic, once for anticyclonic eddies. 

Regions:
   - AR = Agulhas Rings (Agulhas leakage)
   - LC = Loop Current (Gulf of Mexcio)
   - NB = North Brazil (Eddy Boulevard)
   - SO = Southern ocean

```bash
declare -a rgnarr=("AR" "LC" "NB" "SO") 
for rgn in "${rgnarr[@]}"; do sbatch compositefields_hamocc.job zos cyclonic ${rgn}; done
for rgn in "${rgnarr[@]}"; do sbatch compositefields_hamocc.job zos anticyclonic ${rgn}; done
```

Using the identified trackes, gather 2.5x2.5deg around eddy center and save for all other fields of interest to build the composites ([othereddyfields_fromfile_alongtrack_dm_hamocc.py](eddy_track_composite/HAMOCC/othereddyfields_fromfile_alongtrack_dm_hamocc.py)). 

Then use [run_compositing.sh](eddy_track_composite/HAMOCC/run_compositing.sh) to run for each variable. Note that this script should run one variable at a time, otherwise it doesn't know how to append to file. 


## Quick plot of composites
Now time to reap what you sow, let's plot the composites with [plot-eddy-composites-alongtrack-hamocc.py](eddy_track_composite/HAMOCC/plot-eddy-composites-alongtrack-hamocc.py). Actually, not fully tested, so you'll have to work on this. =p

```bash
python plot-eddy-composites-alongtrack-hamocc.py ${varname}
```







