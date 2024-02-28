# Spatial Filters
We perform spatial filtering to tease apart the spatial scale dependency of air-sea coupling coefficients. Here, we provide examples of using 3 different filtering techniques. 

1. [Weighted area-average smoothing](#weighted-area-average-smoothing-using-cdo) using `cdo -smooth` operator. 
   - [Bonus: spatial filtering on HEALpix data](#bonus-spatial-filtering-on-healpix-data).
2. [Bessel filter](#bessel-filter) using a function from py-eddy-tracker. 
3. [Gaussian filter](#gaussian-filter) using a function from GCM filters.


## Weighted area-average smoothing using cdo
Area-averaging over a circle of radius (e.g. 3deg), with a cone-shaped weighting where weight=1 at the centre and weight=0.2 at the radius edge. 
Since data is catalogued using intake, we obtain path of data for use with cdo using `query_yaml.py`. A magic script created by Florian Ziemen for those who'd still like to use cdo shell environment for parts of their analysis. 

```bash
module use /work/k20200/k202134/hsm-tools/outtake/module
module load hsm-tools/unstable

varname='sst'
varfilelist=$(query_yaml.py -c https://raw.githubusercontent.com/eerie-project/intake_catalogues/main/eerie.yaml dkrz disk model-output ifs-fesom2-sr eerie-control-1950 ocean gr025 daily --var ${varname} --uri --cdo)
echo ${varfilelist}

#Let's perform a smoothing over 3deg
outidr=/scratch/m/m300466/eerie-control-1950/gr025/ifs-fesom2-sr/sst/CDOsmooth/sm3deg
cdo -P 64 -smooth,radius=3deg,weight0=1.0,weightR=0.2,maxpoints=5000 -select,name=${varname},year=1950,month=2 ${varfilelist} ${outdir}/${varname}_195002_sm3deg.nc

## Subtract full - smooth = high pass
cdo -sub -select,name=${varname},year=1950,month=2 [ ${varfilelist} ] ${outdir}/${varname}_195002_sm3deg.nc ${outdir}/${varname}_195002_hp3deg.nc

```

**Other example queries:** 

`varfilelist=$(query_yaml.py -c https://raw.githubusercontent.com/eerie-project/intake_catalogues/main/eerie.yaml dkrz disk model-output ifs-fesom2-sr eerie-control-1950 atmos gr025 daily_2d --var 2t --uri --cdo)`

Please refer to [EERIE data viewer](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html) for the data tree structure and variables available.

### Bonus spatial filtering on HEALpix data
One of the strength of CDO is the ability to also perform spatial filtering on some unstructured grid, HEALpix included. 

Basic notes on HEALpix:
| zoom index (ICON) | nside index (IFS/FESOM) |  resolution in degrees | resolution in km |
| --------------- | --------------- | --------------- | --------------- |
| zoom 0 | nside 1 | 59 deg | 6144 km | 
| zoom 1 | nside 2 | 29 deg | 3072 km |
| zoom 2 | nside 4 | 15 deg | 1536 km |
| zoom 3 | nside 8 | 7.3 deg | 768 km |
| zoom 4 | nside 16 | 3.7 deg | 384 km |
| zoom 5 | nside 32 | 1.8 deg | 192 km |
| zoom 6 | nside 64 | 0.92 deg | 96 km |
| zoom 7 | nside 128 | 0.46 deg | 48 km |
| zoom 8 | nside 256 | 0.23 deg | 24 km |
| zoom 9 | nside 512 | 0.11 deg | 12 km |
| zoom 10 | nside 1024 | 0.057 deg | 6 km |

```bash
module use /work/k20200/k202134/hsm-tools/outtake/module/
module add  hsm-tools/unstable

#Frequency output = time = [PT15M, PT30M, PT1H, PT3H, PT6H, P1D]
varname='tas'
varfilelist=$(query_yaml ICON ngc4005 -s time=P1D -s zoom=8 --var ${varname} --uri --cdo)

cdo -P 64 -smooth,radius=3deg,weight0=1.0,weightR=0.2,maxpoints=5000 -select,name=${varname},year=2020,month=2 ${varfilelist} ${outdir}/${varname}_zoom8_195002_sm3deg.nc
```


## Bessel filter
Using a function from py-eddy-tracker, a fixed spatial scale filter is used to smoothed the data. Here's an [example notebook](mesoscale-air-sea-coupling/Spatial_Filters/Bessel_filter_example.ipynb) of how to do this by Aaron Wienkers (ETHZ) and Dian Putrasahan (MPIM), Feb 2024. 

- Use a fixed 700km spatial filter (wavelength)
- Usage of xarray within py-eddy-tracker made possible by Aaron Wienkers, and consequently the use of dask. Much of this example is taken from [https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_xarray_dask_parallel](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_xarray_dask_parallel)
- Intake catalog of EERIE data done by Fabian Wachsmann
- Please use a python environment that works with py-eddy-tracker. [Here's how to setup one](https://pad.gwdg.de/s/UPtvMmBFw). 


## Gaussian filter
Using a function from GCM filters, a varying spatial scale filter of 30*R, where R=Rossby radius, is used to smoothed the data. Here's an [example notebook](mesoscale-air-sea-coupling/Spatial_Filters/Gaussian_filter_example.ipynb) of how to do this by Matthias Aengenheyster (ECMWF) and Dian Putrasahan (MPIM), Feb 2024.
- Use a variable 30*R (R=Rossby radius) spatial filter
- Perform filtering on 0.25deg data as GCM filters can only work on gridded data. Most functions provided by Matthias Aengenheyster and much of this example is taken from [https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/eddy_composites-short.ipynb](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/eddy_composites-short.ipynb)
- Intake catalog of EERIE data done by Fabian Wachsmann
- Please use a python environment that works with GCM filters. [Here's how to setup one](https://pad.gwdg.de/s/UPtvMmBFw), but please skip the part on py-eddy-tracker if you only want an environment for GCM filters.  

Additional files needed/made prior to running script. 
- Some functions from Matthias to be copied over. 

    `cp -p /home/b/b382473/*.py ~/pyfuncs/MA`
- These files are used once each time we run this script. Since we reuse them so much, let's make them fixed files to be hard-coded. 

    `cp -p /home/b/b382473/LR_filtered_1degree_r1440x721.nc /work/mh0256/m300466/ifsfesomgrids/RossbyRadius_filtered_1degree_r1440x721.nc`

     `cp -p /work/bm1344/a270228/EERIE_Hackathon/IFS-FESOM_CONTROL-1950/tco1279-NG5/1950/FESOM/025/daily/ssh_1950_19500101-19500131_025.nc /work/mh0256/m300466/ifsfesomgrids/ssh_1950_IFS25.nc`


