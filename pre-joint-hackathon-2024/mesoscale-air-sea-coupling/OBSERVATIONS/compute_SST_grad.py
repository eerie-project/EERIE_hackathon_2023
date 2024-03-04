# Regrid to tco1279

import os, sys
import xarray as xr
import numpy as np
import filtering as fl
from dask.diagnostics import ProgressBar
import time as T

import argparse
parser = argparse.ArgumentParser()
# parser.add_argument('filename')
parser.add_argument('year')
parser.add_argument('month')
parser.add_argument('day')
parser.add_argument('resol')
parser.add_argument('product')
parser.add_argument('smoothc')
parser.add_argument('smootha')
parser.add_argument('--rm_tmp',default=1)

args = parser.parse_args()
# filename_in = args.filename
year = int(args.year)
month = int(args.month)
day = int(args.day)
resol = args.resol
product = args.product
smoothc = args.smoothc
smootha = args.smootha
rm_tmp = int(args.rm_tmp)
# regridding method: a) conservative MIR, b) bilinear cdo
# method = 'MIR-con' # 'cdo-bil'
method = 'cdo-bil'

assert product in ['OSTIA','ESAv2','ESAv3','GLORYS','ERA5']
assert rm_tmp in [0,1]
assert resol[:3] == 'tco' # only tco grids currently defined
assert resol in ['tco1279','tco199','tco319','tco399'] # currently defined resolutions

# if product in ['ESAv2','ESAv3','GLORYS','ERA5']:
# if product in ['ESAv3','GLORYS','ERA5']:
# if product in ['ESAv3']:
#     sys.exit('Not yet implemented: %s' % product)

t0 = T.time()
print('\n============================')
print('Script: compute_SST_grad.py')
print('Compute SST gradient from %s and regrid to resolution %s, smoothing climatology: %s, smoothing anomalies %s: %.4i-%.2i-%.2i' % (product,resol,smoothc,smootha,year,month,day))
print('Arguments:')
print(args)
print('============================')

# Path and filenames for temporary files
path_tmp = '/ec/res4/scratch/neam/01_SST_VAR/SST/gradients/'
pattern_tmp = '{product}_{smoothc}_{smootha}_sst_ice_{year:04d}{month:02d}{day:02d}.nc'
# pattern_tmp_remap = '{product}_{smoothc}_{smootha}_sst_ice_{year:04d}{month:02d}{day:02d}_{resol}{version}.grib'
pattern_tmp_remap = '{product}_{smoothc}_{smootha}_sst_ice_{year:04d}{month:02d}{day:02d}_{resol}{version}.nc'

# Path and filenames for PERM storage files - "_4" denotes "GTYPE": _4 is for tco grids
assert resol[:3] == 'tco' # this only works for tco grids
if smoothc == '0' and smootha == '0':
    print('No filtering requested of either climatology or anomalies')
    # path_ancils = '/perm/neam/02_AMIP_IFS/ancil/{product}/{resoli}_4/'.format(
    # TESTING
    # path_ancils = '/perm/neam/02_AMIP_IFS/ancil/{product}_v7/{resoli}_4/'.format(
    path_ancils = '/perm/neam/01_SST_VAR/SST/gradients/{product}/{resoli}_4/'.format(
        product=product,resoli=resol[3:]
    )
else:
    path_ancils = '/perm/neam/01_SST_VAR/SST/gradients/{product}_c_{smoothc}_a_{smootha}/{resoli}_4/'.format(
        product=product,smoothc=smoothc,smootha=smootha,resoli=resol[3:]
    )

# pattern_ancil = 'sst_grad_{year:04d}{month:02d}{day:02d}.grib'
pattern_ancil = 'sst_grad_{year:04d}{month:02d}{day:02d}.nc'

# ------------------------------------------------
# Options to modify directories and filenames for testing
# path_ancils += 'test_MIR-con/'
# path_ancils += 'test_cdo-bil/'
# pattern_ancil = 'sst_ice_{year:04d}{month:02d}{day:02d}_test.grib'
# ------------------------------------------------


if not os.path.exists(path_ancils):
    print('Creating output directory')
    os.system('mkdir -p %s' % path_ancils)


# regular data at native resolution, netcdf
file_regular = path_tmp + pattern_tmp.format(product=product, smoothc=smoothc,smootha=smootha,year=year,month=month,day=day)
# tco regridded file, pre-processing, v1
file_tco1 = path_tmp + pattern_tmp_remap.format(product=product, smoothc=smoothc,smootha=smootha,year=year,month=month,day=day,resol=resol,version='_v1')
file_tco2 = path_tmp + pattern_tmp_remap.format(product=product, smoothc=smoothc,smootha=smootha,year=year,month=month,day=day,resol=resol,version='_v2')
file_tco3 = path_tmp + pattern_tmp_remap.format(product=product, smoothc=smoothc,smootha=smootha,year=year,month=month,day=day,resol=resol,version='_v3')
# final formatted daily SST/CI in PERM storage
file_ancil = path_ancils + pattern_ancil.format(year=year,month=month,day=day)

print('Set file for mask')
if resol == 'tco1279':
    # mask='/perm/neam/02_AMIP_IFS/data/i3ba_sst_mask.grib'
    mask='/perm/neam/02_AMIP_IFS/data/lsmoro.v021_1279_lsm_binary.grib'
    setgrid = '/perm/neam/02_AMIP_IFS/i3ba/sstgrib_reorder'
    gridtype = 'O1280'
elif resol == 'tco199':
    # mask='/perm/neam/02_AMIP_IFS/data/hzmh_sst_mask.grib'
    mask='/perm/neam/02_AMIP_IFS/data/lsmoro.v021_199_lsm_binary.grib'
    setgrid = '/perm/neam/02_AMIP_IFS/hzp7/sstgrib_reorder'
    gridtype = 'O200'
elif resol == 'tco319':
    # mask='/perm/neam/02_AMIP_IFS/data/i3es_sst_mask.grib'
    mask='/perm/neam/02_AMIP_IFS/data/lsmoro.v021_319_lsm_binary.grib'
    setgrid = '/perm/neam/02_AMIP_IFS/i3es/sstgrib_reorder'
    gridtype = 'O320'
elif resol == 'tco399':
    # mask='/perm/neam/02_AMIP_IFS/data/i5li_sst_mask.grib'
    mask='/perm/neam/02_AMIP_IFS/data/lsmoro.v021_399_lsm_binary.grib'
    setgrid = '/perm/neam/02_AMIP_IFS/i5li/sstgrib_reorder'
    gridtype = 'O400'
else:
    sys.exit('Not defined for resolution %s' % resol)
print('Defined mask for resolution %s: %s' % (resol,mask))

# ======================================
# LOAD ZARR STORES FOR CHOSEN PRODUCT AND FILTERING SETTINGS

print('Load data as zarr')
if product == 'OSTIA':
    ds = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/original.zarr')
    if not ( smoothc == '0' and smootha == '0'):
        print('Filtering requested: climatology: %s, anomalies: %s' % (smoothc,smootha))
        print('Load requested zarr stores for climatology and anomalies')
        if smoothc == '0':
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/original_clim_loess.zarr')
        else:
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/original_clim_fl_{smoothc}.zarr'.format(smoothc=smoothc))
        if smootha == '0':
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/original_anom_loess_f32.zarr')
        else:
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/original_anom_fl_{smootha}.zarr'.format(smootha=smootha))
    else:
        print('No filtering requested - load only actual data, not climatology or anomalies')
elif product == 'ESAv2':
    ds = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_024/original.zarr')
    if not ( smoothc == '0' and smootha == '0'):
        print('Filtering requested: climatology: %s, anomalies: %s' % (smoothc,smootha))
        print('Load requested zarr stores for climatology and anomalies')
        if smoothc == '0':
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_024/original_clim_loess.zarr')
        else:
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_024/original_clim_fl_{smoothc}.zarr'.format(smoothc=smoothc))
        if smootha == '0':
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_024/original_anom.zarr')
        else:
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/SST_GLO_SST_L4_REP_OBSERVATIONS_010_024/original_anom_fl_{smootha}.zarr'.format(smootha=smootha))
    else:
        print('No filtering requested - load only actual data, not climatology or anomalies')
elif product == 'ESAv3':
    ds = xr.open_zarr('/perm/neam/01_SST_VAR/JASMIN/SST_ESA-CCI_v3/original.zarr')
    if not ( smoothc == '0' and smootha == '0'):
        print('Filtering requested: climatology: %s, anomalies: %s' % (smoothc,smootha))
        print('Load requested zarr stores for climatology and anomalies')
        if smoothc == '0':
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/JASMIN/SST_ESA-CCI_v3/original_clim_loess_Feb29_interp.zarr')
        else:
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/JASMIN/SST_ESA-CCI_v3/original_clim_fl_{smoothc}.zarr'.format(smoothc=smoothc))
        if smootha == '0':
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/JASMIN/SST_ESA-CCI_v3/original_anom_loess_f32.zarr')
        else:
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/JASMIN/SST_ESA-CCI_v3/original_anom_fl_{smootha}.zarr'.format(smootha=smootha))
    else:
        print('No filtering requested - load only actual data, not climatology or anomalies')
elif product == 'GLORYS':
    ds = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/GLOBAL_REANALYSIS_PHY_001_030/original.zarr')
    if not ( smoothc == '0' and smootha == '0'):
        print('Filtering requested: climatology: %s, anomalies: %s' % (smoothc,smootha))
        print('Load requested zarr stores for climatology and anomalies')
        if smoothc == '0':
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/GLOBAL_REANALYSIS_PHY_001_030/original_clim_loess.zarr')
        else:
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/GLOBAL_REANALYSIS_PHY_001_030/original_clim_fl_{smoothc}.zarr'.format(smoothc=smoothc))
        if smootha == '0':
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/GLOBAL_REANALYSIS_PHY_001_030/original_anom_loess_f32.zarr')
        else:
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CMEMS/GLOBAL_REANALYSIS_PHY_001_030/original_anom_fl_{smootha}.zarr'.format(smootha=smootha))
    else:
        print('No filtering requested - load only actual data, not climatology or anomalies')
elif product == 'ERA5':
    ds = xr.open_zarr('/perm/neam/01_SST_VAR/CDS/ERA5/era5_daily.zarr')
    ds['lon'].attrs['units'] = 'degrees_east'
    ds['lon'].attrs['long_name'] = 'longitude'
    if not ( smoothc == '0' and smootha == '0'):
        print('Filtering requested: climatology: %s, anomalies: %s' % (smoothc,smootha))
        print('Load requested zarr stores for climatology and anomalies')
        if smoothc == '0':
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CDS/ERA5/era5_daily_clim_loess.zarr')
        else:
            dsc = xr.open_zarr('/perm/neam/01_SST_VAR/CDS/ERA5/era5_daily_clim_fl_{smoothc}.zarr'.format(smoothc=smoothc))
        dsc['lon'].attrs['units'] = 'degrees_east'
        dsc['lon'].attrs['long_name'] = 'longitude'
        if smootha == '0':
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CDS/ERA5/era5_daily_anom_loess_f32.zarr')
        else:
            dsa = xr.open_zarr('/perm/neam/01_SST_VAR/CDS/ERA5/era5_daily_anom_fl_{smootha}.zarr'.format(smootha=smootha))
        dsa['lon'].attrs['units'] = 'degrees_east'
        dsa['lon'].attrs['long_name'] = 'longitude'
    else:
        print('No filtering requested - load only actual data, not climatology or anomalies')
else:
    sys.exit('Product %s is not defined' % product)

# ======================================
# ASSEMBLING DATA FOR THIS DAY, AND SAVE TO NETCDF
    
# Get data and assemble
        
dsi = ds[['sst']].sel(time='%.4i-%.2i-%.2i' % (year,month,day))
# overwrite SST as requested
if not ( smoothc == '0' and smootha == '0'):
    print('Replace data by clim + anomalies')
    dsi['sst'].values = (
        dsa['sst'].sel(time='%.4i-%.2i-%.2i' % (year,month,day)) 
        + dsc['sst'].sel(time='%.4i-%.2i-%.2i' % (2004,month,day)).drop('time')
    )

# if GLORYS: Need to fill zeros for sea ice cover
if product == 'GLORYS':
    dsi = dsi.drop('depth')
    dsi['sst'].attrs['long_name'] = 'Sea surface temperature'
    dsi['sst'].attrs['standard_name'] = 'sea_surface_temperature'


# Compute SST gradient
grid = fl.get_grid(dsi)
dTdx = grid.interp(grid.derivative(dsi.sst,'X',boundary='fill',fill_value=np.nan),'X') * 1000
dTdy = grid.interp(grid.derivative(dsi.sst,'Y',boundary='fill',fill_value=np.nan),'Y') * 1000

dTdx = dTdx.rename('dTdx')
dTdx.attrs['units'] = 'K/km'
dTdy = dTdx.rename('dTdy')
dTdy.attrs['units'] = 'K/km'

mag = (dTdx**2 + dTdy**2)**0.5
mag = mag.rename('gradient_magnitude')
mag.attrs['units'] = 'K/km'

grads = xr.merge([
    dTdx,
    dTdy,
    mag
])

with ProgressBar():
    grads.load()

# save full-res data to netcdf, per timestep
grads.to_netcdf(
    file_regular
)
print('Done saving native resolution timestep')

# ======================================
# REGRIDDING AND PROCESSING
if method == 'MIR-con':
    print('\nRegrid using conservative MIR (--interpolation=grid-box-average)\n')

    print('Convert to grib')
    # Regrid with cdo to target grid
    command_str = 'cdo -b 24 -f grb2 -selname,dTdx,dTdy {infile} {outfile}'.format(
        infile=file_regular,
        outfile=file_tco1,
    )
    print(command_str)
    os.system(command_str)

    print('Set grib metadata for MIR')
    # NOTE: not sure what's the best way here to determine bounds for MIR - might need to be by dataset? attempt to do here
    latOfFirstGridPoint = (ds.lat.values.min().astype(float).round(3) * 1000000).astype(int)
    latOfLastGridPoint = (ds.lat.values.max().astype(float).round(3) * 1000000).astype(int)
    lonOfFirstGridPoint = ((ds.lon.values.min() + 360).astype(float).round(3) * 1000000).astype(int)
    lonOfLastGridPoint = (ds.lon.values.max().astype(float).round(3) * 1000000).astype(int)
    command_str = 'grib_set -s centre=98,latitudeOfFirstGridPoint={latitudeOfFirstGridPoint},longitudeOfFirstGridPoint={longitudeOfFirstGridPoint},latitudeOfLastGridPoint={latitudeOfLastGridPoint},longitudeOfLastGridPoint={longitudeOfLastGridPoint} {infile} {outfile}'.format(
        latitudeOfFirstGridPoint=latOfFirstGridPoint,
        longitudeOfFirstGridPoint=lonOfFirstGridPoint,
        latitudeOfLastGridPoint=latOfLastGridPoint,
        longitudeOfLastGridPoint=lonOfLastGridPoint,
        infile=file_tco1,
        outfile=file_tco2
    )
    print(command_str)
    os.system(command_str)

    print('Regrid conservatively with MIR')
    command_str = 'MIR_GRIB_INPUT_BUFFER_SIZE=77760179 /usr/local/apps/mars/versions/6.33.15.9/bin/mir --grid={gridtype} --interpolation=grid-box-average --non-linear=missing-if-all-missing {infile} {outfile}'.format(
        gridtype=gridtype,
        infile=file_tco2,
        outfile=file_tco3
    )
    print(command_str)
    os.system(command_str)

    print('Set time axis and mask')
    # command_str = 'cdo -b 24 -f grb2 -settaxis,{year:04d}-{month:02d}-{day:02d},12:00:00,1day -mul {mask} -setmisstodis {infile} {outfile}'.format(
    command_str = 'cdo -b 24 -f nc -settaxis,{year:04d}-{month:02d}-{day:02d},12:00:00,1day -mul {mask} -setmisstodis {infile} {outfile}'.format(
            year=year,
            month=month,
            day=day,
            mask=mask,
            infile=file_tco3,
            outfile=file_ancil
        )
    print(command_str)
    os.system(command_str)


elif method == 'cdo-bil':
    print('\nRegrid using bilinear cdo (cdo remapbil)\n')

    # Regrid with cdo to target grid
    # command_str = 'cdo -b 24 -f nc -setgrid,{setgrid} -setgridtype,unstructured -remapbil,{setgrid} -setmisstodis -selname,dTdx,dTdy {infile} {outfile}'.format(
    # command_str = 'cdo -b 24 -f nc -setgrid,{setgrid} -setgridtype,unstructured -remapbil,{setgrid} -selname,dTdx,dTdy {infile} {outfile}'.format(
    command_str = 'cdo --eccodes -b 24 -f nc -setgrid,{setgrid} -setgridtype,unstructured -remapbil,{setgrid} {infile} {outfile}'.format(
        infile=file_regular,
        outfile=file_tco1,
        setgrid=setgrid
    )
    print(command_str)
    os.system(command_str)

    print('Done regridding')

    print('Begin formatting')

    print('Various grib processing')
    # command_str = 'cdo -b 24 -f nc -settaxis,{year:04d}-{month:02d}-{day:02d},12:00:00,1day -mul {infile} {mask} {outfile}'.format(
    command_str = 'cdo --eccodes -b 24 -f nc -settaxis,{year:04d}-{month:02d}-{day:02d},12:00:00,1day -mul {infile} {mask} {outfile}'.format(
            year=year,
            month=month,
            day=day,
            mask=mask,
            infile=file_tco1,
            outfile=file_tco2
        )
    print(command_str)
    os.system(command_str)

    # Get grid and save
    maskfile = xr.open_dataset(mask)
    dsi2 = xr.open_dataset(file_tco2)
    dsi2 = xr.merge([
        dsi2.rename({'rgrid':'values'}),
        maskfile[['latitude','longitude']]
    ]).load().drop(['reduced_points','lat'])
    dsi2.to_netcdf(file_ancil)
    # print('Set centre')
    # command_str = 'grib_set -s centre=98 {infile} {outfile}'.format(
    #     infile=file_tco2,
    #     # outfile=file_tco3
    #     outfile=file_ancil
    # )
    # print(command_str)
    # os.system(command_str)

else:
    sys.exit('Regridding method %s is not defined. Exiting...' % method)

# Done: Regridding and processing
# ======================================

assert os.path.exists(file_ancil)

print('\nOutput saved in: %s\n' % file_ancil)

if rm_tmp == 1:
    print('Remove temporary files')
    for f in [
            file_regular,
            file_tco1,
            file_tco2,
            file_tco3
            ]:
        if os.path.exists(f):
            print('Remove file %s' % f)
            os.system('rm %s' % f)
else:
    print('Do not remove temporary files')


print('\n============================')
# print('Processed {product} SST/CI data using conservative MIR regridding for day {year:04d}-{month:02d}-{day:02d} at resolution {resol} with smoothing clim: {smoothc}, smoothing anom: {smootha}'.format(
print('Computed SST gradient from {product} using {method} regridding for day {year:04d}-{month:02d}-{day:02d} at resolution {resol} with smoothing clim: {smoothc}, smoothing anom: {smootha}'.format(
    product=product,
    method=method,
    year=year,
    month=month,
    day=day,
    resol=resol,
    smoothc=smoothc,
    smootha=smootha
    )
)
tf = T.time()
print('Total time: %.1f seconds' % (tf-t0))
print('============================')
print('Done')