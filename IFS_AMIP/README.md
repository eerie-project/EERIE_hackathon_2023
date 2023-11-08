# IFS data from IFS-AMIP simulations done at ECMWF

For this hackathon we make available four IFS-AMIP simulations run at ECMWF, at a tco399 resolution (approximately 28km). For ease of the analysis, the data provided for the hackathon has been regridded to a 0.25 degree regular grid. The data is primarily accessible through the intake catalogue structure on DKRZ (data is also on Jasmin, more below).

To explore which variables are available for which experiments and streams, the *metadata* directory contains searchable \<exp\>__\<stream\> .csv files listing the metadata for each variable. Additional information on ECMWF variables is available in the [ECMWF Parameter Database](https://codes.ecmwf.int/grib/param-db/) which can be searched by short name, GRIB code, units etc. Particular care is advised for flux data (precipitation, surface heat fluxes etc.) which may be provided either as *rates* (e.g. mm/day, W/m^2, typical for monthly means) or as *accumulations* (e.g. m, J/m^2, typical for high-frequency output).

AMIP runs are atmosphere-only runs, withtout an ocean model, forced with sea surface temperature (SST) and sea ice concentration (SIC).
Given the purpose of the AMIP runs to study the impact of the presence of mesoscale features, the runs exist in pairs: One is forced with observed SST and SIC, taken from the OSTIA dataset (also available under #OBSERVATIONS), while in a twin experiment the observed SST *anomalies* are smoothed out with a filter the length scale of which is a multiple of the local Rossby radius of deformation. The multiple is indicated in the run ID, i.e. lr30 implies a factor of 30. For more details see #OBSERVATIONS.

| Run                | Data        |  SST
|--------------------|-------------|-----------|
| amip-hist-obs      | 2010 - 2020 | unfiltered OSTIA SST
| amip-hist-obs-lr30 | 2010 - 2020 | OSTIA SST smoothed with 30 x Rossby radius
| amip-ng-obs        | 2020 - 2021 | unfiltered OSTIA SST
| amip-ng-obs-lr30   | 2020 - 2021 | OSTIA SST smoothed with 30 x Rossby radius

The "hist" runs are historical runs with time-dependent forcing based on IFS CY48R1.1, including some new EERIE source updates.
The "ng" runs use the NextGEMS cycle 3 configuration, i.e. perpetual 2020 forcing (except for SST & SIC).

## Data structure:
The data is organized in streams by frequency, 2D/3D and grid (here only 0.25 degree) 
amip-hist-obs and amip-hist-obs-lr30:
* 2D_24h_0.25deg: daily snapshots of 2D data
* 2D_6h_0.25deg: 6-hourly snapshots of 2D data
* 2D_const_0.25deg: constant 2D fields (e.g. land-sea mask)
* 2D_monthly_0.25deg: monthly means 2D data
* 3D_24h_0.25deg: daily snapshots of 3D data
* 3D_6h_0.25deg: 6-hourly snapshots of 3D data
* 3D_monthly_0.25deg: monthly means of 3D data
amip-ng-obs and amip-ng-obs-lr30:
* all (available) output is in the dcda stream. It contains 2D data (6-hourly) and 3D data (24-hourly). One variable (density of lightning strikes in the past 6 hours) has been split off and is not in the stream "lightning".

## Notebooks

* STARTHERE_IFS.ipynb - A few starting points on how to access the data, compute simple metrics and plot.

## Data collections

IFS data are stored in [intake catalogues](https://intake.readthedocs.io/en/latest/catalog.html): [EERIE intake catalogues[(https://github.com/eerie-project/intake_catalogues/tree/main). We attempt to show the available variables through the .csv files in the metadata directory.

## Data on Jasmin
The whole dataset has been mirrored to Jasmin. Currently it is not within an intake-catalogue structure. However it can be loaded using the underlying .json files "like zarr files".
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
