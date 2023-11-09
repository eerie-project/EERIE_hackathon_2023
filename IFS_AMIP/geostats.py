import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def lon_360_to_180(da,lon='lon',inplace=False):
    '''
    Convert longitude from (0-360 E) to (180W - 180E)
    Reference: https://gis.stackexchange.com/a/201793
    '''
    if inplace == True:
        raise ValueError('option inplace=True in not functional, does not sort longitude appropriately.')
    if not lon in da.coords:
        print('Try to infer: longitude is named "longitude?"')
        if not 'longitude' in da.coords:
            print('Cannot find coordinate named "lon" or "longitude"')
            raise ValueError
        else:
            print("Found coordinate 'longitude'")
            lon = 'longitude'
    if inplace == True:
        da[lon] = np.mod(da[lon] + 180, 360) - 180
        da = da.sortby(lon)
    else:
        lon_attrs = da[lon].attrs
        da_out = da.assign_coords({lon:np.mod(da[lon] + 180, 360) - 180}).sortby(lon)
        da_out[lon].attrs = lon_attrs
        return da_out
#     return da.sortby('lon')

def lon_180_to_360(da,lon='lon',inplace=False):
    '''
    Convert longitude from (180W - 180E) to (0-360 E)
    Reference: https://gis.stackexchange.com/a/201793
    '''
    if inplace == True:
        raise ValueError('option inplace=True in not functional, does not sort longitude appropriately.')
    if not lon in da.coords:
        print('Try to infer: longitude is named "longitude?"')
        if not 'longitude' in da.coords:
            print('Cannot find coordinate named "lon" or "longitude"')
            raise ValueError
        else:
            lon = 'longitude'
    if inplace == True:
        da[lon] = np.mod(da[lon], 360)
        da = da.sortby(lon)
    else:
        lon_attrs = da[lon].attrs
        da_out = da.assign_coords({lon:np.mod(da[lon], 360)}).sortby(lon)
        da_out[lon].attrs = lon_attrs
        return da_out
#     return da.sortby('lon')


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
