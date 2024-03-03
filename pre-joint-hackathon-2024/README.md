# Pre Joint Hackathon 2024

As preparations for the joint EERIE/NextGEMS hackathon (March 2024), here's a collection of examples particularly for topics on mesoscale eddies and their impact on air-sea coupling, ocean state (physical and BGC) and atmospheric state. 
 - [Eddy identification, tracking and compositing](eddy_track_composite/README.md) of physical (ocean/atmos) and [biogeochemical properties](eddy_track_composite/HAMOCC/README.md)
 - [Spatial filters](mesoscale-air-sea-coupling/Spatial_Filters/README.md) on regular grid
   1. [Weighted area-average smoothing](mesoscale-air-sea-coupling/Spatial_Filters/README.md#weighted-area-average-smoothing-using-cdo) using `cdo -smooth` operator. 
       - [Spatial filtering on HEALpix data](mesoscale-air-sea-coupling/Spatial_Filters/README.md#bonus-spatial-filtering-on-healpix-data).
   2. [Bessel filter](mesoscale-air-sea-coupling/Spatial_Filters/README.md#bessel-filter) using a function from py-eddy-tracker. 
   3. [Gaussian filter](mesoscale-air-sea-coupling/Spatial_Filters/README.md#gaussian-filter) using a function from GCM filters.
 - [Scale dependency of air-sea coupling](mesoscale-air-sea-coupling/README.md)
    - [ICON](mesoscale-air-sea-coupling/ICON/README.md)
    - [IFS/FESOM](mesoscale-air-sea-coupling/IFS-FESOM/README.md)
- [Mean vs eddy fluxes in the ocean](mean_eddy_flux/README.md)
    - [vertical heat fluxes in ICON](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/vertical_heat_flux_ICON_WP6_hackathon.ipynb) by Stella Bērziņa and Matthias Münnich
    - [in-situ or potential density from potential temperature and salinity](mean_eddy_flux/#in-situ-or-potential-density)
    - [find depth of isopycnal surfaces](mean_eddy_flux/#depth-of-isopycnal-surfaces)
