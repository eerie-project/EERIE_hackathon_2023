# Author: Moritz Epke
# Example of how to use the gcm_filters package to filter a gridded 2D field with "regular" and "irregular" grid spacing
# Here a solution to obtain gcm grid_vars: dxw, dyw, dxs, dys, area, kappa_w, kappa_s is presented: Solution adapted from Uchida 2023

# regular: evenly spaced grid (in meter)
# irregular: constant grid spacing in degrees, but irregular in meridional direction (in meter)
# dataset ds is gridded and has dims: time depthi lat lon
# wet_mask dims: lat lon; only contains ones and zeros

# !!! wet_mask must only contain ones and zeros !!!

# Note that an IRREGULAR in latitude and longitude is missing

# %%
import pyicon as pyic
import smt_modules.all_funcs as eva
import pandas as pd
import netCDF4 as nc
import xarray as xr    
import numpy as np

import gsw
import gcm_filters

# %%
t_space       = 1
savefig       = False
lat_reg       =  30,  40
lon_reg       = -78, -68
fpath_ckdtree = '/work/mh0033/m300602/icon/grids/smt/ckdtree/rectgrids/smt_res0.02_180W-180E_90S-90N.nc'
fig_path      = '/home/m/m300878/submesoscaletelescope/results/smt_natl/uchida_eval/'
path_2_data   = '/work/mh0033/m300878/smt/uchida_tseries/data/'

time   = 80
idepth = 10
# %%
mask_land_100 = eva.load_smt_land_mask(depthc=32)
mask_land_100 = pyic.interp_to_rectgrid_xr(mask_land_100, fpath_ckdtree=fpath_ckdtree, lon_reg=lon_reg, lat_reg=lat_reg)
mask_land_100 = mask_land_100.drop('depthc')
# %%
path_2_data = '/work/mh0033/m300878/smt/uchida_tseries/data/'
ds           = xr.open_dataarray(path_2_data + 'b.nc', chunks={'time': 1, 'depthi': 1})
ds           = ds * mask_land_100

# %% ###################################### Using REGULAR_WITH_LAND ######################################

def convert_degree_to_meter(lat):
    r        = 6371000
    latitude = np.linspace(0,90,90)
    delta    = 2*np.pi*r/360*np.cos(latitude/90* np.pi/2)
    return(delta[lat])

conversion_factor = convert_degree_to_meter(int(ds.lat.mean().data))
dx_min   = (ds.lat[1]-ds.lat[0]).data * conversion_factor
wet_mask = mask_land_100
wet_mask = wet_mask.fillna(0)
# %%
filter = gcm_filters.Filter(

    filter_scale=30000,

    dx_min=dx_min,

    filter_shape=gcm_filters.FilterShape.GAUSSIAN,

    grid_type=gcm_filters.GridType.REGULAR_WITH_LAND,

    grid_vars={'wet_mask': wet_mask}

)
filter
# %%
da_filtered = filter.apply(ds.isel(time=time), dims=['lat', 'lon'])
da_filtered.isel(depthi=idepth).plot()

# %% ################################### USING IRREGULAR_WITH_LAND ######################################
xx, yy = np.meshgrid(ds.lon, 
                     ds.lat
                    )
ny, nx = xx.shape
# computes spacing between two grid points depending on latitude in m; extrapolation to maintain same shape as b
dx = xr.DataArray(xr.DataArray(gsw.distance(xx, yy), dims=['lat','lon'],
                               coords={'lat':np.arange(ny),'lon':np.arange(.5,nx-1,1)}
                              ).interp(lon=np.arange(nx), method="linear",
                                       kwargs={"fill_value": "extrapolate"}).data,
                  dims=['lat','lon'], 
                  coords={'lat':ds.lat.data,'lon':ds.lon.data}
                 )
# computes spacing between two grid points depending on longitude in m; extrapolation to maintain same shape as b
# in this example constant since grid is only irregular in meridional direction
dy = xr.DataArray(xr.DataArray(gsw.distance(xx, yy, axis=0), dims=['lat','lon'],
                               coords={'lat':np.arange(.5,ny-1,1),'lon':np.arange(nx)}
                              ).interp(lat=np.arange(ny), method="linear",
                                       kwargs={"fill_value": "extrapolate"}).data,
                  dims=['lat','lon'], 
                  coords={'lat':ds.lat.data,'lon':ds.lon.data}
                 )
area = (dx * dy)
dx
# %%

# here no filtersize changes are applied; only the grid is irregular; Rossby Radisu dependent filter properties would go in here
kappa_w = xr.ones_like(wet_mask)
kappa_s = xr.ones_like(wet_mask)

dlat = ds.lat.diff('lat')[0]
dlon = ds.lon.diff('lon')[0]

dxw = xr.DataArray(dx.interp(lon=np.arange(dx.lon.min(),dx.lon.max()+dlon,dlon),
                             method='linear',
                             kwargs={"fill_value": "extrapolate"}).data,
                   dims=dx.dims, coords=dx.coords
                  ) # x-spacing centered at western cell edge

dyw = xr.DataArray(dy.interp(lon=np.arange(dy.lon.min(),dy.lon.max()+dlon,dlon),
                             method='linear',
                             kwargs={"fill_value": "extrapolate"}).data,
                   dims=dy.dims, coords=dy.coords
                  ) # y-spacing centered at western cell edge

dxs = xr.DataArray(dx.interp(lat=np.arange(dx.lat.min(),dx.lat.max()+dlat,dlat),
                             method='linear',
                             kwargs={"fill_value": "extrapolate"}).data,
                   dims=dx.dims, coords=dx.coords
                  ) # x-spacing centered at southern cell edge

dys = xr.DataArray(dy.interp(lat=np.arange(dy.lat.min(),dy.lat.max()+dlat,dlat),
                             method='linear',
                             kwargs={"fill_value": "extrapolate"}).data,
                   dims=dy.dims, coords=dy.coords
                  ) # y-spacing centered at southern cell edge
dxw

# %% in this example only latitudinal spacing is irregular (in meter) thus most coefficients are constant
dxs = dxw = dx
dys = dyw = dy

# %%
dx_min = min(dxw.min(), dyw.min(), dxs.min(), dys.min()).data
wet_mask = mask_land_100

wet_mask       = wet_mask.fillna(0)              # wet mask needs to be ones and zeros
wet_mask[0,:]  = np.zeros_like(wet_mask[0,:] )   # fix impact from southern boundary
wet_mask[:,-1] = np.zeros_like(wet_mask[:,-1] )  # fix impact from eastern boundary

mask_land_100_new =  wet_mask.where(wet_mask>0)

filter = gcm_filters.Filter(

    filter_scale=30000,

    dx_min=dx_min,

    filter_shape=gcm_filters.FilterShape.GAUSSIAN,

    grid_type=gcm_filters.GridType.IRREGULAR_WITH_LAND,

    grid_vars={'wet_mask': wet_mask, 
               'dxw'    : dxw,
               'dyw'    : dyw,
               'dxs'    : dxs,
               'dys'    : dys,
               'area'   : area,
               'kappa_w': kappa_w,
               'kappa_s': kappa_s}

)
filter
# %%
da_filtered = filter.apply(ds.isel(time=time), dims=['lat', 'lon'])
da_filtered = da_filtered * mask_land_100_new


(da_filtered).isel(depthi=idepth).plot()
# %%
(ds).isel(time=time).isel(depthi=idepth).plot()
# %%
((ds*wet_mask - da_filtered)).isel(time=time).isel(depthi=idepth).plot(vmin=-5e-3,vmax=5e-3, cmap='RdBu_r')
# %%
