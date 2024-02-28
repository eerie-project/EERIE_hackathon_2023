#!/usr/bin/env python
# coding: utf-8

# 
# Compute KE from geostrophic surface velocities 
#
import sys
yr=sys.argv[1]
mth=sys.argv[2]
yyyy=int(yr)

import glob, os
from subprocess import call
import multiprocessing
from netCDF4 import Dataset
import netCDF4 as nc
import xarray as xr
import numpy as np
import datetime

sys.path.insert(0, r'/home/m/m300466/pyfuncs')
from extractICONdata import *
from edgevertexcell import *

sys.path.append('/work/mh0256/m300466/pyicon')
import pyicon as pyic


run='erc1011'
gname = 'r2b9_oce_r0004'
lev = 'L128'
rgrid_name = 'global_0.05'
path_data     = f'/work/bm1344/k203123/experiments/{run}/'
path_grid     = f'/work/mh0256/m300466/icongrids/grids/{gname}/'
path_ckdtree  = f'{path_grid}ckdtree/'
fpath_ckdtree = f'{path_grid}ckdtree/rectgrids/{gname}_res0.05_180W-180E_90S-90N.npz'
#fpath_fx      = f'{path_grid}{gname}_{lev}_fx.nc'
#fpath_tgrid=f'{path_grid}{gname}_tgrid.nc'
fpath_tgrid=f'/pool/data/ICON/grids/public/mpim/0016/icon_grid_0016_R02B09_O.nc'
print(fpath_tgrid)
#exit(1)

f = Dataset(fpath_tgrid, 'r')
clon = f.variables['clon'][:] * 180./np.pi
clat = f.variables['clat'][:] * 180./np.pi
f.close()

#Fakely use atm model type to substitute for 2D ocean only [runs much faster!!!]
IcDo = pyic.IconData(
    fname        = run+'_oce_2d_1d_mean_20020101T000000Z.nc',
    path_data    = path_data+'run_20020101T000000-20020131T235845/',
    path_grid    = path_grid,
    gname        = gname,
    lev          = lev,
    rgrid_name   = rgrid_name,
    #load_rectangular_grid = False,
    do_triangulation    = False,
    omit_last_file      = False,
    load_vertical_grid = False,
    #calc_coeff          = True,
    #calc_coeff_mappings = False,
    model_type = 'atm',
              )

fpath_ckdtree = IcDo.rgrid_fpath_dict[rgrid_name]
IcDo.fixed_vol_norm = pyic.calc_fixed_volume_norm(IcDo)
IcDo.edge2cell_coeff_cc = pyic.calc_edge2cell_coeff_cc(IcDo)
IcDo.edge2cell_coeff_cc_t = pyic.calc_edge2cell_coeff_cc_t(IcDo)

expid='erc1011'
outdir='/work/mh0287/m300466/EERIE/'+expid+'/geostrophic/'
#ds2d = xr.open_mfdataset(path_data+'run_200[2-8]*/'+expid+'_oce_2d_1d_mean_'+'*T000000Z.nc')
#ds2d = xr.open_mfdataset(path_data+'run_'+str(yyyy)+'*/'+expid+'_oce_2d_1d_mean_'+'*T000000Z.nc')
if float(mth)<10:
    mm='0'+str(int(mth))
else:
    mm=str(int(mth))
ds2d = xr.open_mfdataset(path_data+'run_'+str(yyyy)+mm+'*/'+expid+'_oce_2d_1d_mean_'+'*T000000Z.nc')
#ds3d = xr.open_mfdataset(path_data+'run_200[2-8]*/'+expid+'_oce_ml_1d_mean_'+'*T000000Z.nc')

#Need vorticity grid
dso = xr.open_dataset('/work/mh0287/m300083/experiments/dpp0066/dpp0066_oce_3dlev_P1D_20200909T000000Z.nc')

gridds=xr.open_dataset(fpath_tgrid)
#Coriolis
omega=7.2921159e-5 #radians/second
fCo=2*omega*np.sin(gridds.clat.values)
Colatlim=2 #Coriolis latitude limit
g0=9.81 #gravity 
rho0=1024 #density ref

import numpy.ma as ma
fillval=np.nan
dsmask=gridds['cell_sea_land_mask']
lsmask2=ma.masked_values(np.where(dsmask.values!=-2,fillval,1),fillval)
lsmask=ma.masked_values(np.where(dsmask.values>=0,fillval,1),fillval)

#For daily data:
fdatearrf=ds2d.time.dt.strftime("%Y%m%d.%f")
fdatearr=ds2d.time.dt.strftime("%Y%m%d")
#Need to shift by 12 hours to get the right date
newdatearrflist=[]
newdatearrlist=[]
for tt in range(len(ds2d.time.data)):
    # newdatelist.append(datetime.datetime.strptime(str(ds2d.time.data[tt])[:10], '%Y-%m-%d')-datetime.timedelta(hours=12))
    newdatearrflist.append((datetime.datetime.strptime(str(ds2d.time.data[tt])[:10], '%Y-%m-%d')-datetime.timedelta(hours=12)).strftime("%Y%m%d.%f"))
    newdatearrlist.append((datetime.datetime.strptime(str(ds2d.time.data[tt])[:10], '%Y-%m-%d')-datetime.timedelta(hours=12)).strftime("%Y%m%d"))
newdatearrf=np.array(newdatearrflist)
newdatearr=np.array(newdatearrlist)

#for ii in range(0,1):
#for ii in range(0,np.shape(fdatearr)[0]):
for ii in range(0,len(fdatearr)):
    #fdate=str(fdatearr[ii].values)
    fdate=newdatearr[ii]
    print('Processing for '+fdate)

    print('Extracting SSH')
    ssh=ds2d['ssh'].sel(time=fdatearr[ii]).values.squeeze()
    print('size of ssh=',np.shape(ssh))

    #Compute SSH gradients
    print('Compute gradient (located on edge)')
    print(np.shape(IcDo.adjacent_cell_of_edge))
    gradh_ssh = (ssh[np.newaxis,IcDo.adjacent_cell_of_edge[:,1]]-ssh[np.newaxis,IcDo.adjacent_cell_of_edge[:,0]])*IcDo.grad_coeff
    print('gradh_ssh=',np.shape(gradh_ssh))
    del(ssh)

    print('Project gradient onto cell centers (single level)')
    p_gradh_ssh = edges2cell(IcDo, gradh_ssh)
    print('p_gradhssh=',np.shape(p_gradh_ssh))
    del(gradh_ssh)

    print('Get d/dx and d/dy')
    dSSHdx, dSSHdy = pyic.calc_2dlocal_from_3d(IcDo, p_gradh_ssh)
    print('dSSHdx=',np.shape(dSSHdx))
    print('dSSHdy=',np.shape(dSSHdy))
    del(p_gradh_ssh)
    
    #Compute geostrophic surface velocity and remove noisy data
    ugeo=np.where(np.abs(g0*fCo)<=2*omega*np.sin(Colatlim/180*np.pi),fillval,(-g0/fCo)*dSSHdy)*lsmask2
    vgeo=np.where(np.abs(g0*fCo)<=2*omega*np.sin(Colatlim/180*np.pi),fillval,(g0/fCo)*dSSHdx)*lsmask2
    #ugeo = ma.masked_values(ugeo,fillval)
    #vgeo = ma.masked_values(vgeo,fillval)
    print('ugeo,vgeo = ',np.shape(ugeo))
    del(dSSHdy)
    del(dSSHdx)
    KE = np.sqrt(ugeo**2+vgeo**2)*lsmask2
    geoKE = KE/(rho0*fCo)*(rho0*fCo)
    geoKE = geoKE.squeeze()
    print('Geostrophic surface KE=',np.shape(geoKE))
    del(ugeo)
    del(vgeo)
    del(KE)

    nctime = float(newdatearrf[ii])

    geoKEfile=outdir+'geoKE/dm/'+expid+'_geoKE_dm_'+fdate+'.nc'
    print('Write to '+geoKEfile)
    writenc1d_r2b9O(geoKEfile,nctime,14886338,geoKE,'geoKE','Surface geostrophic kinetic energe','sfc_geostrophic_KE','m2/s2')

    del(geoKE)

    
