#!/bin/python

# ©2023 MPI-M, Dian Putrasahan

# Track the eddies, get track IDs where eddy last more than mindays. Along the identified tracks, gather 2.5x2.5deg around eddy center and save. 

import sys
varname=sys.argv[1]
eddy_type=sys.argv[2]
rgn=sys.argv[3]
# #expid=sys.argv[1]
# yr=sys.argv[1]
# yyyy=int(yr)
#varname='to'
#varname='mlotst10'

import os 
import shutil
import numpy as np
from datetime import datetime, timedelta
import xarray as xr

mindays=10 #min number of days for tracked eddy
expid='ngc_72lev_HAM_prod'
fq='dm'
wavelength=400  #choice of spatial cutoff for high pass filter in km
pixel_limit=(20, 500)  # Min and max pixel count for valid contour
shape_error=55  # Error max (%) between ratio of circle fit and contour
eddydir='/work/bm1344/m300466/reg25/'+expid+'/eddytrack/sm'+str(wavelength)+'km/se'+str(shape_error)+'/pixmin'+str(pixel_limit[0])+'/pixmax'+str(pixel_limit[1])+'/'
tracker_dir=eddydir+'tracks/'

# eddy_type='cyclonic'
#eddy_type='anticyclonic'

#dscorres = xr.open_dataset(tracker_dir+expid+'_'+eddy_type+'_'+fq+'_correspondance.nc')
dstracks = xr.open_dataset(tracker_dir+eddy_type+'_tracks.nc')
#dsshort = xr.open_dataset(tracker_dir+eddy_type+'_short.nc')
#dsuntrack = xr.open_dataset(tracker_dir+eddy_type+'_untracked.nc')

dlon=2.5
dlat=2.5
res=0.25
npts=int(dlon/res) #number of points from centre

########################################
#Get desired region [Agulhas leakage in this case]
#ARidx = np.argwhere(((dstracks.latitude.values<=-20) & (dstracks.latitude.values>=-45) &
#                     (dstracks.longitude.values>350)) | ((dstracks.latitude.values<=-20) &
#                     (dstracks.latitude.values>=-45) & (dstracks.longitude.values<25)) )
if rgn=='SO': 
    ARidx = np.argwhere((dstracks.latitude.values<=-40) & (dstracks.latitude.values>=-65))
elif rgn=='AR': 
    ARidx = np.argwhere((dstracks.latitude.values<=-30) & (dstracks.latitude.values>=-45) & 
            (dstracks.longitude.values>0) & (dstracks.longitude.values<25))
    mindays=60 #min number of days for tracked eddy
elif rgn=='NB': 
    ARidx = np.argwhere(((dstracks.latitude.values<=10) & (dstracks.latitude.values>=0.5) & 
        (dstracks.longitude.values>300)) & (dstracks.longitude.values<320))
elif rgn=='LC': 
    ARidx = np.argwhere(((dstracks.latitude.values<=30) & (dstracks.latitude.values>=20) & 
        (dstracks.longitude.values>270)) & (dstracks.longitude.values<280))

#Get track IDs for Agulhas rings, remove all duplicates
ARtrackid=np.array(sorted(list(set(dstracks.track.values[ARidx].squeeze()))))
print('Track IDs=',ARtrackid)

#Get number of obs for each track for Agulhas rings
trackIDs=dstracks.track.values
tracklen=[]
for ii in range(trackIDs.max()+1):
    tracklen.append(len(np.argwhere(trackIDs == ii)))
lentrack=np.array(tracklen)[ARtrackid]
print('No. of obs for each tracked ID =',lentrack)

#Remove tracks with less than mindays
newARtrackid=np.delete(ARtrackid,np.r_[np.argwhere(lentrack<mindays)])
print('Track IDs that last more than '+str(mindays)+' days=',newARtrackid)
lentrack=np.array(tracklen)[newARtrackid]
print('No. of obs for each tracked ID =',lentrack)
del(tracklen)


def geteddy_alongtrack(dmvarfile,varname,loncen,latcen,dlon=2.5,dlat=2.5,npts=npts):
    npts2=npts*2
    loncen=round(loncen,2)
    latcen=round(latcen,2)
    dsvar=xr.open_dataset(dmvarfile)
    if varname=='rho':
        FIELD=dsvar['rhopoto']
    else:
        FIELD=dsvar[varname]
    lonmin=round(loncen-dlon,2)
    lonmax=round(loncen+dlon,2)
    latmin=round(latcen-dlat,2)
    latmax=round(latcen+dlat,2)
    print('eddy center='+str(loncen)+','+str(latcen))
    print('lonmin='+str(lonmin)+', lonmax='+str(lonmax)+', latmin='+str(latmin)+', latmax='+str(latmax))
    if (lonmin < 0) & (lonmax < 0):
        FIELDcomp=FIELD.sel(lon=slice(lonmin+360,lonmax+360),lat=slice(latmin,latmax))
    elif (lonmin < 0) & (lonmax >= 0):
        FIELDcomp=xr.concat([FIELD.sel(lon=slice(lonmin+360,360),lat=slice(latmin,latmax)),FIELD.sel(lon=slice(0,lonmax),lat=slice(latmin,latmax))],dim='lon')
    elif (lonmax > 360):
        FIELDcomp=xr.concat([FIELD.sel(lon=slice(lonmin,360),lat=slice(latmin,latmax)),FIELD.sel(lon=slice(0,lonmax-360),lat=slice(latmin,latmax))],dim='lon')
    else:
        FIELDcomp=FIELD.sel(lon=slice(lonmin,lonmax),lat=slice(latmin,latmax))
    FIELDcomp=FIELDcomp.squeeze()
    # print(np.shape(FIELDcomp))
    if np.shape(FIELDcomp.squeeze())!=(npts2,npts2):
        print(np.shape(FIELDcomp))
        print('issue with '+dmvarfile)
        # FIELDcomp=FIELDcomp[:,:npts2,:npts2]
        FIELDcomp=FIELDcomp[:npts2,:npts2]
    return FIELDcomp

#Note that this extract eddy tracks but does not normalise to eddy radius
def extract_eddytrack_raw(dstracks,tridx,varname='zos',expid='erc1011',fq='dm',wavelength=700,dlon=2.5,dlat=2.5,res=0.25):
    npts=int(dlon/res)
    npts2=npts*2
    alongtrackidx=np.argwhere(dstracks.track.values==tridx)
    Reff=dstracks.effective_radius.values[alongtrackidx] #in metres
    loncen=dstracks.longitude.values[alongtrackidx]
    latcen=dstracks.latitude.values[alongtrackidx]
    timearr=dstracks.time.values[alongtrackidx].flatten()
    date_arr=[]
    FIELDcomp=[]
    for tt in range(len(timearr)):
        date_arr.append(datetime.strptime(str(timearr[tt])[:10], '%Y-%m-%d'))
        date=date_arr[tt]
        # print('Extracting for '+date.strftime('%Y%m%d'))
        #Get high pass filtered classified data
        outdir='/work/bm1344/m300466/reg25/'+expid+'/eddytrack/'
        if varname=='to' or varname=='so' or varname=='rho' or varname=='delcar' or varname=='delsil' or varname=='det' or varname=='dissic' or varname=='dissoc' or varname=='hi' or varname=='no3' or varname=='NPP' or varname=='o2' or varname=='phydiaz' or varname=='phyp' or varname=='po4' or varname=='remin' or varname=='talk' or varname=='wpoc':
            dmvarfile=outdir+varname+'/sm'+str(int(wavelength))+'km/'+expid+'_'+varname+'_1_'+fq+'_'+date.strftime('%Y%m%d')+'_IFS25_hp'+str(wavelength)+'.nc'
        else:
            dmvarfile=outdir+varname+'/sm'+str(int(wavelength))+'km/'+expid+'_'+varname+'_'+fq+'_'+date.strftime('%Y%m%d')+'_IFS25_hp'+str(wavelength)+'.nc'
        FIELDcomp.append(geteddy_alongtrack(dmvarfile,varname,loncen[tt][0],latcen[tt][0],dlon=dlon,dlat=dlat,npts=npts))
        del(dmvarfile)

    for ii in range(len(FIELDcomp)):
        if np.shape(FIELDcomp[ii].squeeze())!=(npts2,npts2):
            print(np.shape(FIELDcomp[ii].squeeze()))
            # print('issue with track#'+str(alongtrackidx))
        FIELDcomp[ii]=FIELDcomp[ii].assign_coords(lat=np.arange(-npts,npts)*res,lon=np.arange(-npts,npts)*res)

    return alongtrackidx, date_arr, FIELDcomp, FIELDcomp[0].attrs


for tridx in newARtrackid:
    print('Extracting for eddy track ',tridx)
    #Extract tracked eddies
    alongtrackidx, date_arr, FIELDcomp, FIELDattrs = extract_eddytrack_raw(dstracks,tridx,varname=varname,expid=expid,wavelength=wavelength,dlon=dlon,dlat=dlat,res=res)

    #Put SSH composite into xarray
    #dsSSH=create_eddycomp_dataset(SSHcomp,date_arr,npts,res,SSHattrs,tridx,alongtrackidx,dstracks)
    #Put FIELD composite into xarray
    fileout=tracker_dir+rgn+'/'+varname+'/'+varname+'_'+rgn+'_'+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'+str(tridx)+'.nc'
    if not os.path.isdir(tracker_dir+rgn+'/'+varname): os.mkdir(tracker_dir+rgn+'/'+varname)
    dsnew=xr.DataArray(data=np.array(FIELDcomp).squeeze(),
                 coords={'time':date_arr, 'y':np.arange(-npts,npts)*res, 'x':np.arange(-npts,npts)*res},
                 dims=['time','y','x'],name=varname,attrs=FIELDattrs)
    dsnew.to_netcdf(fileout)

    del(alongtrackidx)
    del(date_arr)
    del(FIELDcomp)
    del(FIELDattrs)
    del(fileout)
    del(dsnew)

