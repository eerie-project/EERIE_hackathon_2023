#!/bin/python

# ©2023 MPI-M, Dian Putrasahan

import sys
#expid=sys.argv[1]
yr=sys.argv[1]
mth=sys.argv[2]
day=sys.argv[3]
yyyy=int(yr)
mm=int(mth)
dd=int(day)

from py_eddy_tracker.dataset.grid import RegularGridDataset
import numpy as np
from datetime import datetime, timedelta
from netCDF4 import Dataset
import os

# Read in example SSH data that has been mapped onto a 0.25deg regular grid.
# /work/bm1344/m300466/reg25/ngc_72lev_HAM_prod/zos

expid='ngc_72lev_HAM_prod'
varname='zos'
fq='dm'
date = datetime(yyyy,mm,dd)

wavelength=400  #choice of spatial cutoff for high pass filter in km
step_ht=0.002 #step between two isolines of detection (m); intervals to search for closed contours (2mm in this case)
pixel_limit=(20, 500)  # Min and max pixel count for valid contour
shape_error=55  # Error max (%) between ratio of circle fit and contour

def detection1file(varfile,varname,date,wavelength,step_ht,pixlim,shape_error):
    g = RegularGridDataset(varfile, "lon", "lat", centered=True)
    # date = datearr[tt] # detect each timestep individually because of memory issues
    g.add_uv(varname)
    g.bessel_high_filter(varname, wavelength, order=1)

    a, c = g.eddy_identification(varname, "u", "v",
    date,  # Date of identification
    step_ht,  # step between two isolines of detection (m)
    pixel_limit=pixlim,  # Min and max pixel count for valid contour
    shape_error=shape_error  # Error max (%) between ratio of circle fit and contour
    )
    return a,c,g


outdir='/work/bm1344/m300466/reg25/'+expid+'/eddytrack/'
if not os.path.isdir(outdir): os.mkdir(outdir)
outdir1=outdir+'sm'+str(wavelength)+'km/'
outdir2=outdir+'sm'+str(wavelength)+'km/se'+str(shape_error)+'/'
outdir3=outdir+'sm'+str(wavelength)+'km/se'+str(shape_error)+'/pixmin'+str(pixel_limit[0])+'/'
outdir4=outdir+'sm'+str(wavelength)+'km/se'+str(shape_error)+'/pixmin'+str(pixel_limit[0])+'/pixmax'+str(pixel_limit[1])+'/'
if not os.path.isdir(outdir1): os.mkdir(outdir1)
if not os.path.isdir(outdir2): os.mkdir(outdir2)
if not os.path.isdir(outdir3): os.mkdir(outdir3)
if not os.path.isdir(outdir4): os.mkdir(outdir4)


# Save to netcdf 
print('Identifying daily eddies for '+date.strftime('%Y%m%d'))
varfile='/work/bm1344/m300466/reg25/'+expid+'/'+varname+'/'+expid+'_'+varname+'_'+fq+'_'+date.strftime('%Y%m%d')+'_IFS25.nc'
a_filtered, c_filtered, g_filtered = detection1file(varfile,varname,date,wavelength,step_ht,pixel_limit,shape_error)
with Dataset(date.strftime(outdir4+expid+"_anticyclonic_"+fq+"_"+date.strftime('%Y%m%d')+".nc"), "w") as h:
    a_filtered.to_netcdf(h)
with Dataset(date.strftime(outdir4+expid+"_cyclonic_"+fq+"_"+date.strftime('%Y%m%d')+".nc"), "w") as h:
    c_filtered.to_netcdf(h)
del a_filtered
del c_filtered
del g_filtered
del date


