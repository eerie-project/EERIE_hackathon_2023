#!/bin/python
# ©2024 Matthias Aengenheyster (ECMWF) and Dian Putrasahan (MPIM)

# Use GCM Gaussian filter to filter eddies out
# Use intake to read in data (0.25deg data), then apply filter on daily fields. To run them per year each time, per model, per variable. Takes ~105mins per script. 

import os, sys
varname=sys.argv[1]
yr=sys.argv[2]

#varname = 'ssh'
yyyy=int(yr)

bnds = dict(lat=slice(-85,85))
wavelength='30R'

expid='ifs-fesom'
daterng='19500101-19701231'

# Directories
#varname='wspd'
indir='/work/bm1344/m300466/reg25/ifsfesom/30dayrunmean/'+varname+'/'
filtdir=indir+'Gaussian/'
smdatadir=filtdir+'sm'+wavelength+'/'
if not os.path.exists(filtdir):
        os.makedirs(filtdir)
if not os.path.exists(smdatadir):
        os.makedirs(smdatadir)


import gcm_filters
import numpy as np
import xarray as xr
import pandas as pd
import intake

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cmocean.cm as cmo
import seaborn as sns

import time as T
from datetime import datetime
from dask.diagnostics import ProgressBar

# Functions copied over from Matthias Aengenheyster
sys.path.insert(0, r'/home/m/m300466/pyfuncs/MA')
import geostats as gs
import filtering as fl

import warnings
warnings.filterwarnings("ignore")


#ifs-fesom_wspd_19500101-19701231_IFS25_30dayrmn.nc
filein=indir+expid+'_'+varname+'_'+daterng+'_IFS25_30dayrmn.nc'
ds1=xr.open_dataset(filein)

timesel = dict(time=slice(str(yyyy)+'-01-01',str(yyyy)+'-12-31'))
ds_subset1 = ds1.sel(timesel)
datearr = np.array([pd.Timestamp(t).to_pydatetime() for t in ds_subset1.time.values])

print('High pass filter daily '+varname+' for year='+str(datearr[0].year)+'-'+str(datearr[-1].year))

#############################################################
def get_area(da,mask=False):
    print('Computing grid-box area')
    import iris.analysis as ia
    if 'time' in da.dims:
        da = da.isel(time=0).drop('time')
    d = da.to_iris()
    d.coord('longitude').guess_bounds()
    d.coord('latitude').guess_bounds()

    area_weights = ia.cartography.area_weights(d)
    area = xr.ones_like(da) * area_weights
    if mask:
        area = area.where(~np.isnan(da))
    area = area.rename('area').load()
    area.attrs['long_name'] = 'grid_box_area'
    area.attrs['units'] = 'm^2'
    return area

def get_da_field(ds, varname, bnds):
    ds = ds[[varname]].sel(bnds)
    # ds = fl.define_grid_metrics(ds)
    
    # wetmask_gl = xr.where(np.isnan(ds[varname].isel(time=0)),0,1).load()
    wetmask_gl = xr.where(np.isnan(ds[varname]),0,1).load()
    # wetmask_gl = xr.where(np.isnan(ds[varname]),0,1).load()
    # Set mask to zero at southern (irrelevant - Antarctica) and northern (Arctic) boundary to prevent "outflow" of information
    wetmask_gl[0,:] = 0
    wetmask_gl[-1,:] = 0
    wet_mask = wetmask_gl.drop('time').chunk({'lat': len(ds.lat), 'lon': len(ds.lon)})  # 1 chunk

    da_field = ds[varname].where(wet_mask)
    da_field = da_field.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)})  # 1 chunk
    return da_field.to_dataset()
    
def setup_filter(ds, varname, bnds):
    '''
    Setup filter based on <varname> in ds, limited to geographical bnds
    Using a Gaussian filter with varying spatial scales (factor * Rossby radius)
    '''
    ds = ds[[varname]].sel(bnds)
    ds = fl.define_grid_metrics(ds)

    dxw = ds.dxc.rename({'lon_g':'lon'}).assign_coords(lon=ds.lon).rename('dxw')#.sel(lat=slice(-60,60))
    dyw = ds.dyg.rename({'lon_g':'lon'}).assign_coords(lon=ds.lon).rename('dyw')#.sel(lat=slice(-60,60))
    dxs = ds.dxg.rename({'lat_g':'lat'}).assign_coords(lat=ds.lat).rename('dxs')#.sel(lat=slice(-60,60))
    dys = ds.dyc.rename({'lat_g':'lat'}).assign_coords(lat=ds.lat).rename('dys')#.sel(lat=slice(-60,60))
    # grid spacings, between cell centers (_c) and cell boundaries (_g), based on the MITgcm terminology
    # dxw = x-spacing centered at western cell edge
    # dyw = y-spacing centered at western cell edge
    # dxs = x-spacing centered at southern cell edge
    # dys = y-spacing centered at southern cell edge

    dx_min = min(
        dxw.min(),
        dyw.min(),
        dxs.min(),
        dys.min()).values
    
    area = gs.get_area(ds[varname])

    wetmask_gl = xr.where(np.isnan(ds[varname].isel(time=0)),0,1).load()
    # wetmask_gl = xr.where(np.isnan(ds[varname]),0,1).load()
    # Set mask to zero at southern (irrelevant - Antarctica) and northern (Arctic) boundary to prevent "outflow" of information
    wetmask_gl[0,:] = 0
    wetmask_gl[-1,:] = 0
    
    wet_mask = wetmask_gl.drop('time').chunk({'lat': len(ds.lat), 'lon': len(ds.lon)})  # 1 chunk
    area = area.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)})  # 1 chunk
    dxw = dxw.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)}) # 1 chunk
    dyw = dyw.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)}) # 1 chunk
    dxs = dxs.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)}) # 1 chunk
    dys = dys.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)}) # 1 chunk

    # da_field = ds[varname].where(wet_mask)
    # da_field = da_field.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)})  # 1 chunk

    # https://gcm-filters.readthedocs.io/en/latest/examples/example_filter_types.html#preparing-the-grid-input-variables  
    # ======================
    # ROSSBY-RADIUS BASED FILTERING
    # ======================
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
    #LRfactor, LRmax, LRmin: multiple of Rossby radius, and maximum/minimum cutoffs
    #NB: minimum is done before the  factor, but the maximum is done after
    # Largest range of LR_min_max30_gl = (LRfactor * LRmin , LRmax) 

    # L_max = LR.max().values
    L_max_gl = LR_min_max30_gl.max().values
    filter_scale = L_max_gl
    kappa_min_max30_gl = LR_min_max30_gl**2 / L_max_gl**2
    kappa_min_max30_gl = kappa_min_max30_gl.chunk({'lat': len(ds.lat), 'lon': len(ds.lon)}) # 1 chunk

    kappa_w = kappa_min_max30_gl.copy()
    kappa_s = kappa_min_max30_gl.copy()
    # kappa_w and kappa_s are the diffusivity in x and y, that needs a lengthscale for scaling.
    # For a constant lengthscale, they are both =1, and one can change them separately to have different filter lengths per direction
    # We should keep kappa to between 0 and 1. 
    
    
    specs = dict(
        filter_scale=filter_scale * 1e3, #from km to m
        dx_min=dx_min,
        filter_shape=gcm_filters.FilterShape.GAUSSIAN,
        grid_type=gcm_filters.GridType.IRREGULAR_WITH_LAND,
    )

    filter_cpu = gcm_filters.Filter(grid_vars={
        'area': area,
        'wet_mask': wet_mask,
        'dxw': dxw,
        'dyw': dyw,
        'dxs': dxs,
        'dys': dys,
        'kappa_w': kappa_w,
        'kappa_s': kappa_s,
        }, **specs)
    print('Filter: ',filter_cpu)
    
    return filter_cpu

def filter_data(filter_obj, da_field, load=False):
    fields_filtered = filter_obj.apply(
        da_field, dims=['lat', 'lon'])
        # ds, dims=['lon'])
    if load:
        with ProgressBar():
            fields_filtered.load()
    return fields_filtered


# Parallel function wrapper to the for-loop
# Does NOT work!!!
def delayed_Gfilter_and_save(date, tt):
    
    # Load data from xarray into netcdf4 type
    ds_subset = ds_subset1[[varname]].sel(bnds).isel(time=tt)
    # da_ssh.time.encoding.pop("_FillValue",None)
    da_field=get_da_field(ds_subset, varname, bnds)

    print('High pass filter of '+varname+' for '+date.strftime('%Y%m%d'))
    fields_filtered=filter_data1(filter_cpu, da_field, load=False)
    
    if varname=='to' or varname=='so' or varname=='rho':
        zidx=1
        foutname=smdatadir+'/'+varname+'_'+str(zidx)+'_'+date.strftime('%Y%m%d')+'_sm'+wavelength+'.nc'
    else:
        foutname=smdatadir+'/'+varname+'_'+date.strftime('%Y%m%d')+'_sm'+wavelength+'.nc'

    fields_filtered.to_netcdf(path=foutname)


def gaussian_gcm_filter(ds_subset1,varname,bnds,datearr,tt,smdatadir,wavelength,filter_cpu): 
    date = datearr[tt]
    # Load data from xarray into netcdf4 type
    ds_subset = ds_subset1[[varname]].sel(bnds).isel(time=tt)
    # da_ssh.time.encoding.pop("_FillValue",None)
    da_field=get_da_field(ds_subset, varname, bnds)

    print('High pass filter of '+varname+' for '+date.strftime('%Y%m%d'))
    fields_filtered=filter_data(filter_cpu, da_field, load=False)

    if varname=='to' or varname=='so' or varname=='rho':
        zidx=1
        foutname=smdatadir+'/'+varname+'_'+str(zidx)+'_'+date.strftime('%Y%m%d')+'_sm'+wavelength+'.nc'
    else:
        foutname=smdatadir+'/'+varname+'_'+date.strftime('%Y%m%d')+'_sm'+wavelength+'.nc'

    fields_filtered.to_netcdf(path=foutname)
    del ds_subset
    del da_field
    del fields_filtered
    del foutname
########################################################################

# filter_cpu=setup_filter(ds_subset1, varname, bnds)
dsifs=xr.open_dataset('/work/mh0256/m300466/ifsfesomgrids/ssh_1950_IFS25.nc')
filter_cpu=setup_filter(dsifs.sel(time=slice('1950-01-01','1950-01-03')),'ssh',dict(lat=slice(-85,85)))
#dsifs=xr.open_dataset(filein)
#filter_cpu=setup_filter(dsifs.sel(time=slice('1950-01-01','1950-01-03')),varname,dict(lat=slice(-85,85)))

for tt in range(0,len(datearr)):
    gaussian_gcm_filter(ds_subset1,varname,bnds,datearr,tt,smdatadir,wavelength,filter_cpu)
