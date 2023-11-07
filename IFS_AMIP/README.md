# IFS data from IFS-AMIP simulations done at ECMWF

For this hackathon we make available four IFS-AMIP simulations run at ECMWF, at a tco399 resolution (approximately 28km). For ease of the analysis, the data provided for the hackathon has been regridded to a 0.25 degree regular grid.

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

## Notebooks

* STARTHERE_IFS.ipynb - A few starting points on how to access the data, compute simple metrics and plot.

## Data collections

IFS data are stored in [intake catalogues](https://intake.readthedocs.io/en/latest/catalog.html). We still figuring out how to best represent infromation about stored there. 

