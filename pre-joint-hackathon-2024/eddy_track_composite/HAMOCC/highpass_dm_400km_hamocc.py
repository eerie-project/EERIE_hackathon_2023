#!/bin/python
# ©2023 MPI-M, Dian Putrasahan

import sys
varname=sys.argv[1]
kmcut=sys.argv[2]
wavelength=int(kmcut)  #choice of spatial cutoff for high pass filter in km

print('High pass filter daily '+varname)

from py_eddy_tracker.dataset.grid import RegularGridDataset
from datetime import datetime, timedelta
import numpy as np

expid='ngc_72lev_HAM_prod'
fq='dm'
daterng='20200101-20201225'
datearr=np.arange(datetime(2020,1,1), datetime(2020,12,26), timedelta(days=1)).astype(datetime)

datadir='/work/bm1344/m300466/reg25/'+expid+'/'+varname+'/'
outdir0='/work/bm1344/m300466/reg25/'+expid+'/eddytrack/'+varname+'/'
outdir=outdir0+'sm'+str(int(wavelength))+'km/'
#Must create dirs first. 
#if not os.path.isdir(outdir0): os.mkdir(outdir0)
#if not os.path.isdir(outdir): os.mkdir(outdir)

if varname=='to' or varname=='so' or varname=='rho' or varname=='delcar' or varname=='delsil' or varname=='det' or varname=='dissic' or varname=='dissoc' or varname=='hi' or varname=='no3' or varname=='NPP' or varname=='o2' or varname=='phydiaz' or varname=='phyp' or varname=='po4' or varname=='remin' or varname=='talk' or varname=='wpoc':
    zidx=1
    varfile=datadir+expid+'_'+varname+'_'+str(zidx)+'_'+fq+'_'+daterng+'_IFS25.nc'
else:
    varfile=datadir+expid+'_'+varname+'_'+fq+'_'+daterng+'_IFS25.nc'

def besselhighpass(varfile, varname, datearr, tt, wavelength):
    g = RegularGridDataset(varfile, "lon", "lat", centered=True, indexs = dict(time=tt))
    g.dimensions['time']=1  #extracts only one time step that was specified by indexs = dict(time=tt)
    if varname=='rho':
        g.bessel_high_filter('rhopoto', wavelength, order=1)
    else:
        g.bessel_high_filter(varname, wavelength, order=1) #perfroms only on 1 time index
    date = datearr[tt] # detect each timestep individually because of memory issues
    if varname=='to' or varname=='so' or varname=='rho' or varname=='delcar' or varname=='delsil' or varname=='det' or varname=='dissic' or varname=='dissoc' or varname=='hi' or varname=='no3' or varname=='NPP' or varname=='o2' or varname=='phydiaz' or varname=='phyp' or varname=='po4' or varname=='remin' or varname=='talk' or varname=='wpoc':
        zidx=1
        g.write(outdir+expid+'_'+varname+'_'+str(zidx)+'_'+fq+'_'+date.strftime('%Y%m%d')+'_IFS25_hp'+str(wavelength)+'.nc')
    else:
        g.write(outdir+expid+'_'+varname+'_'+fq+'_'+date.strftime('%Y%m%d')+'_IFS25_hp'+str(int(wavelength))+'.nc')

    
for tt in range(0,len(datearr)):
    date = datearr[tt]
    print('High pass filter of '+varname+' for '+date.strftime('%Y%m%d'))
    besselhighpass(varfile, varname, datearr, tt, wavelength)
