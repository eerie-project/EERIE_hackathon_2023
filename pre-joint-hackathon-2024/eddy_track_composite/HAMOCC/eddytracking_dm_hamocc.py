#!/bin/python

# ©2023 MPI-M, Dian Putrasahan

# Track the eddies and save data that allows continuation of tracking later on.

import sys
#yr=sys.argv[1]
#yyyy=int(yr)

# Testing out eddy tracker
import os 
import glob

from py_eddy_tracker.featured_tracking.area_tracker import AreaTracker
from py_eddy_tracker.tracking import Correspondances

import numpy as np
from datetime import datetime, timedelta
from netCDF4 import Dataset
import xarray as xr


expid='ngc_72lev_HAM_prod'
fq='dm'
wavelength=400  #choice of spatial cutoff for high pass filter in km
pixel_limit=(20, 500)  # Min and max pixel count for valid contour
shape_error=55  # Error max (%) between ratio of circle fit and contour

eddydir='/work/bm1344/m300466/reg25/'+expid+'/eddytrack/sm'+str(wavelength)+'km/se'+str(shape_error)+'/pixmin'+str(pixel_limit[0])+'/pixmax'+str(pixel_limit[1])+'/'
tracker_dir=eddydir+'tracks/'
if not os.path.exists(tracker_dir):  os.makedirs(tracker_dir)

nb_obs_min = 10 # minimum of 10 points in track to be considered a long trajectory
raw = False # 
cmin = 0.05 # minimum contour
virtual = 4 # number of consecutive timesteps with missing detection allowed
class_kw = dict(cmin=cmin)
zarr = False


#Functions from eddy-tracking.py (Malcolm Roberts)
def tracking(file_objects, previous_correspondance, eddy_type, zarr=False, nb_obs_min=10, raw=True, cmin=0.05, virtual=4):
    # %%
    # We run a tracking with a tracker which uses contour overlap, on first time step
    output_dir = os.path.dirname(previous_correspondance)
    class_kw = dict(cmin=cmin)
    if not os.path.isfile(previous_correspondance):
        c = Correspondances(
            datasets=file_objects, class_method=AreaTracker, 
            class_kw=class_kw, virtual=virtual
        )
        c.track()
        c.prepare_merging()
    else:
        c = Correspondances(
            datasets=file_objects, class_method=AreaTracker, 
            class_kw=class_kw, virtual=virtual,
            previous_correspondance=previous_correspondance
        )
        c.track()
        c.prepare_merging()
        c.merge()

    new_correspondance = previous_correspondance[:-3]+'_new.nc'
    with Dataset(new_correspondance, "w") as h:
        c.to_netcdf(h)

    try:
        # test can read new file, and then move to replace old file
        nc = Dataset(new_correspondance, 'r')
        os.rename(new_correspondance, previous_correspondance)
    except:
        raise Exception('Error opening new correspondance file '+new_correspondance)

    write_obs_files(c, raw, output_dir, zarr, eddy_type, nb_obs_min)
    

def write_obs_files(c, raw, output_dir, zarr, eddy_type, nb_obs_min):
    kw_write = dict(path=output_dir, zarr_flag=zarr, sign_type=eddy_type)

    fout = os.path.join(output_dir, eddy_type+'_untracked.nc')
    c.get_unused_data(raw_data=raw).write_file(
        filename=fout
    )

    short_c = c._copy()
    short_c.shorter_than(size_max=nb_obs_min)
    short_track = short_c.merge(raw_data=raw)

    if c.longer_than(size_min=nb_obs_min) is False:
        long_track = short_track.empty_dataset()
    else:
        long_track = c.merge(raw_data=raw)

    # We flag obs
    if c.virtual:
        long_track["virtual"][:] = long_track["time"] == 0
        long_track.normalize_longitude()
        long_track.filled_by_interpolation(long_track["virtual"] == 1)
        short_track["virtual"][:] = short_track["time"] == 0
        short_track.normalize_longitude()
        short_track.filled_by_interpolation(short_track["virtual"] == 1)

    print("Longer track saved have %d obs", c.nb_obs_by_tracks.max())
    print(
        "The mean length is %d observations for long track",
        c.nb_obs_by_tracks.mean(),
    )

    fout = os.path.join(output_dir, eddy_type+'_tracks.nc')
    long_track.write_file(filename=fout)
    fout = os.path.join(output_dir, eddy_type+'_short.nc')
    short_track.write_file(
        #filename="%(path)s/%(sign_type)s_track_too_short.nc", **kw_write
        filename=fout
    )



eddy_type='anticyclonic'
previous_correspondance = os.path.join(tracker_dir, expid+'_'+eddy_type+'_'+fq+'_correspondance.nc')
# search = os.path.join(eddydir+expid+'_'+eddy_type+'_'+fq+'_20200[1-3]*.nc')
search = os.path.join(eddydir+expid+'_'+eddy_type+'_'+fq+'_2020????.nc')
print('search files ',search)
file_objects = sorted(glob.glob(search))
tracking(file_objects, previous_correspondance, eddy_type, zarr=zarr, nb_obs_min=nb_obs_min, raw=raw, cmin=cmin)

eddy_type='cyclonic'  #need to include all changes with eddy_type
previous_correspondance = os.path.join(tracker_dir, expid+'_'+eddy_type+'_'+fq+'_correspondance.nc')
search = os.path.join(eddydir+expid+'_'+eddy_type+'_'+fq+'_2020????.nc')
print('search files ',search)
file_objects = sorted(glob.glob(search))
tracking(file_objects, previous_correspondance, eddy_type, zarr=zarr, nb_obs_min=nb_obs_min, raw=raw, cmin=cmin)

