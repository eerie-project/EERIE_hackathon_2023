#!/usr/bin/env python
# coding: utf-8

# ## Example for eddy compositing along tracked eddy based on daily data using py-eddy-tracker
# ### Extraction of eddy along the track (SSH fields)
# eddy_fromfile_alongtrack_dm_erc1011.py
# ### Pull out other fields associated with tracked eddy
# othereddyfields_fromfile_alongtrack_dm_erc1011.py
# 
# 
import sys
varname=sys.argv[1]
eddy_type=sys.argv[2]
rgn=sys.argv[3]

# eddy_type='cyclonic'
# eddy_type='anticyclonic'

import os 
import numpy as np
from datetime import datetime, timedelta
import xarray as xr

figpath='/home/m/m300466/iconfigs/EERIE/hamocc/eddytrack/'

expid='ngc_72lev_HAM_prod'
fq='dm'
wavelength=400  #choice of spatial cutoff for high pass filter in km
pixel_limit=(20, 500)  # Min and max pixel count for valid contour
shape_error=55  # Error max (%) between ratio of circle fit and contour

eddydir='/work/bm1344/m300466/reg25/'+expid+'/eddytrack/sm'+str(wavelength)+'km/se'+str(shape_error)+'/pixmin'+str(pixel_limit[0])+'/pixmax'+str(pixel_limit[1])+'/'
tracker_dir=eddydir+'tracks/'
figpath='/home/m/m300466/iconfigs/EERIE/hamocc/eddytrack/'
figprefix=figpath+expid+'_'+rgn+'_'+eddy_type+'_'

#dscorres = xr.open_dataset(tracker_dir+expid+'_'+eddy_type+'_'+fq+'_correspondance.nc')
dstracks = xr.open_dataset(tracker_dir+eddy_type+'_tracks.nc')
#dsshort = xr.open_dataset(tracker_dir+eddy_type+'_short.nc')
#dsuntrack = xr.open_dataset(tracker_dir+eddy_type+'_untracked.nc')

dlon=2.5
dlat=2.5
res=0.25
npts=int(dlon/res) #number of points from centre

fprefix=tracker_dir+rgn+'/'+expid+'_'+rgn+'_'+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'
vprefix=tracker_dir+rgn+'/'+varname+'/'+varname+'_'+rgn+'_'+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'


##########################################################################

from matplotlib import pyplot as plt
from matplotlib.pyplot import cm 
# from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER,LATITUDE_FORMATTER
import matplotlib.ticker as mticker

def get_trackid(rgn,dstracks):
    #Get desired region 
    if rgn=='SO': 
        ARidx = np.argwhere((dstracks.latitude.values<=-40) & (dstracks.latitude.values>=-65))
        mindays=10 #min number of days for tracked eddy    
    elif rgn=='AR': 
        ARidx = np.argwhere((dstracks.latitude.values<=-30) & (dstracks.latitude.values>=-45) & 
                (dstracks.longitude.values>0) & (dstracks.longitude.values<25))
        mindays=60 #min number of days for tracked eddy
    elif rgn=='NB': 
        ARidx = np.argwhere(((dstracks.latitude.values<=10) & (dstracks.latitude.values>=0.5) & 
            (dstracks.longitude.values>300)) & (dstracks.longitude.values<320))
        mindays=10 #min number of days for tracked eddy
    elif rgn=='LC': 
        ARidx = np.argwhere(((dstracks.latitude.values<=30) & (dstracks.latitude.values>=20) &
            (dstracks.longitude.values>270)) & (dstracks.longitude.values<280))
        mindays=10 #min number of days for tracked eddy

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

    return newARtrackid

def build_composite(newARtrackid,fprefix,vprefix,varname):
    FIELDcomp=[]
    SSHcomp=[]
    for tridx in newARtrackid:
        # tridx=newARtrackid[0]
        print('Load fields for eddy track ',tridx)
    
        #Load composite dataset
        zosfileout=fprefix+str(tridx)+'.nc'
        varfileout=vprefix+str(tridx)+'.nc'
        dsSSH=xr.open_dataset(zosfileout)
        dsFIELD=xr.open_dataset(varfileout)
        # print('Lifetime of eddy# '+str(tridx)+' = '+ str(len(dsSSH.n)))
        #print('eddy center (lon,lat) = ('+str(dsSSH.lon.values.mean())+', '+str(dsSSH.lat.values.mean())+')')
    
        FIELDpercomp=dsFIELD[varname]
        SSHpercomp=dsSSH.zos
        #print(FIELDpercomp.shape)
        #mean of each eddy
        FIELDcomp.append(xr.concat(FIELDpercomp[:,:,:],dim='eddy').mean(dim='eddy'))
        SSHcomp.append(xr.concat(SSHpercomp[:,:,:],dim='eddy').mean(dim='eddy'))
    
    avgSSHcomp=xr.concat(SSHcomp,dim='eddy').mean(dim='eddy')
    avgFIELDcomp=xr.concat(FIELDcomp,dim='eddy').mean(dim='eddy')
    return avgSSHcomp, avgFIELDcomp

def plot_composite(avgSSHcomp,avgFIELDcomp,varname,vmin,vmax,plot_title,figprefix):
    fig = plt.figure(figsize=(6, 5))
    #ax = fig.add_axes([0.05, 0.03, 0.90, 0.94])
    ax = fig.add_axes([0.05, 0.05, 0.94, 0.92])
    CM=ax.pcolormesh(avgFIELDcomp.x,avgFIELDcomp.y,avgFIELDcomp,cmap='RdBu_r',shading='gouraud',vmin=vmin,vmax=vmax)
    CS=ax.contour(avgSSHcomp.x,avgSSHcomp.y,avgSSHcomp,levels=[0.,0.1,0.2,0.3],colors='k')
    ax.clabel(CS, fontsize=9, inline=True)
    plt.colorbar(CM,orientation='vertical')
    # ax.set_xlim(-2,2)
    # ax.set_ylim(-2,2)
    ax.set_title(plot_title)
    fig.savefig(figprefix+varname+'_20200101-20201225.png')

####################################################################################
newARtrackid=get_trackid(rgn,dstracks)
avgSSHcomp,avgFIELDcomp = build_composite(newARtrackid,fprefix,vprefix,varname)

fac=1
if varname=='to':
    vmin=-0.6
    vmax=0.6
elif varname=='so':
    vmin=-0.1
    vmax=0.1
elif varname=='mlotst':
    vmin=-25
    vmax=25
elif varname=='Wind_Speed_10m':
    vmin=-0.15
    vmax=0.15
elif varname=='sea_level_pressure':
    vmin=-5
    vmax=5
elif varname=='atmos_fluxes_HeatFlux_Latent':
    vmin=-15
    vmax=15
elif varname=='atmos_fluxes_HeatFlux_Sensible':
    vmin=-15
    vmax=15
elif varname=='atmos_fluxes_FrshFlux_Precipitation':
    vmin=-0.2
    vmax=0.2
    fac=1000*86400/1000 #convert from kg/m2/s to mm/day
#declare -a varnamearr=("co2flux" "o2flux" "pco2" "coex90" "NPP" "dissic" "dissoc" "phyp" "phydiaz" "det" "talk" "no3" "po4" "o2" "delcar" "delsil")
#declare -a varnamearr=("calex90" "opex90" "wpoc" "remin" "hi")
elif varname=='co2flux':
    vmin=-5e-12
    vmax=5e-12
elif varname=='o2flux':
    vmin=-1e-10
    vmax=1e-10
elif varname=='pco2':
    vmin=-5e0
    vmax=5e0
elif varname=='coex90':
    vmin=-1e-14
    vmax=1e-14
elif varname=='NPP':
    vmin=-1e-14
    vmax=1e-14
elif varname=='dissic':
    vmin=-5e-6
    vmax=5e-6
    fac=1
elif varname=='dissoc':
    vmin=-1e-8
    vmax=1e-8
    fac=1
elif varname=='phyp':
    vmin=-3e-9
    vmax=3e-9
    fac=1
elif varname=='phydiaz':
    vmin=-3e-11
    vmax=3e-11
    fac=1
elif varname=='det':
    vmin=-5e-10
    vmax=5e-10
elif varname=='talk':
    vmin=-5e-6
    vmax=5e-6
elif varname=='no3':
    vmin=-1e-6
    vmax=1e-6
elif varname=='po4':
    vmin=-5e-8
    vmax=5e-8
elif varname=='o2':
    vmin=-5e-6
    vmax=5e-6
elif varname=='delcar':
    vmin=-5e-15
    vmax=5e-15
elif varname=='delsil':
    vmin=-5e-14
    vmax=5e-14

plot_title=varname+' for '+rgn+' region ('+eddy_type+')'
plot_composite(avgSSHcomp,avgFIELDcomp*fac,varname,vmin,vmax,plot_title,figprefix)

################################################################################
### Evolution of composites

#### In[111]:
###varname='to'
###seg=10
###if varname=='to':
###    vmin=-0.6
###    vmax=0.6
###
###for segidx in range(22):
#### for segidx in np.arange(0,20):
###    FIELDcomp=[]
###    SSHcomp=[]
###    for tridx in newARtrackid:
###        # print('Load fields for eddy track ',tridx)
###        #Load composite dataset
###        fileout=tracker_dir+expid+'_'+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'+str(tridx)+'.nc'
###        dsFIELD=xr.open_dataset(fileout)
###        # print('Lifetime of eddy# '+str(tridx)+' = '+ str(len(dsFIELD.n)))
###        # print('eddy center (lon,lat) = ('+str(dsFIELD.lon.values.mean())+', '+str(dsFIELD.lat.values.mean())+')')
###
###        FIELDpercomp=dsFIELD[varname]
###        SSHpercomp=dsFIELD.ssh
###        # print(FIELDpercomp.shape)
###        if FIELDpercomp.shape[0]>=((segidx+1)*seg):
###            #Mean of each eddy
###            FIELDcomp.append(xr.concat(FIELDpercomp[segidx*seg:(segidx+1)*seg,:,:],dim='eddy').mean(dim='eddy'))
###            SSHcomp.append(xr.concat(SSHpercomp[segidx*seg:(segidx+1)*seg,:,:],dim='eddy').mean(dim='eddy'))
###        del FIELDpercomp
###        del SSHpercomp
###        
###    avgSSHcomp=xr.concat(SSHcomp,dim='eddy').mean(dim='eddy')
###    avgFIELDcomp=xr.concat(FIELDcomp,dim='eddy').mean(dim='eddy')
###    
###    fig = plt.figure(figsize=(5, 4))
###    ax = fig.add_axes([0.05, 0.03, 0.90, 0.94])
###    CM=ax.pcolormesh(avgFIELDcomp.x,avgFIELDcomp.y,avgFIELDcomp,cmap='RdBu_r',shading='gouraud',vmin=vmin,vmax=vmax)
###    CS=ax.contour(avgSSHcomp.x,avgSSHcomp.y,avgSSHcomp,levels=[0.,0.1,0.2,0.3],colors='k')
###    ax.clabel(CS, fontsize=9, inline=True)
###    plt.colorbar(CM,orientation='vertical')
###    ax.set_title('Composite for day '+str(segidx*seg)+' to '+str((segidx+1)*seg)+' ('+str(np.shape(SSHcomp)[0])+' eddies)')
###    del avgFIELDcomp
###    del avgSSHcomp
###    del FIELDcomp
###    del SSHcomp
###    
###
###
#### In[130]:
###
###
###varname='mlotst10'
###seg=10
###if varname=='to':
###    vmin=-0.6
###    vmax=0.6
###elif varname=='mlotst10':
###    vmin=-25
###    vmax=25
###
###for segidx in range(22):
#### for segidx in np.arange(0,20):
###    FIELDcomp=[]
###    SSHcomp=[]
###    for tridx in newARtrackid:
###        # print('Load fields for eddy track ',tridx)
###        #Load composite dataset
###        fileout=tracker_dir+expid+'_'+eddy_type+'_'+str(dlon)+'x'+str(dlat)+'deg_trackID_'+str(tridx)+'.nc'
###        dsFIELD=xr.open_dataset(fileout)
###        # print('Lifetime of eddy# '+str(tridx)+' = '+ str(len(dsFIELD.n)))
###        # print('eddy center (lon,lat) = ('+str(dsFIELD.lon.values.mean())+', '+str(dsFIELD.lat.values.mean())+')')
###
###        FIELDpercomp=dsFIELD[varname]
###        SSHpercomp=dsFIELD.ssh
###        # print(FIELDpercomp.shape)
###        if FIELDpercomp.shape[0]>=((segidx+1)*seg):
###            #Mean of each eddy
###            FIELDcomp.append(xr.concat(FIELDpercomp[segidx*seg:(segidx+1)*seg,:,:],dim='eddy').mean(dim='eddy'))
###            SSHcomp.append(xr.concat(SSHpercomp[segidx*seg:(segidx+1)*seg,:,:],dim='eddy').mean(dim='eddy'))
###        del FIELDpercomp
###        del SSHpercomp
###        
###    avgSSHcomp=xr.concat(SSHcomp,dim='eddy').mean(dim='eddy')
###    avgFIELDcomp=xr.concat(FIELDcomp,dim='eddy').mean(dim='eddy')
###    
###    fig = plt.figure(figsize=(5, 4))
###    ax = fig.add_axes([0.05, 0.03, 0.90, 0.94])
###    CM=ax.pcolormesh(avgFIELDcomp.x,avgFIELDcomp.y,avgFIELDcomp,cmap='RdBu_r',shading='gouraud',vmin=vmin,vmax=vmax)
###    CS=ax.contour(avgSSHcomp.x,avgSSHcomp.y,avgSSHcomp,levels=[0.,0.1,0.2,0.3],colors='k')
###    ax.clabel(CS, fontsize=9, inline=True)
###    plt.colorbar(CM,orientation='vertical')
###    ax.set_title('Composite for day '+str(segidx*seg)+' to '+str((segidx+1)*seg)+' ('+str(np.shape(SSHcomp)[0])+' eddies)')
###    del avgFIELDcomp
###    del avgSSHcomp
###    del FIELDcomp
###    del SSHcomp
###    


