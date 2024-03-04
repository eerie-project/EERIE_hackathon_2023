#Composite tracked eddies with higher resolution data than 0.25deg
#Author: Moritz Epke

# %%
from py_eddy_tracker.dataset.grid import RegularGridDataset
from datetime import datetime, timedelta
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
import os 
import glob

from py_eddy_tracker.featured_tracking.area_tracker import AreaTracker
from py_eddy_tracker.tracking import Correspondances

import numpy as np
from datetime import datetime, timedelta
import xarray as xr
# %%
import smt_modules.all_funcs as eva
from importlib import reload
import pyicon as pyic
reload(eva)
import sys
sys.path.insert(0, '../')
import funcs as fu
# %%
# root_dir = '/scratch/m/m300878/agulhas_eddies/exp9/'
# root_dir = '/work/mh0033/m300878/eddy_tracks/agulhas_eddies/exp9/'
root_dir = '/work/mh0033/m300878/eddy_tracks/agulhas_eddies/exp7/'

varname     = 'zos'
wavelength  = 700  #choice of spatial cutoff for high pass filter in km
shape_error = 25 #choice of shape error in km
eddy_dir    = f'{root_dir}'+'eddytrack_wv_'+str(int(wavelength))+'_se_'+str(int(shape_error))
eddy_type   = 'cyclonic'


# rgn='AR'
mindays=20 #min number of days for tracked eddy

tracker_dir=eddy_dir+'tracks/'

dlon       = 1.8
dlat       = 1.8
res        = 0.02
npts       = int(dlon/res) #number of points from centre

dscorres  = xr.open_dataset(tracker_dir+eddy_type+'_correspondance.nc')
dstracks  = xr.open_dataset(tracker_dir+eddy_type+'_tracks.nc')
dsshort   = xr.open_dataset(tracker_dir+eddy_type+'_short.nc')
dsuntrack = xr.open_dataset(tracker_dir+eddy_type+'_untracked.nc')


# %%
#Get desired region [Agulhas rings and leakage]
# ARidx = np.argwhere((dstracks.latitude.values<=-30) & (dstracks.latitude.values>=-45) & (dstracks.longitude.values>0) & (dstracks.longitude.values<25))
ARidx = np.argwhere((dstracks.latitude.values<=-20) & (dstracks.latitude.values>=-36) & (dstracks.longitude.values>-15) & (dstracks.longitude.values<20))

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

# %% plot contours
reload(fu)

fu.plot_eddy_contours_dian(dstracks, newARtrackid[:7])
# %%
def geteddy_alongtrack(dmvarfile,loncen,latcen,dlon=2.5,dlat=2.5,npts=npts):
    npts2   = npts*2
    loncen  = round(loncen,2)
    latcen  = round(latcen,2)

    FIELD  = dmvarfile
    lonmin = round(loncen-dlon,2)
    lonmax = round(loncen+dlon,2)
    latmin = round(latcen-dlat,2)
    latmax = round(latcen+dlat,2)
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
        print('Shape correction')
        data = FIELDcomp
        xlen = data.lon.size
        ylen = data.lat.size
        M = np.ones((int(2*npts),int(2*npts)))*np.nan
        M[int(npts-ylen/2):int(npts+ylen/2),int(npts-xlen/2):int(npts+xlen/2)] = data

        da         = xr.DataArray(M,dims=['lat','lon'],coords={'lat':np.arange(-npts,npts)*res,'lon':np.arange(-npts,npts)*res})
        da['time'] = data.time
        FIELDcomp  = da

    if np.shape(FIELDcomp.squeeze())!=(npts2,npts2):
        print(np.shape(FIELDcomp))
        print('issue with '+dmvarfile)
        FIELDcomp=FIELDcomp[:,:npts2,:npts2]

    return FIELDcomp


#Note that this extract eddy tracks but does not normalise to eddy radius
def extract_eddytrack_raw(dstracks,tridx,wavelength,dlon,dlat,res, path):
    npts          = int(dlon/res)
    npts2         = npts*2
    alongtrackidx = np.argwhere(dstracks.track.values==tridx)
    Reff          = dstracks.effective_radius.values[alongtrackidx] #in metres
    loncen        = dstracks.longitude.values[alongtrackidx]
    latcen        = dstracks.latitude.values[alongtrackidx]
    timearr       = dstracks.time.values[alongtrackidx].flatten()
    # timearr_xr = xr.DataArray(data=timearr,coords={'time':timearr},dims=['time'])

    ds_KE         = xr.open_dataset(path)
    # timearr_xr    = timearr_xr.sel(time=slice(ds_KE.time[0],ds_KE.time[-1]))
    # timearr       = timearr_xr.values

    print(f'load dataset from {path}')
    date_arr      = []
    FIELDcomp     = []
    for tt in range(len(timearr)):
        date_arr.append(datetime.strptime(str(timearr[tt])[:13], '%Y-%m-%dT%H'))
        # date=date_arr[tt]

        # raw input data to be extracted
        dmvarfile = ds_KE.KE.isel(time=tt)
        FIELDcomp.append(geteddy_alongtrack(dmvarfile,loncen[tt][0],latcen[tt][0],dlon=dlon,dlat=dlat,npts=npts))
        del(dmvarfile)
    
    for ii in range(len(FIELDcomp)):
        if np.shape(FIELDcomp[ii].squeeze())!=(npts2,npts2):
            print(np.shape(FIELDcomp[ii].squeeze()))
            print('issue with track#'+str(alongtrackidx))
        FIELDcomp[ii]=FIELDcomp[ii].assign_coords(lat=np.arange(-npts,npts)*res,lon=np.arange(-npts,npts)*res)
    
    # ds = xr.concat(FIELDcomp,dim='time')
    return alongtrackidx, date_arr, FIELDcomp, FIELDcomp[0].attrs

#Note it is not normalized to eddy radius
def create_eddycomp_dataset(SSHcomp,date_arr,npts,res,SSHattrs,tridx,alongtrackidx,dstracks):
    compSSH=xr.DataArray(data=np.array(SSHcomp).squeeze(),
                 coords={'time':date_arr, 'y':np.arange(-npts,npts)*res, 'x':np.arange(-npts,npts)*res},
                 dims=['time','y','x'],name='KE',attrs=SSHattrs)

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



# %%
#Extract composites along track and save to file
if False:
    path_data          = '/work/mh0033/m300878/crop_interpolate/smtwv/ssh/002deg/exp9_KE_100m_fine.nc'
    # path_data          = '/work/mh0033/m300878/crop_interpolate/smtwv/ssh/002deg/exp9_KE_100m.nc'
    path_save_composite = '/composite_exp9_KE_100m/'
else:
    path_data          = '/work/mh0033/m300878/crop_interpolate/smtwv/ssh/002deg/exp7_KE_100m_fine.nc'
    path_save_composite = '/composite_exp7_KE_100m/'

for tridx in newARtrackid:
    print('Extracting for eddy track ',tridx)

    alongtrackidx, date_arr, SSHcomp, SSHattrs = extract_eddytrack_raw(dstracks,tridx,wavelength,dlon,dlat,res, path=path_data)

    dsSSH   = create_eddycomp_dataset(SSHcomp,date_arr,npts,res,SSHattrs,tridx,alongtrackidx,dstracks)

    fileout = tracker_dir+path_save_composite+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'+str(tridx)+'.nc'
    dsSSH.to_netcdf(fileout)
# %% ######################################################################
eddy_type  = 'cyclonic'
ds = xr.open_dataset(tracker_dir+path_save_composite+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_7.nc')


# %%
