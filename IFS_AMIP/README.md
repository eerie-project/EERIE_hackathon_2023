# IFS data from IFS-AMIP simulations done at ECMWF

Contact: Matthias Aengenheyster @mattphysics, matthias.aengenheyster@ecmwf.int

**For an immediate start with the data, look at the notebook "STARTHERE_IFS_production.ipynb". Continue reading for more information on the simulations.**

**For interactive browsing of the available data on Levante, including interactive visualization, check the [STAC catalogue]([url](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/stac-browser/index.html#/external/raw.githubusercontent.com/eerie-project/intake_catalogues/refs/heads/main/dkrz/disk/stac-templates/catalog-experiments.json?.language=en)) and look for "ifs-amip"**

We make available the IFS-AMIP production runs (indicated by version "v20240901") for EERIE, as well as six preliminary low-resolution (tco399, approximately 28 km) IFS-AMIP simulations. For ease of the analysis, most of the data provided for the hackathon has been regridded to a 0.25 degree regular grid. We do provide *some* 2D data on the native grid. The data is primarily accessible through the intake catalogue structure on DKRZ (some data is also on Jasmin, more below).

AMIP runs are atmosphere-only runs, without an ocean model, forced with sea surface temperature (SST) and sea ice concentration (SIC).

We have conducted two primary *types* of runs: 
1. historical ("hist") runs, that is AMIP runs initialized from ERA5 and forced with observed SST and sea ice (for the production runs, this is ESA-CCI v3).
2. idealized runs where either the SST anomaly or the SST climatology has been low-pass filtered to remove the time-varying mesoscale, or climatological fronts. These are labeled by the kind of filtering, e.g. "hist-c-0-a-lr20" indicates no filtering to the climatology ("c-0") and filtering to the anomalies with 20 times the local Rossby radius ("a-lr20"). 

A large number of variables have been provided at various frequencies, and even more are available on request. The native catalouges contain the year 2023 for all available variables and frequencies. Please explore the catalogues through "intake" (see the notebooks) or the [STAC catalogue]([url](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/stac-browser/index.html#/external/raw.githubusercontent.com/eerie-project/intake_catalogues/refs/heads/main/dkrz/disk/stac-templates/catalog-experiments.json?.language=en)). 

For the preliminary runs, you can explore available variables through the *metadata* directory and its searchable \<exp\>__\<stream\> .csv files listing the metadata for each variable. Additional information on ECMWF variables is available in the [ECMWF Parameter Database](https://codes.ecmwf.int/grib/param-db/) which can be searched by short name, GRIB code, units etc. Particular care is advised for flux data (precipitation, surface heat fluxes etc.) which may be provided either as *rates* (e.g. m/s, W/m^2, typical for monthly means) or as *accumulations* (e.g. m, J/m^2, typical for high-frequency output).

In preliminary runs SST and SIC were taken from the OSTIA dataset (also available under #OBSERVATIONS), while for the production runs ESA-CCI v3 was used instead for better data quality (especially in the early period).

| Catalogue | Experiment | Version | Resolution | Expver | Runname (deprecated)  | Date Range  |  SST      |
|-----------|------------|---------|------------|--------|-----------------------|-------------|-----------|
| ifs&#8209;amip&#8209;tco1279 | hist | v20240901 | tco1279 (~9km) | 0001 | -- | 1980 - 2023 | ESA-CCI v3 |
| ifs-amip-tco399 | hist | v20240901 | tco399 (~28km) | 0002 | -- | 1980 - 2023 | ESA-CCI v3 |
| ifs&#8209;amip&#8209;tco1279 | hist-c-0-a-lr20 | v20240901 | tco1279 (~9km) | 0003 | -- | 1980 - 2023 | ESA-CCI v3, anomalies smoothed with 20 x Rossby radius |
| ifs-amip-tco399 | hist-c-0-a-lr20 | v20240901 | tco399 (~28km) | 0004 | -- | 1980 - 2023 | ESA-CCI v3, anomalies smoothed with 20 x Rossby radius |
| ifs-amip-tco399 | hist-c-lr20-a-0 | v20240901 | tco399 (~28km) | 0006 | -- | 1980 - 2023 | ESA-CCI v3, climatology smoothed with 20 x Rossby radius |
||
| ifs-amip-tco399 | hist | v20240304 | tco399 (~28km) | iabh | amip-hist-esav3      | 2020 - 2021-09 | unfiltered OSTIA SST
| ifs-amip-tco399 | hist-c-0-a-lr30 | v20240304 | tco399 (~28km) | iaou | amip-hist-esav3-c-0-a-lr30 | 2020 | OSTIA SST, with daily *anomalies* smoothed with 30 x Rossby radius
||
| ifs-amip-tco399 | hist | v20231106 | tco399 (~28km) | i6ps | amip-hist-obs      | 2010 - 2020 | unfiltered OSTIA SST
| ifs-amip-tco399 | hist-c-0-a-lr30 | v20231106 | tco399 (~28km) | i6pt | amip-hist-obs-lr30 | 2010 - 2020 | OSTIA SST, with daily *anomalies* smoothed with 30 x Rossby radius
| ifs-amip-tco399 | hist-c-lr30-a-0 | v20231106 | tco399 (~28km) | i7j7 | amip-hist-obs-c-lr30-a-0.atmos.gr025      | 2010 - 2020 | OSTIA SST, with daily *climatology* smoothed with 30 x Rossby radius
| ifs-amip-tco399 | hist&#8209;c&#8209;lr30&#8209;a&#8209;lr30 | v20231106 | tco399 (~28km) | i7j8 | amip-hist-obs-c-lr30-a-lr30.atmos.gr025 | 2010 - 2020 | OSTIA SST, with both *climatology* and *anomalies* smoothed with 30 x Rossby radius
||
| ifs-amip-tco399 | hist | v20231006 | tco399 (~28km) | -- | amip-ng-obs        | 2020-01-20 - 2021 | unfiltered OSTIA SST
| ifs-amip-tco399 | hist-c-0-a-lr30 | v20231006 | tco399 (~28km) | -- | amip-ng-obs-lr30   | 2020-01-20 - 2021 | OSTIA, with daily SST *anomalies* smoothed with 30 x Rossby radius

Dates are inclusive (only year implies full year available, year-month implies full month is available).

## Versions:
* v20240901: Production runs, should be used unless otherwise indicated.
* v20231006: Preliminary runs for the 2023 EERIE GA & Hackathon using NextGEMS cycle 3 configuration using OSTIA SST
* v20231106: Preliminary runs for the 2023 EERIE GA & Hackathon using prepIFS based on IFS CY48R1.1 using OSTIA SST
* v20240304: Preliminary runs for the 2024 Joing EERIE/nextGEMS Hackathon using prepIFS based on IFS CY48R1.1 using ESA-CCI v3 SST

The "hist" runs are historical runs with time-dependent forcing based on IFS CY48R1.1, including some new EERIE source updates.
The "ng" runs use the NextGEMS cycle 3 configuration, i.e. perpetual 2020 forcing (except for SST & SIC).

## Data structure:
The data is organized in streams by frequency, 2D/3D and grid (primarily at 0.25 degree, though some native data is available) 
* 2D_6h_native: 6-hourly snapshots and accumulations of 2D data, *on the native tco399 grid*.
* 2D_6h_0.25deg: 6-hourly snapshots and accumulations of 2D data
* 2D_24h_0.25deg: daily snapshots and accumulations of 2D data
* 2D_const_0.25deg: constant 2D fields (e.g. land-sea mask)
* 2D_monthly_0.25deg: monthly means 2D data, also some min/max fields
* 3D_24h_0.25deg: daily snapshots or means/min/max of 3D data
* 3D_6h_0.25deg: 6-hourly snapshots of 3D data
* 3D_monthly_0.25deg: monthly means,min,max of 3D data

Note the "0.25deg" or "native" suffix is often dropped as the resolution is evident from the sub-catalogue.

## Units
The 6-hourly output is generally given as instantaneous state variables (e.g. temperature) or accumulated fluxes (e.g. precipitation). Accumulations are given in accumulated units (e.g. for precipitation, in metres), which can be understood as per time-interval, which for our data are always 6 hours. 
Instantaneous variables are contained in catalogues like "2D_6h", while accumulations are in "2D_6h_acc". 

Daily means and monthly means are computed from hourly model output. State variables retain their units (e.g. Kelvin for temperature) while accumulated variables are converted in *mean rates* (e.g. m/s for precipitation). The temporal means for accumulated variables are exact up to numerical precision. In addition there are a few "maximum" and "minimum" output variables (maximum wind gust, maximum and minimum surface air temperature) which represent the statistics over the time-interval and are computed model-internally at model timestep resolution.

The time-axis of the catalogues is constructed to reflect the valid time-period of the data:
* Instantaneous variables are at their valid time, e.g. temperature at 12:00 represents the instantenous value at that time.
* Accumulated and mean/min/max variables are shifted to the center of their valid *period*, e.g. accumulated precipitation from 00:00 - 06:00 is coded at 03:00.
* Daily means are coded at 12:00
* Monthly means are coded at 12:00 on the 15th of each month.


## Notebooks
* STARTHERE_IFS_production.ipynb - A few starting points on how to access the data, compute simple metrics and plot.
* STARTHERE_IFS.ipynb - A (deprecated) starting notebook used for previous hackathon and preliminary simulations.

## Data collections

IFS data are stored in [intake catalogues](https://intake.readthedocs.io/en/latest/catalog.html): [EERIE intake catalogues[(https://github.com/eerie-project/intake_catalogues/tree/main). We attempt to show the available variables through the .csv files in the metadata directory.

## Data on Jasmin
Most of the dataset has been mirrored to Jasmin. Currently it is not within an intake-catalogue structure. However it can be loaded using the underlying .json files "like zarr files".
\<stream\> gives the stream name (see above), \<dim\> is either "2d" or "3d" depending on whether it is 2D or 3D data.
Locations:
* amip-hist-obs: /gws/nopw/j04/eerie/model_derived_data/EERIE/IFS-AMIP/prepIFS/OSTIA/gribscan/\<stream\>/json.dir/atm\<dim\>.json
* amip-hist-obs-lr30: /gws/nopw/j04/eerie/model_derived_data/EERIE/IFS-AMIP/prepIFS/OSTIA_LR30/gribscan/\<stream\>/json.dir/atm\<dim\>.json
* amip-ng-obs: /gws/nopw/j04/eerie/model_derived_data/EERIE/IFS-AMIP/RAPS/OSTIA/gribscan/\<stream\>/json.dir/atm\<dim>.json
* amip-ng-obs-lr30: /gws/nopw/j04/eerie/model_derived_data/EERIE/IFS-AMIP/RAPS/OSTIA_LR30/gribscan/\<stream\>/json.dir/atm\<dim>.json

In python, load this data via the following command:
ds = xr.open_zarr(
    'reference::path_to_json',
    consolidated=False
)
