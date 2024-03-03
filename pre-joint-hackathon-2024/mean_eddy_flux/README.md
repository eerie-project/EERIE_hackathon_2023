# Deciphering eddy from mean component of fluxes
Some examples on:
  - [vertical heat fluxes in ICON](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/vertical_heat_flux_ICON_WP6_hackathon.ipynb) by Stella Bērziņa and Matthias Münnich
  - how to compute [in-situ or potential density from potential temperature and salinity](#in-situ-or-potential-density)
  - [find depth of isopycnal surfaces](#depth-of-isopycnal-surfaces)
  - compute/[interpolate quantity onto isopycnal surface](#interpolate-onto-isopycnal-surfaces) (work in progress!)


## In-situ or potential density
Compute in-situ density
```bash
ocefile=/work/bm1344/k203123/experiments/erc1011/run_20391101T000000-20391130T235845/erc1011_oce_ml_1mth_mean_20391201T000000Z.nc
cdo -P 24 -rhopot -adisit -chname,to,tho,so,sao -select,name=to,so ${ocefile} insitu_rho_erc1011_mm_203912.nc
```

Compute potential density (ref 2000m, 200 bar)
```bash
cdo -P 24 -rhopot,200 -adisit,200 -chname,to,tho,so,sao -select,name=to,so ${ocefile} rhopoto_sigma2_erc1011_mm_203912.nc
```

Compute potential density (ref surface, 0 bar)
```bash
cdo -P 24 -rhopot,0 -adisit,0 -chname,to,tho,so,sao -select,name=to,so ${ocefile} rhopoto_sigma0_erc1011_mm_203912.nc
```

## Depth of isopycnal surfaces
```bash
rhofile=insitu_rho_erc1011_mm_203912.nc
cdo -chname,rhopoto,isodepth -isosurface,1026.0 ${rhofile} isodepths_10260.nc
cdo -chname,rhopoto,isodepth -isosurface,1026.2 ${rhofile} isodepths_10262.nc
cdo -chname,rhopoto,isodepth -isosurface,1026.4 ${rhofile} isodepths_10264.nc
cdo -chname,rhopoto,isodepth -isosurface,1026.6 ${rhofile} isodepths_10266.nc
cdo -chname,rhopoto,isodepth -isosurface,1026.8 ${rhofile} isodepths_10268.nc
cdo -chname,rhopoto,isodepth -isosurface,1027.0 ${rhofile} isodepths_10270.nc
cdo merge isodepths_102*.nc isodepths.nc
ncap2 -O -h -s 'sfc(:)={1026.0,1026.2,1026.4,1026.6,1026.8,1027.0}' isodepths.nc isodepths.nc
ncatted -O -h -a standard_name,isodepth,m,c,"isopycnal_depth" isodepths.nc
ncatted -O -h -a long_name,isodepth,m,c,"depth of isopycnals" isodepths.nc
ncatted -O -h -a units,isodepth,m,c,"m" isodepths.nc
ncatted -O -h -a code,isodepth,d,, isodepths.nc
ncatted -O -h -a positive,depth,c,c,"down" isodepths.nc
```

## Interpolate onto isopycnal surfaces
**(Not working, this is work in progress!)**
```bash
fxfile=/work/mh0256/m300466/icongrids/grids/r2b9_oce_r0004/R2B9L72_fx.nc
srcdepthfile=R2B9L72_depth.nc
interp_rhofile=rho_on_isopyc_erc1011_203912.nc

#cdo -select,name=depth_CellMiddle ${fxfile} ${srcdepthfile}
#cdo -intlevel3d,isodepths.nc ${rhofile} ${srcdepthfile} ${int_rhofile}
```

