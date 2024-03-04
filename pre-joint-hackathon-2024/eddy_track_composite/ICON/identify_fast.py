# %%
import sys
import glob, os
import pyicon as pyic
import smt_modules.all_funcs as eva
from smt_modules.icon_smt_levels import dzw, dzt, depthc, depthi
import smt_modules.tools as tools
import smt_modules.init_slurm_cluster as scluster 
sys.path.insert(0, '../')
import funcs as fu

import pandas as pd
import netCDF4 as nc
import xarray as xr    
import numpy as np
import datetime          #https://docs.python.org/3/library/datetime.html
from datetime import datetime, timedelta
from netCDF4 import Dataset

from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
ccrs_proj = ccrs.PlateCarree()

from importlib import reload
import dask
import math 

from py_eddy_tracker.dataset.grid import RegularGridDataset


# %% get cluster
reload(scluster)

client, cluster = scluster.init_dask_slurm_cluster(walltime='01:00:00', wait=False)
cluster
client

# %%
varname = 'zos'

# datadir = '/work/mh0033/m300878/crop_interpolate/smtwv/ssh/03deg/smtwv0007_ssh'
datadir = '/work/mh0033/m300878/crop_interpolate/smtwv/ssh/03deg/smtwv0009_ssh_fine_cropped'

# ds = xr.open_dataset(datadir+'.nc')
# ds_KE = xr.open_dataset('/work/mh0033/m300878/crop_interpolate/smtwv/ssh/002deg/exp7_KE_100m_fine.nc')
# ds = ds.sel(time=slice(ds_KE.time[0],ds_KE.time[-1]))#use same time interval as KE
# ds.to_netcdf(datadir+'_cropped.nc')

# datadir = '/work/mh0033/m300878/crop_interpolate/smtwv/ssh/002deg/smtwv0007_ssh_02'

# root_dir = '/scratch/m/m300878/agulhas_eddies/exp9/'
root_dir = '/work/mh0033/m300878/eddy_tracks/agulhas_eddies/exp7/'

# %%
if False:
    ds            = xr.open_dataset(datadir+'.nc')
    mask_land     = eva.load_smt_wave_land_mask()
    lon_reg       = [-15, 20]
    lat_reg       = [-36, -20]
    fpath_ckdtree = '/work/mh0033/m300602/icon/grids/smtwv_oce_2022/ckdtree/rectgrids/smtwv_oce_2022_res0.30_180W-180E_90S-90N.nc'
    mask_interp   = pyic.interp_to_rectgrid_xr(mask_land, fpath_ckdtree, lon_reg, lat_reg)
    ds_sel        = ds.where(( ds.lon > lon_reg[0]) & ( ds.lon < lon_reg[1]) & ( ds.lat > lat_reg[0]) & ( ds.lat < lat_reg[1]), drop=True)
    ds_masked     = ds_sel*mask_interp

    ds_masked.zos.attrs['units'] = 'm'
    ds_masked.to_netcdf(datadir+'_masked2.nc')

# %%
# datafiles = sorted(glob.glob(datadir+"*_masked2.nc"))
datafiles = sorted(glob.glob(datadir+".nc"))
ds        = xr.open_dataset(datafiles[0])
ds        = ds.isel(time=slice(2,ds.time.shape[0],2)) #use same time interval as KE
datearrs  = ds.time.values
datearrs  = pd.to_datetime(datearrs)


# %% Computation
reload(fu)

for wavelength in [700]:
    for shape_error in [25]:
        print('wavelength, shape_error = ', wavelength, shape_error)
        print('year = ', datearrs.size)
        ntsteps_per_loop = 51
        ntsteps          = len(datearrs)
        tcounter         = np.zeros((ntsteps//ntsteps_per_loop)+2)
        tcounter[:-1]    = np.arange(0,(ntsteps//ntsteps_per_loop)+1)*ntsteps_per_loop
        tcounter[-1]     = ntsteps
        dask_steps       = math.ceil(ntsteps/ntsteps_per_loop)
        for x in range(dask_steps):
            print('tt vals = ', np.arange(tcounter[x],tcounter[x+1],1))
            lazy_results = []
            for tt in np.arange(tcounter[x],tcounter[x+1],1):
                tt = int(tt)
                lazy_result = dask.delayed(fu.detection_save_netcdf_output)(
                                                varfile     = datafiles[0], # dask.delayed
                                                varname     = varname,
                                                datearr     = datearrs[tt],
                                                tt          = int(tt),
                                                wavelength  = wavelength,
                                                shape_error = shape_error,
                                                root_dir    = root_dir)

                lazy_results.append(lazy_result)  

            futures = dask.compute(*lazy_results)
            results = dask.compute(*futures)




# %%#####################################################
# Test plot
reload(fu)
tt          = 2000
i           = 0
wavelength  = 700
shape_error = 25
a0, c0, g0 = fu.detection(datafiles[i],varname,datearrs[tt],tt,wavelength,shape_error)


# %%
ax = fu.start_axes(f"Eddies detected over SSH for t={tt}")
m = g0.display(ax, "zos", vmin=-0.15, vmax=0.15)
a0.display(
    ax,
    lw=0.75,
    label="Anticyclones in the filtered grid ({nb_obs} eddies)",
    ref=-25,
    color="green",
)
c0.display(
    ax,
    lw=0.75,
    label="Cyclones in the filtered grid ({nb_obs} eddies)",
    ref=-25,
    color="blue",
)
ax.legend()
plt.ylim(-36, -20)
plt.xlim(-15, 20)
fu.update_axes(ax, m)
# %%
