# Eddy tracking and compositing

We use [py-eddy-tracker](https://py-eddy-tracker.readthedocs.io/en/stable/index.html) to identify and track eddies, then build composites for some collection of eddies. 

**Table of contents**:
1) [Python environment for py-eddy-tracker](#python-environment-for-py-eddy-tracker)
2) [Example notebooks with py-eddy-tracker on EERIE data](#example-notebooks-with-py-eddy-tracker-on-eerie-data)
3) [Parameter choices for py-eddy-tracker](#parameter-choices-for-py-eddy-tracker)
4) [Eddy compositing in joint hackathon (2024)](#joint-hackathon-mar-2024) 

## Python environment for py-eddy-tracker
We learnt from the EERIE hackathon in Nov. 2023, that it takes quite some effort of to setup the python environment for usage with py-eddy-tracker. Here are [3 options on how to get a working environment](pyenv/README.md) for py-eddy-tracker with xarray and dask. 
   1) Instructions on how to build your own environment
   2) Use someone else's working environment
   3) Use a pre-made environment that can be loaded via 'module load'. 
   
A working [conda environment list](pyenv/eddyenv_dap_v1.txt) on Levante is also provided in case program versions cause some issues. 


## Example notebooks with py-eddy-tracker on EERIE data and NextGEMS (HAMOCC)
As an example, we use model SSH fields (0.25deg because AVISO uses the same resolution) to identify eddies. From EERIE hackathon in Nov. 2023, here are some example notebooks. 
- Basic setup to identify, track and composite eddies using ICON output from known paths (Dian Putrasahan). Here's how to:
    1) [identify and track eddies](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-IDtrackcompeddy-daily.ipynb) 
    2) [build eddy composites](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-eddycompositeotherfields-daily.ipynb) from various 0.25deg fields
    3) [plot composites](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-plot-eddycompositesalongtrack-dm.ipynb)
- Computation time was getting long. Here's how to run the code in [parallel and perform parameter sensitivity experiments](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_parallel_computing) (Arjun Kumar).
- Modified way to [parallelise eddy identification code](ICON/identify_fast.py) and [compositing with higher res data](ICON/composite_tracks.py) than 0.25deg (Moritz Epke) 
- py-eddy-tracker reads in netcdf file but does not know how to use xarray. This issue was dealt with and we can now [use xarray with py-eddy-tracker + some parallelisation](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_xarray_dask_parallel) (Aaron Wienkers). Furthermore, the code uses dask for parallelisation. 
- Now, feeding py-eddy-tracker with xarray obtained from reading in with intake catalog is possible. So here's an example of how to [identify and track eddies with IFS/FESOM output from intake catalog](IFS-FESOM/IDtrackeddy-daily-intake_IFSFESOM.ipynb) with xarray and some parallelisation (Aaron Wienkers and Dian Putrasahan). 
- Applying [py-eddy-tracker on HAMOCC](HAMOCC/README.md) fields (Johann Jungclaus and Dian Putrasahan)



## Parameter choices for py-eddy-tracker
Here are the parameter choices used for AVISO, following [recommendation from py-eddy-tracker author](https://github.com/AntSimi/py-eddy-tracker/discussions/198) and used by Malcolm Roberts for HadGEM output. 

| Parameter (identification) | Value | Description |
| ------------------------------- | ------------ | --------------------------- |
| wavelength (Bessel filter) | 700 km | spatial cutoff for high pass filter in km |
| wavelength_order (filter) | 1 | |
| step_ht | 0.002 m | intervals to search for closed contours (m) |
| shape error | 70 | Error max (%) between ratio of circle fit and contour |
| nb_step_to_be_mle | 0 (default 2?) | don't allow micro relief in an eddy, used for computing amplitude | 
| sampling (affects storage) | Not set (default 50) | affects storage, using 20-30 is acceptable |
| pixel_limit | Not set (default None) | Min and max pixel count for valid contour (5, 2000)  |
| presampling_multiplier | Not set (default 10) | |
| sampling_method | Not set (default visvalingam) | |
| precision | Not set (default None) | |


| Parameter (tracking) | Value |
| ------------------------ | ------------ |
| cmin | 0.05 |
| virtual | 4 |

## Spatial filtering prior to eddy compositing
When building eddy composites, we'll typically perform a spatial filtering to obtain the anomalous fields associated with the spatial scale of the eddy. There are multiple spatial filters to choose from. Here, we show 3 different ways to perform spatial filtering. 
1. [Weighted area-average smoothing](../mesoscale-air-sea-coupling/Spatial_Filters/README.md#weighted-area-average-smoothing-using-cdo) using `cdo -smooth` operator. 
2. [Bessel filter](../mesoscale-air-sea-coupling/Spatial_Filters/README.md#bessel-filter) using a function from py-eddy-tracker. 
3. [Gaussian filter](../mesoscale-air-sea-coupling/Spatial_Filters/README.md#gaussian-filter) using a function from GCM filters.

## Joint hackathon (Mar 2024) 
For the joint hackathon (Mar 2024), in the breakout session on eddy composites, we may tackle a few subtopics relating to eddy composites including:
1) 3D eddy composities (T, S, BGC)
2) scale composite with eddy radius
3) rotation of eddy to direction of background wind or SST gradients
4) bring your own topic ......


