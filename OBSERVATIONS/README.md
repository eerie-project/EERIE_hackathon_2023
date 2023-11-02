# Observations on DKRZ

Notebokks in this folder show simple examples of how to open observations datasets located at DKRZ through [EERIE catalog](https://github.com/eerie-project/intake_catalogues/tree/main).

* AVISO - Satellite derived [Sea Surface Height above Geoid](https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-sea-level-global?tab=overview).
* CERES - Clouds and Earth's Radiant Energy Systems (CERES) Energy Balanced and Filled (EBAF)
* EN4 - ocean climatology. Data v4.2.2_g10 version from 1950 to 2022
* ERA5 - atmospheric reanalysis. There are two versions - monthly means of several basic variables (`era5`) and complete set located on DKRZ in GRIB format (`era5-dkrz`).
* GPM - precipitation. [Integrated Multi-satellitE Retrievals for GPM](https://gpm.nasa.gov/data/imerg). Only years 2020-2021 (untill September) are present.
* MSWEP - precipitation. [Multi-Source Weighted-Ensemble Precipitation](https://www.gloh2o.org/mswep/).
* OSI-SAF - [sea ice products.](https://osi-saf.eumetsat.int/products/sea-ice-products) 
* PHC3 - ocean climatology. [Polar science center Hydrographic Climatology](https://psc.apl.washington.edu/nonwp_projects/PHC/Climatology.html)
* WOA18 - ocean climatology. [World Ocean Atlas 2018](https://www.ncei.noaa.gov/access/world-ocean-atlas-2018/)
* OSTIA - sea surface temperature and sea ice concentrations from [Copernicus Marine Service](https://data.marine.copernicus.eu/product/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/description). Used for [IFS-AMIP runs](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/README.md#ifs). This includes the raw data and processed data: climatology and filtered SST using a variety of filter lengthscales.
