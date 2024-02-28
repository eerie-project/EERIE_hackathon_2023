#!/usr/bin/env python
# coding: utf-8

# 
# Compute SST gradients and windstress curl and divergence. 
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
outdir='/work/mh0287/m300466/EERIE/'+expid+'/'
#ds2d = xr.open_mfdataset(path_data+'run_200[2-8]*/'+expid+'_oce_2d_1d_mean_'+'*T000000Z.nc')
#ds2d = xr.open_mfdataset(path_data+'run_'+str(yyyy)+'*/'+expid+'_oce_2d_1d_mean_'+'*T000000Z.nc')
if float(mth)<10:
    mm='0'+str(int(mth))
else:
    mm=str(int(mth))
#ds2d = xr.open_mfdataset(path_data+'run_'+str(yyyy)+mm+'*/'+expid+'_oce_2d_1d_mean_'+'*T000000Z.nc')
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

dsuas = xr.open_dataset(outdir+'uas/dm/'+expid+'_uas_dm_'+str(yyyy)+mm+'_r2b9O.nc')
dsvas = xr.open_dataset(outdir+'vas/dm/'+expid+'_vas_dm_'+str(yyyy)+mm+'_r2b9O.nc')
#For daily data:
fdatearrf=dsuas.time.dt.strftime("%Y%m%d.%f")
fdatearr=dsuas.time.dt.strftime("%Y%m%d")
##Need to shift by 12 hours to get the right date
#newdatearrflist=[]
#newdatearrlist=[]
#for tt in range(len(ds2d.time.data)):
#    newdatearrflist.append((datetime.datetime.strptime(str(ds2d.time.data[tt])[:10], '%Y-%m-%d')-datetime.timedelta(hours=12)).strftime("%Y%m%d.%f"))
#    newdatearrlist.append((datetime.datetime.strptime(str(ds2d.time.data[tt])[:10], '%Y-%m-%d')-datetime.timedelta(hours=12)).strftime("%Y%m%d"))
#newdatearrf=np.array(newdatearrflist)
#newdatearr=np.array(newdatearrlist)

##For monthly data
#yrmtharr=["2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12","2021-01","2021-02","2021-03","2021-04","2021-05","2021-06","2021-07","2021-08","2021-09","2021-10","2021-11","2021-12","2022-01","2022-02"]
#fdatearr=["20200215","20200315","20200415","20200515","20200615","20200715","20200815","20200915","20201015","20201115","20201215","20210115","20210215","20210315","20210415","20210515","20210615","20210715","20210815","20210915","20211015","20211115","20211215","20220115","20220215"]
#fdatearrf=["20200215.000000","20200315.000000","20200415.000000","20200515.000000","20200615.000000","20200715.000000","20200815.000000","20200915.000000","20201015.000000","20201115.000000","20201215.000000","20210115.000000","20210215.000000","20210315.000000","20210415.000000","20210515.000000","20210615.000000","20210715.000000","20210815.000000","20210915.000000","20211015.000000","20211115.000000","20211215.000000","20220115.000000","20220215.000000"]


#for ii in range(0,1):
for ii in range(0,np.shape(fdatearr)[0]):
#for ii in range(0,len(fdatearr)):
    fdate=str(fdatearr[ii].values)
    #fdate=newdatearr[ii]
    print('Processing for '+fdate)
#    print('Extracting SST')
#    ts=ds2d['to'].isel(depth=0).sel(time=fdatearr[ii]).values.squeeze()
#    print('size of ts=',np.shape(ts))

    print('Extracting uas')
    uas=dsuas['uas'].isel(height_2=0).sel(time=str(fdatearr[ii].values)).values.squeeze()
    #print('size of uas=',np.shape(uas))
    print('Extracting vas')
    vas=dsvas['vas'].isel(height_2=0).sel(time=str(fdatearr[ii].values)).values.squeeze()
    #print('size of vas=',np.shape(vas))

#    #Compute SST gradients
#    print('Compute gradient (located on edge)')
#    print(np.shape(IcDo.adjacent_cell_of_edge))
#    gradh_ts = (ts[np.newaxis,IcDo.adjacent_cell_of_edge[:,1]]-ts[np.newaxis,IcDo.adjacent_cell_of_edge[:,0]])*IcDo.grad_coeff
#    print('gradh_ts=',np.shape(gradh_ts))
#    del(ts)
#
#    print('Project gradient onto cell centers (single level)')
#    p_gradh_ts = edges2cell(IcDo, gradh_ts)
#    print('p_gradhts=',np.shape(p_gradh_ts))
#    del(gradh_ts)
#
#    print('Get d/dx and d/dy')
#    dTdx, dTdy = pyic.calc_2dlocal_from_3d(IcDo, p_gradh_ts)
#    print('dTdx=',np.shape(dTdx))
#    print('dTdy=',np.shape(dTdy))
#    del(p_gradh_ts)
#
#
#    #Compute downwind and crosswind SST gradients
    mwnd=np.sqrt(uas*uas + vas*vas)
    cosphi=uas/mwnd
    sinphi=vas/mwnd
    print('wspd=',np.shape(mwnd))
    print('cosphi=',np.shape(cosphi))
    print('sinphi=',np.shape(sinphi))
    del(mwnd)
    fillval=np.nan

#
#    downT=cosphi*dTdx.squeeze()+sinphi*dTdy.squeeze()
#    crossT=sinphi*dTdx.squeeze()-cosphi*dTdy.squeeze()
#    print('downT=',np.shape(downT))
#    print('crossT=',np.shape(crossT))
#    del(dTdx)
#    del(dTdy)
#
#
#    fillval=-99999
#    downT=np.where(np.isnan(downT),fillval,downT)
#    crossT=np.where(np.isnan(crossT),fillval,crossT)

    # Wind divergence and curl
    print('Project fluxes on 3D sphere')
    p_wnd = pyic.calc_3d_from_2dlocal(IcDo, uas[np.newaxis,:], vas[np.newaxis,:])
    print('p_wnd=',np.shape(p_wnd))
    del(uas)
    del(vas)

    # calculate edge array
    print('Project from cell centre to edges')
    ptp_wnd = pyic.cell2edges(IcDo, p_wnd.squeeze())
    print('ptp_wnd=',np.shape(ptp_wnd))
    del(p_wnd)

    # calculate divergence
    print('div_coeff=',np.shape(IcDo.div_coeff))
    print('edge_of_cell=',np.shape(IcDo.edge_of_cell))
    print('Compute divergence of wind')
    div_wind = (ptp_wnd[np.newaxis,IcDo.edge_of_cell]*IcDo.div_coeff[np.newaxis,:,:]).sum(axis=2)
    print('div_wind=',np.shape(div_wind))
    div_wind=np.where(np.isnan(cosphi),fillval,div_wind)*lsmask2

    # calculate curl
    print('rot_coeff=',np.shape(IcDo.rot_coeff))
    print('edges_of_vertex=',np.shape(IcDo.edges_of_vertex))
    print('Compute curl of wind (single level)')
    ptv_curl_wnd = (ptp_wnd[np.newaxis,IcDo.edges_of_vertex]*IcDo.rot_coeff[np.newaxis,:,:]).sum(axis=2)
    print('curl_wnd=',np.shape(ptv_curl_wnd))
    del(ptp_wnd)
    print('Convert to xarray')
    ptv_curl_wnd=xr.DataArray(ptv_curl_wnd.squeeze(), coords=dict(ncells_3=(["ncells_3"],dso.ncells_2.data)) , dims=["ncells_3"])
    print('Project from vertices to cell centre')
    curl_wind=vertex2cell(ptv_curl_wnd,IcDo)
    print('curl_wind=',np.shape(curl_wind))
    #curl_wind=np.where(np.isnan(cosphi),fillval,curl_wind)
    #curlwind=np.where(np.abs(curl_wind)>=2e-5,fillval,curl_wind)*lsmask2
    curlwind=np.where(np.isnan(cosphi),fillval,curl_wind)*lsmask2
    del(curl_wind)
    del(ptv_curl_wnd)
    del(cosphi)
    del(sinphi)

    #nctime = float(newdatearrf[ii])
    nctime = float(fdatearrf[ii].values)

#    dTfile=outdir+'downSSTgrad/dm/'+expid+'_downSSTgrad_dm_'+fdate+'.nc'
#    print('Write to '+dTfile)
#    writenc1d_r2b9O(dTfile,nctime,14886338,downT,'downSSTgrad','Downwind SST gradient','downwind SST gradient','K/m')
#
#    cTfile=outdir+'crossSSTgrad/dm/'+expid+'_crossSSTgrad_dm_'+fdate+'.nc'
#    print('Write to '+cTfile)
#    writenc1d_r2b9O(cTfile,nctime,14886338,crossT,'crossSSTgrad','Crosswind SST gradient','crosswind SST gradient','K/m')

    divfile=outdir+'winddiv/dm/'+expid+'_winddiv_dm_'+fdate+'.nc'
    print('Write to '+divfile)
    writenc1d_r2b9O(divfile,nctime,14886338,div_wind.squeeze(),'winddiv','Wind divergence','wind_divergence','1/s')

    curlfile=outdir+'windcurl/dm/'+expid+'_windcurl_dm_'+fdate+'.nc'
    print('Write to '+curlfile)
    #writenc1d_r2b9O(curlfile,nctime,7487687,curl_wind.squeeze(),'windcurl','Wind curl','wind_curl','1/s')
    writenc1d_r2b9O(curlfile,nctime,14886338,curlwind.squeeze(),'windcurl','Wind curl','wind_curl','1/s')

#    del(downT)
#    del(crossT)
    del(div_wind)
    del(curlwind)



