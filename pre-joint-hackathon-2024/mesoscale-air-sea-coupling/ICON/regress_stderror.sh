#!/bin/sh

########################### High-pass 3deg filtered data ###################################
### DJF ###
#Regression
mkdir -p /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/
#TAUmag on SST
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taumag_on_to_dm_IFS25_30dayrmn_hp3deg_DJF.nc
#taucurl on sfcvort
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_DJF.nc
#taucurl on crossSSTgrad
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_hp3deg_DJF.nc
#taudiv on downSSTgrad
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_hp3deg_DJF.nc
#windcurl on sfcvort
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_windcurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_DJF.nc
#wspd10 on SST
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_hp3deg_DJF.nc

#Standard Error
neff=40        #(180/30)*7 -2
cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taumag_on_to_dm_IFS25_30dayrmn_hp3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_hp3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_hp3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_windcurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_hp3deg_DJF.nc


### JJA ###
#Regression
cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taumag_on_to_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_windcurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_hp3deg_JJA.nc

#Standard Error
neff=40        #(180/30)*7 -2
cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taumag_on_to_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_windcurl_on_sfcvort_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_hp3deg_JJA.nc

########################### Smoothed 3deg data ##########################################
### DJF ###
#Regression
mkdir -p /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taumag_on_to_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_windcurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_sm3deg_DJF.nc

#Standard Error
neff=40        #(180/30)*7 -2
cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taumag_on_to_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_windcurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_sm3deg_DJF.nc

### JJA ###
#Regression
cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taumag_on_to_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_windcurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_sm3deg_JJA.nc

#Standard Error
neff=40        #(180/30)*7 -2
cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/3deg/erc1011_taumag_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taumag_on_to_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/3deg/erc1011_crossSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/3deg/erc1011_taudiv_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/3deg/erc1011_downSSTgrad_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/3deg/erc1011_sfcvort_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_windcurl_on_sfcvort_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/3deg/erc1011_Wind_Speed_10m_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/3deg/erc1011_to_1_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_sm3deg_JJA.nc

########################### total field data ##########################################
### DJF ###
#Regression
mkdir -p /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/
cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/erc1011_taumag_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taumag_on_to_dm_IFS25_30dayrmn_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_sfcvort_dm_IFS25_30dayrmn_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/erc1011_crossSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/erc1011_crossSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/erc1011_taudiv_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/erc1011_downSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/erc1011_downSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/erc1011_windcurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_windcurl_on_sfcvort_dm_IFS25_30dayrmn_DJF.nc

cdo -div -timcovar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/erc1011_Wind_Speed_10m_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_DJF.nc

#Standard Error
neff=40        #(180/30)*7 -2
cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/erc1011_taumag_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taumag_on_to_dm_IFS25_30dayrmn_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_sfcvort_dm_IFS25_30dayrmn_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/erc1011_crossSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/erc1011_taudiv_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/erc1011_downSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/erc1011_windcurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_windcurl_on_sfcvort_dm_IFS25_30dayrmn_DJF.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/erc1011_Wind_Speed_10m_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_DJF.nc

### JJA ###
#Regression
cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/erc1011_taumag_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taumag_on_to_dm_IFS25_30dayrmn_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_sfcvort_dm_IFS25_30dayrmn_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/erc1011_crossSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/erc1011_crossSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/erc1011_taudiv_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/erc1011_downSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/erc1011_downSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/erc1011_windcurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_windcurl_on_sfcvort_dm_IFS25_30dayrmn_JJA.nc

cdo -div -timcovar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/erc1011_Wind_Speed_10m_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/regress_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_JJA.nc

#Standard Error
neff=40        #(180/30)*7 -2
cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taumag/erc1011_taumag_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taumag_on_to_dm_IFS25_30dayrmn_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_sfcvort_dm_IFS25_30dayrmn_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/crossSSTgrad/erc1011_crossSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taucurl_on_crossSSTgrad_dm_IFS25_30dayrmn_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taudiv/erc1011_taudiv_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/downSSTgrad/erc1011_downSSTgrad_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_taudiv_on_downSSTgrad_dm_IFS25_30dayrmn_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/erc1011_windcurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/sfcvort/erc1011_sfcvort_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_windcurl_on_sfcvort_dm_IFS25_30dayrmn_JJA.nc

cdo -sqrt -divc,${neff} -div -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/Wind_Speed_10m/erc1011_Wind_Speed_10m_dm_20020101-20081231_IFS25_30dayrmn.nc ] -timvar -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/to/erc1011_to_1_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/regress/stderror_Wind_Speed_10m_on_to_dm_IFS25_30dayrmn_JJA.nc

#########################################################################################################
##Correlation between windcurl and stresscurl
###high-pass 3deg filtered data
mkdir -p /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr
cdo -timcor -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr/timecorr_taucurl_windcurl_dm_IFS25_30dayrmn_hp3deg_JJA.nc

cdo -timcor -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_hp3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr/timecorr_taucurl_windcurl_dm_IFS25_30dayrmn_hp3deg_DJF.nc

###smoothed 3deg data
cdo -timcor -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr/timecorr_taucurl_windcurl_dm_IFS25_30dayrmn_sm3deg_JJA.nc

cdo -timcor -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/3deg/erc1011_taucurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/3deg/erc1011_windcurl_dm_??????_IFS25_30dayrmn_sm3deg.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr/timecorr_taucurl_windcurl_dm_IFS25_30dayrmn_sm3deg_DJF.nc

### total field data
cdo -timcor -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=JJA [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/erc1011_windcurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr/timecorr_taucurl_windcurl_dm_IFS25_30dayrmn_JJA.nc

cdo -timcor -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/taucurl/erc1011_taucurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] -select,season=DJF [ /work/bm1344/k203123/reg25/erc1011/30dayrunmean/windcurl/erc1011_windcurl_dm_20020101-20081231_IFS25_30dayrmn.nc ] /work/bm1344/k203123/reg25/erc1011/30dayrunmean/timecorr/timecorr_taucurl_windcurl_dm_IFS25_30dayrmn_DJF.nc
