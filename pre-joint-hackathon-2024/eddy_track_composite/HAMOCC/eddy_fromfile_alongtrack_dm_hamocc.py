#!/bin/python

# ©2023 MPI-M, Dian Putrasahan

# For the eddy corridor in the North Brazilian Current, track the eddies, get track IDs where eddy last more than 10 days. Along the identified tracks, gather 2.5x2.5deg around eddy center and save. 

import sys
eddy_type=sys.argv[1]
rgn=sys.argv[2]
# #expid=sys.argv[1]
# yr=sys.argv[1]
# yyyy=int(yr)

import os 
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
if not os.path.isdir(tracker_dir+rgn): os.mkdir(tracker_dir+rgn)


#eddy_type='cyclonic'
#eddy_type='anticyclonic'

dscorres = xr.open_dataset(tracker_dir+expid+'_'+eddy_type+'_'+fq+'_correspondance.nc')
dstracks = xr.open_dataset(tracker_dir+eddy_type+'_tracks.nc')
dsshort = xr.open_dataset(tracker_dir+eddy_type+'_short.nc')
dsuntrack = xr.open_dataset(tracker_dir+eddy_type+'_untracked.nc')

dlon=2.5
dlat=2.5
res=0.25
npts=int(dlon/res) #number of points from centre

########################################
#Get desired region [Southern Ocean in this case]
# ARidx = np.argwhere(((dstracks.latitude.values<=-20) & (dstracks.latitude.values>=-45) &
#                      (dstracks.longitude.values>350)) | ((dstracks.latitude.values<=-20) &
#                      (dstracks.latitude.values>=-45) & (dstracks.longitude.values<25)) )
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

#Remove tracks with less than minimum number of days 
newARtrackid=np.delete(ARtrackid,np.r_[np.argwhere(lentrack<mindays)])
print('Track IDs that last more than ',mindays,' days=',newARtrackid)
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
    if np.shape(FIELDcomp.squeeze())!=(npts2,npts2):
        print(np.shape(FIELDcomp))
        print('issue with '+dmvarfile)
        FIELDcomp=FIELDcomp[:,:npts2,:npts2]
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

#Note it is not normalized to eddy radius
def create_eddycomp_dataset(SSHcomp,date_arr,npts,res,SSHattrs,tridx,alongtrackidx,dstracks):
    compSSH=xr.DataArray(data=np.array(SSHcomp).squeeze(),
                 coords={'time':date_arr, 'y':np.arange(-npts,npts)*res, 'x':np.arange(-npts,npts)*res},
                 dims=['time','y','x'],name='zos',attrs=SSHattrs)
    dsSSH=compSSH.to_dataset()
    # dsSSH=dsSSH.assign({'eddytrackID':tridx})
    cpts=dstracks.uavg_profile.shape[1]
    dsSSH=dsSSH.merge(xr.DataArray(data=tridx,name='eddytrackID',attrs={'long name':'ID of eddy track'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=alongtrackidx.flatten(),coords={'time':date_arr},dims=['time'],name='track'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.longitude.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='lon',attrs={'long name':'longitude of eddy centre'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.latitude.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='lat',attrs={'long name':'latitude of eddy centre'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.effective_radius.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='effective_radius',attrs={'long name':'Effective radius of eddy'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.effective_area.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='effective_area',attrs={'long name':'Effective area of eddy'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.amplitude.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='amplitude',attrs={'long name':'Amplitude of eddy'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.time.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='date_time',attrs={'long name':'date and time in datetime64'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.observation_number.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='n',attrs={'long name':'days since first detection'}))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.uavg_profile.values[alongtrackidx].squeeze(),
                                   coords={'time':date_arr,'contour':np.arange(0,cpts)},dims=['time','contour'],name='uavg_profile'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.speed_average.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='speed_average'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.speed_area.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='speed_area'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.effective_contour_longitude.values[alongtrackidx].squeeze(),
                                   coords={'time':date_arr,'contour':np.arange(0,cpts)},dims=['time','contour'],name='contour_lon_e'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.effective_contour_latitude.values[alongtrackidx].squeeze(),
                                   coords={'time':date_arr,'contour':np.arange(0,cpts)},dims=['time','contour'],name='contour_lat_e'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.effective_radius.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='radius_e'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.num_point_e.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='num_point_e'))
    dsSSH=dsSSH.merge(xr.DataArray(data=np.array(dstracks.effective_contour_shape_error.values[alongtrackidx].flatten(),dtype='float32'),coords={'time':date_arr},dims=['time'],name='shape_error_e'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.speed_contour_longitude.values[alongtrackidx].squeeze(),
                                   coords={'time':date_arr,'contour':np.arange(0,cpts)},dims=['time','contour'],name='contour_lon_s'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.speed_contour_latitude.values[alongtrackidx].squeeze(),
                                   coords={'time':date_arr,'contour':np.arange(0,cpts)},dims=['time','contour'],name='contour_lat_s'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.speed_radius.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='radius_s'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.num_point_s.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='num_point_s'))
    dsSSH=dsSSH.merge(xr.DataArray(data=np.array(dstracks.speed_contour_shape_error.values[alongtrackidx].flatten(),dtype='float32'),coords={'time':date_arr},dims=['time'],name='shape_error_s'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.num_contours.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='nb_contour_selected'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.longitude_max.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='lon_max'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.latitude_max.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='lat_max'))
    # dsSSH=dsSSH.merge(xr.DataArray(data=eddies_area_tracker.height_external_contour[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='height_external_contour'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.inner_contour_height.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='height_inner_contour'))
    # dsSSH=dsSSH.merge(xr.DataArray(data=eddies_area_tracker.height_max_speed_contour[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='height_max_speed_contour'))
    dsSSH=dsSSH.merge(xr.DataArray(data=dstracks.cost_association.values[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='cost_association'))
    # dsSSH=dsSSH.merge(xr.DataArray(data=eddies_area_tracker.virtual[alongtrackidx].flatten(),coords={'time':date_arr},dims=['time'],name='virtual'))

    return dsSSH


#Note it is not normalized to eddy radius
def appendto_eddycomp_dataset(dsSSH,varname,FIELDcomp,date_arr,npts,res,FIELDattrs):
    dsSSH=dsSSH.merge(xr.DataArray(data=np.array(FIELDcomp).squeeze(),
                 coords={'time':date_arr, 'y':np.arange(-npts,npts)*res, 'x':np.arange(-npts,npts)*res},
                 dims=['time','y','x'],name=varname,attrs=FIELDattrs))
    return dsSSH

for tridx in newARtrackid:
    print('Extracting for eddy track ',tridx)
    #Extract tracked eddies
    alongtrackidx, date_arr, SSHcomp, SSHattrs = extract_eddytrack_raw(dstracks,tridx,varname='zos',expid=expid,wavelength=wavelength,dlon=dlon,dlat=dlat,res=res)

    #Put SSH composite into xarray
    dsSSH=create_eddycomp_dataset(SSHcomp,date_arr,npts,res,SSHattrs,tridx,alongtrackidx,dstracks)

    fileout=tracker_dir+rgn+'/'+expid+'_'+rgn+'_'+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'+str(tridx)+'.nc'
    dsSSH.to_netcdf(fileout)
    del(alongtrackidx)
    del(date_arr)
    del(SSHcomp)
    del(SSHattrs)
    del(fileout)
    del(dsSSH)


