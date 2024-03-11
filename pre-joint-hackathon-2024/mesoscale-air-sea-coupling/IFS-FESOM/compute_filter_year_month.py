# Script to low-pass filter a specific month of the 30-day rolling mean daily means of IFS AMIP output
# Matthias Aengenheyster, March 2024

# Functions copied over from Matthias Aengenheyster

import xarray as xr
import numpy as np
from dask.diagnostics import ProgressBar

import sys
sys.path.insert(0, r'/home/b/b382473')
import geostats as gs
import filtering as fl

import filter_functions as ff


import argparse
parser = argparse.ArgumentParser()
# parser.add_argument('filename')
parser.add_argument('varname')
parser.add_argument('year')
parser.add_argument('month')

args = parser.parse_args()
print(args)
# filename_in = args.filename
varname = args.varname
year = int(args.year)
month = int(args.month)


if varname == 'sst':
    ds = xr.open_dataset('/work/bk1377/b382473/reg25/ifsamip/OSTIA/mean_30d/sst_30d_%.4i.nc' % year).sel(time='%.4i-%.2i' % (year,month))
    name = 'sst'
elif varname == 'speed':
    ds = xr.open_dataset('/work/bk1377/b382473/reg25/ifsamip/OSTIA/mean_30d/speed_30d_%.4i.nc' % year).sel(time='%.4i-%.2i' % (year,month))
    name = '10si'
elif varname == 'winddiv':
    ds = xr.open_dataset('/work/bk1377/b382473/reg25/ifsamip/OSTIA/mean_30d/winddiv_30d_%.4i.nc' % year).sel(time='%.4i-%.2i' % (year,month))
    name = 'winddiv'
elif varname == 'downT':
    ds = xr.open_dataset('/work/bk1377/b382473/reg25/ifsamip/OSTIA/mean_30d/downT_30d_%.4i.nc' % year).sel(time='%.4i-%.2i' % (year,month))
    name = 'downT'
else:
    sys.exit('varname %s is not defined' % varname)

bnds = dict(lat=slice(-85,85))

# sub-select data
# print('TESTING: ONLY 2 TIMESTEPS')
# ds = ds.isel(time=slice(40,42))

LR_gl = xr.open_dataarray('/work/mh0256/m300466/ifsfesomgrids/RossbyRadius_filtered_1degree_r1440x721.nc').sel(bnds)
#is the Rossby radius regridded to the 1/4 degree grid from PHC3.0 climatology

# factor 30, (300-1500 km)
LRfactor = 30
LRmax = 1500

# small: factor 5 (50-250 km)
# LRfactor = 5
# LRmax = 250
# large: factor 90 (900-4500 km)
# LRfactor = 90
# LRmax = 4500
# medium: factor 12 (120-600 km)
# LRfactor = 12
# LRmax = 600

LRmin = 10 # set minimum length to 10
LR_min_max30_gl = xr.where(LR_gl<LRmin,LRmin,LR_gl)
LR_min_max30_gl = xr.where(LR_min_max30_gl*LRfactor>LRmax,LRmax,LR_min_max30_gl*LRfactor) # 30 x rossby radius, capped at 1500 km


print('Get field')
# Load data from xarray into netcdf4 type
# ds_subset = ds_subset1[[varname]].sel(bnds).isel(time=tt)

# da_ssh.time.encoding.pop("_FillValue",None)
da_field = ff.get_da_field(
    # sst_30d.to_dataset().isel(time=slice(300,302)), 
    # sst_30d.to_dataset().isel(time=slice(30,33)), 
    ds,
    name, 
    bnds
)

print('Get filter')
filter_cpu = ff.setup_filter(
    # sst_30d.to_dataset().isel(time=slice(30,33)), 
    ds,
    name,
    bnds
)

print('Get filtered data')
fields_filtered = ff.filter_data(filter_cpu, da_field, load=False)


print('Compute filtering')
with ProgressBar():
    fields_filtered.load()

outfile = '/work/bk1377/b382473/reg25/ifsamip/OSTIA/mean_30d_filtered/%s_30d_%.4i-%.2i.nc' % (varname,year,month)
print('Save results to %s' % outfile)
fields_filtered.to_netcdf(
    outfile
)

print('Done')