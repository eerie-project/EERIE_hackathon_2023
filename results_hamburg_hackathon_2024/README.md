# Post Joint Hackathon 2024

Hackathon was a success! Here's a collection of material from the hackathon. 

- Starter pack pad translated to markdown file in this repo. 

As preparations for the joint EERIE/NextGEMS hackathon (March 2024), here's a collection of examples particularly for topics on mesoscale eddies and their impact on air-sea coupling, ocean state (physical and BGC) and atmospheric state. 
 - [Eddy identification, tracking and compositing](eddy_track_composite/README.md) of physical (ocean/atmos) and biogeochemical properties
    - ICON (read-in netcdf; serial running): [identify and track eddies](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-IDtrackcompeddy-daily.ipynb), [build eddy composites](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-eddycompositeotherfields-daily.ipynb), [plot composites](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-plot-eddycompositesalongtrack-dm.ipynb) by Dian Putrasahan
    - ICON (read-in netcdf; parallel running): [py-eddy-tracker parameter sensitivity experiment](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_parallel_computing) by Arjun Kumar
    - ICON ([parallelise eddy identification code](eddy_track_composite/ICON/identify_fast.py) and [compositing with higher res data](eddy_track_composite/ICON/composite_tracks.py) than 0.25deg by Moritz Epke
    - ICON ([read-in as xarray; parallel running](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_xarray_dask_parallel)) by Aaron Wienkers
    - [IFS-AMIP](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/eddy_composites-short.ipynb) (atm response) by Matthias Aengenheyster
    - [IFS/FESOM](eddy_track_composite/IFS-FESOM/IDtrackeddy-daily-intake_IFSFESOM.ipynb) (use intake and read-in as xarray; parallel running) by Aaron Wienkers and Dian Putrasahan
    - [HAMOCC](eddy_track_composite/HAMOCC/README.md) (read-in netcdf; serial running) by Johann Jungclaus and Dian Putrasahan
 - [Spatial filters](mesoscale-air-sea-coupling/Spatial_Filters/README.md) on regular grid
    1. [Weighted area-average smoothing](mesoscale-air-sea-coupling/Spatial_Filters/README.md#weighted-area-average-smoothing-using-cdo) using `cdo -smooth` operator
        - [Spatial filtering on HEALpix data](mesoscale-air-sea-coupling/Spatial_Filters/README.md#bonus-spatial-filtering-on-healpix-data)
    2. [Bessel filter](mesoscale-air-sea-coupling/Spatial_Filters/README.md#bessel-filter) using a function from py-eddy-tracker by Dian Putrasahan
    3. [Gaussian filter](mesoscale-air-sea-coupling/Spatial_Filters/README.md#gaussian-filter) using a function from GCM filters by Matthias Aengenheyster and Dian Putrasahan
 - [Scale dependency of air-sea coupling](mesoscale-air-sea-coupling/README.md)
    - [ICON](mesoscale-air-sea-coupling/ICON/README.md) by Dian Putrasahan
    - [IFS/FESOM](mesoscale-air-sea-coupling/IFS-FESOM/README.md) by Matthias Aengenheyster, Rohit Ghosh and Dian Putrasahan
- [Mean vs eddy fluxes in the ocean](mean_eddy_flux/README.md)
    - [vertical heat fluxes in ICON](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/vertical_heat_flux_ICON_WP6_hackathon.ipynb) by Stella Bērziņa and Matthias Münnich
    - [in-situ or potential density from potential temperature and salinity](mean_eddy_flux/#in-situ-or-potential-density)
    - [find depth of isopycnal surfaces](mean_eddy_flux/#depth-of-isopycnal-surfaces)
- Impact of eddies on atmosphere mean state (IFS-AMIP)
    - [2D atm clim state](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_atmosresponse_to_SST_forcing_djf_clmdiff.ipynb) by Iuliia Polkova
    - [3D atm clim state](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_atmosresponse_to_SST_forcing_djf_clmdiff_3D.ipynb) by Iuliia Polkova
    - [atm covariability/correlation](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_atmosresponse_to_SST_forcing_djf_correlation.ipynb) by Iuliia Polkova
    - [local atm response (composites)](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_composites.ipynb) by Chris Roberts and Matthias Aengenheyster
 
