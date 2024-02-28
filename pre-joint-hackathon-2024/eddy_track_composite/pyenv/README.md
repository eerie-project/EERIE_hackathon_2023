# Python environment for py-eddy-tracker
We learnt from the EERIE hackathon in Nov. 2023, that it takes quite some effort of to setup the python environment for usage with py-eddy-tracker. Instructions on how to [build your own environment](#build-your-own-python-environment) or [use someone else's working environment](#using-someone-elses-working-python-environment) can be found [here](https://pad.gwdg.de/s/UPtvMmBFw).  A working [conda environment list](eddyenv_dap_v1.txt) on Levante is also provided in case program versions cause some issues. 


## Build your own python environment
Here, we provide instructions to build your own python environment and get py-eddy-tracker and GCM filters to work with ICON, IFS/FESOM and IFS-AMIP data. 

```bash
module purge
source /work/mh0256/m300466/miniconda3/bin/activate
mamba create -n eddyenv_dap_v1 python=3.10 ipykernel
conda activate eddyenv_dap_v1
conda env list
python -m ipykernel install --user --name eddyenv_dap_v1  --display-name="eddyenv_dap_v1"
conda deactivate
```

```bash
conda env list
source activate /work/mh0256/m300466/miniconda3/envs/eddyenv_dap_v1
mamba install gcm_filters xgcm
mamba install cdo nco dask dask-jobqueue xarray pandas cartopy matplotlib numpy netcdf4 zarr healpix jupyter seaborn cmocean iris
mamba install intake intake-esm intake-xarray python-cdo scipy scikit-learn jupyterlab spectrum easydev tqdm distributed aiohttp requests fastparquet
mamba install cfunits cdsapi eccodes ecmwf-api-client ecflow python-eccodes cfgrib 
mamba install pyfesom2

python -m pip install --upgrade pip
module load git
python3.10 -m pip install git+https://gitlab.dkrz.de/m300602/pyicon.git
python3.10 -m pip install pyeddytracker
    #xarray 2024.2.0 requires numpy>=1.23, but you have numpy 1.22.4 which is incompatible.
    
pip show numpy
pip install numpy==1.26.4
```

#### Getting py-eddy-tracker with xarray
In order to use py-eddy-tracker with xarray, you'll need to replace grid.py with a modified grid.py provided by Aaron Wienkers. Details can be found on https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_xarray_dask_parallel

Go to folder where grid.py in this python env is located. 
```bash
cd /work/mh0256/m300466/miniconda3/envs/eddyenv_dap_v1/lib/python3.10/site-packages/py_eddy_tracker/dataset/
cp -p grid.py grid.py.orig
# Replace grid.py with the one from github https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/pyeddytracker_xarray_dask_parallel/grid.py
```

Go to py-eddy-tracker directory (exactly where you did « git clone git@github.com:AntSimi/py-eddy-tracker.git »), and into the subdirectory where grid.py is located. 

```bash
cd /work/mh0256/m300466/pyeddytracker/src/py_eddy_tracker/dataset
cp -p grid.py grid.py.orig
# Replace grid.py with the one from github https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/pyeddytracker_xarray_dask_parallel/grid.py
# Or do
cp -p /work/mh0256/m300466/miniconda3/envs/eddyenv_dap_v1/lib/python3.10/site-packages/py_eddy_tracker/dataset/grid.py /work/mh0256/m300466/pyeddytracker/src/py_eddy_tracker/dataset/grid.py 
```

Go to py-eddy-tracker directory (exactly where you did « git clone git@github.com:AntSimi/py-eddy-tracker.git »)
```bash
cd /work/mh0256/m300466/pyeddytracker
python -m pip install --force-reinstall .
pip show matplotlib
pip install matplotlib==3.7.1
```

## Using someone else's working python environment
Go to where your folder that points to where `kernel.json` files are collected and used for visibility as an environment on jupyterhub. This may be in your $HOME directory, or for some of us, it is in ~/.local/share/jupyter/kernels

Perform a symbolic link to where this environment resides from that folder.

```
ln -s /home/m/m300466/.local/share/jupyter/kernels/eddyenv_dap_v1
```
