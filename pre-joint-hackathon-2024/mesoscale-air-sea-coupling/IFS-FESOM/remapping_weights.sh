#!/bin/sh

#Create variable_on_grid files. 
cdo -select,name=sd,day=1 /work/bm1344/m300466/native/IFS/ifs-fesom_wind_divcurl_197101_gridded.nc /work/mh0256/m300466/ifsfesomgrids/variable_on_tco1279gridpoint.nc
cdo -select,day=1 /work/bm1344/a270228/EERIE_NextG_Hackathon/IFS-FESOM_CONTROL-1950/tco1279-NG5/1971/FESOM/native/daily/fesom_sst_19710101-19710131_daily-NG5.nc /work/mh0256/m300466/ifsfesomgrids/variable_on_NG5node.nc
cdo -daymean -select,name=sd,day=1 /work/bm1344/m300466/native/IFS/test_ifsamip_wind_divcurl_201002_gridded.nc /work/mh0256/m300466/ifsfesomgrids/variable_on_tco399gridpoint.nc

# Create remapping weights from NG5 FESOM native grid to gridded tco1279 IFS (original) grid
cdo -P 24 -gencon,/work/mh0256/m300466/ifsfesomgrids/variable_on_tco1279gridpoint.nc \
    -setgrid,/work/ab0995/a270088/public/grids/NG5_griddes_nodes_IFS.nc \
    /work/mh0256/m300466/ifsfesomgrids/variable_on_NG5node.nc \
  /work/mh0256/m300466/ifsfesomgrids/NG5_to_tco1279gridpoint_conremapweights.nc


#Create weights from tco1279 IFS original grid to IFS25grid
cdo -P 24 -gencon,/work/mh0256/m300466/DPP/grid/temp_IFS25invertlat_MR_gridexample.nc /work/mh0256/m300466/ifsfesomgrids/variable_on_tco1279gridpoint.nc  /work/mh0256/m300466/ifsfesomgrids/tco1279gridpoint_to_IFS25invertlat_conremapweights.nc

# Create weights from NG5 FESOM native grid to IFS25grid
cdo -P 24 -gencon,/work/mh0256/m300466/DPP/grid/temp_IFS25invertlat_MR_gridexample.nc -setgrid,/work/ab0995/a270088/public/grids/NG5_griddes_nodes_IFS.nc /work/mh0256/m300466/ifsfesomgrids/variable_on_NG5node.nc  /work/mh0256/m300466/ifsfesomgrids/NG5_to_IFS25invertlat_conremapweights.nc

#Create weights from tco399(28km) IFS original grid to IFS25grid
cdo -P 24 -gencon,/work/mh0256/m300466/DPP/grid/temp_IFS25invertlat_MR_gridexample.nc /work/mh0256/m300466/ifsfesomgrids/variable_on_tco399gridpoint.nc  /work/mh0256/m300466/ifsfesomgrids/tco399gridpoint_to_IFS25invertlat_conremapweights.nc

