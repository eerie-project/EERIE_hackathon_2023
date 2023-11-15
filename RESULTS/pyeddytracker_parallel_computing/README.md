# Testing sensitivity of py eddy tracker by taking advantage of parallel computing 
(Arjun Kumar November 2023)

This folder contains 4 jupyter notebooks which I used to test the sensitivity of the py eddy tracker to two parameters: 1) the cutoff wavelength for the high pass filter and 2) the shape error. The main result is that the choice of parameters used for the py eddy tracker have a non-negligible effect on the average eddy radius and speed. 

### Contents:

- Notebooks
- Parallel computing
- Data used
- Python environment


## Notebooks:

All notebooks are adapted from the notebooks made available via Github for the EERIE hackathon  (EERIE_hackathon_2023/ICON/ICON-O). Need to run identifying_eddies first, then tracking_eddies and then global_stats_tracked_eddies.

* 1. identifying_eddies.ipynb
    - Eddies are identified with py eddy tracker using sea surface height
    - Run py eddy tracker over 6-year dataset for wavelength of 200 and 700 km and shape error of 30 and 70% (2 params x 2 values = tracker run 4 times)
    - Data written out to netCDF files
 
* 2. tracking_eddies.ipynb
    - Identified eddies are stitched together to form tracks
    - Loop over different combinations of wavelength and shape-error parameters
    - Tracks written out to netCDF files
    
* 3. global_stats_tracked_eddies.ipynb
    - Read in eddy tracks derived for 4 parameter-combinations
    - Create global maps of anti-cyclonic and cyclonic eddies
    - Create zonally-average plot of eddy-average speed and radius

* 4. highpassfilter_otherfields.ipynb
    - Aplpy high pass filter on other fields (temperature in this case)
    - Not necessary for to reproduce results, but demonstrates how code can be sped up with parallel computing


## Parallel computing: 

I use lazy function from dask to run py edder tracker for multiple time steps simulataneously. I use SLURMCluster from dask_jobqueue to get the resources and actually do the computation. Examples of the dask lazy function can be found at (https://examples.dask.org/applications/embarrassingly-parallel.html). For SLURMCluster I followed documentation from dkrz available at (https://docs.dkrz.de/blog/2020/dask_jobqueue.html)

## Data used:
    - 6 years of ICON ocean data interpolated onto the IFS grid (0.25 x 0.25 degrees)
    - Data located on levante at /work/bm1344/k203123/reg25/erc1011/
    
## Python environment:

Setting up the environment to run the py eddy tracker was the most tedious part and took the better part of a day for most people at the hackathon (me included). Setting up the environment would not have been possible without the dkrz team. What worked for me in the end was the following: 

% mamba env create -f environment.yaml

The environment.yaml file looks like this:  
    
name: pyeddyenv
channels:
  - conda-forge
dependencies:
  - python=3.10
  - ipykernel
  - ca-certificates
  - openssl
  - xarray
  - matplotlib
    #  - opencv-python
  - pint
  - polygon3
  - pyyaml
  - requests
  - scipy
  - zarr
  - netCDF4
  - numpy
  - numba
  - pip
  - pip:
    - flake8
    - pytest
    - pytest-cov
    - git+https://github.com/AntSimi/py-eddy-tracker
    

