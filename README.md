# Repository of the first EERIE hackathon

This repo contain infromation necessary for data access, and examples of data processing for 1st EERIE hackathon

## Agenda
https://events.hifis.net/event/913/timetable/?view=standard

## Data

The EERIE simulations are in progress, so initially examples will be based on data from other projects, but there are already some EERIE based examples as well. We will gradually update examples with EERIE simulations when they become available.

We have compiled a list of variables that we aim to make available during the hackathon.
https://docs.google.com/spreadsheets/d/1HWtNO28EBd4O6PdOh5RCHIHsgQ_TByT5F4i2ugNVTfg/edit#gid=0

There are two sheets:

* EERIE: comprises first-priority variables interpolated to a 0.25-degree regular grid. We will try to deliver these for all simulations.

* WP7: lists second-priority variables. We will also strive to deliver these, but availability might differ among modeling groups.

Kindly plan your hackathon tasks with this in mind.

### Data structure

Data will be available through intake catalogs. It might be new experience for many, so please have a loot at:
* [General description about data structure and how to access data through catalogs on DKRZ](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/COMMON/eerie_data-access_dkrz-disk.ipynb) 
* Navigating through catalogs can be tricky at first, here is an example of [how to search inside some of the catalogs](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/COMMON/searching_catalogs.ipynb)

### Simulations
Current overview of simulations:

<img width="605" alt="Screenshot 2023-11-08 at 22 06 07" src="https://github.com/eerie-project/EERIE_hackathon_2023/assets/3407313/9798565c-9dee-4fa0-aef2-aee90afe9f18">



More detailed information about the availability of data on different grids and time frequencies can be found in the readme of each individual model's subfolder.

#### IFS/FESOM

##### Test data 
* nextGEMS Cycle 3 simulations. Description of simulations: https://easy.gems.dkrz.de/DYAMOND/NextGEMS/index.html#id4

##### EERIE simulations

* eerie-control-1950 - tco1279-NG5 (atmosphere 10 km, ocean 5-13 km). Currently 2 years available.
  * cat['dkrz']['disk']['model-output']['ifs-fesom2-sr']['eerie-control-1950']

#### ICON

##### Test data (not used in hackathon)
* nextGEMS Cycle 2 simulations Description of simulations: https://easy.gems.dkrz.de/DYAMOND/NextGEMS/index.html#id1

##### EERIE simulations
* eerie-control-1950 - 5 km ocean and 10km atmosphere
  * cat['dkrz']['disk']['model-output']['icon-esm-er']['eerie-control-1950']
  * Please note that for the first 7 years (model years 2002-2008), the 3d daily atmosphere (not 2d) are instantaneous values. This has been rectified to daily mean values from model year 2009 onwards. 

#### UM/NEMO

Initial data from the full eerie-piControl simulation is available:

| Model                          | Suite ID | Atmos Data  | Ocean Data  |
|--------------------------------|----------|-------------|-------------|
| HadGEM3-GC5-EERIE-N96-ORCA1    | cy163    | 1851 - 2081 |             |
| HadGEM3-GC5-EERIE-N216-ORCA025 | cy021    | 1851 - 1981 | 1851 - 1900 |
| HadGEM3-GC5-EERIE-N640-ORCA12  | cx993    | 1851 - 1901 | 1851 - 1890 |

CMORised atmosphere data is available on JASMIN in the `/gws/nopw/j04/eerie/public/data/EERIE/` directory.  The folder structure follows the CMIP conventions. The ocean data has not been CMORised but the raw ocean and seaice netCDF files have been included in the same directory structure (regridded and one variable per file).

#### IFS
Data from AMIP (atmosphere-only forced with sea surface temperature (SST) and sea ice concentration (SIC)) runs is available.
Given the purpose of the AMIP runs to study the impact of the presence of mesoscale features, the runs exist in pairs: One is forced with observed SST and SIC, taken from the OSTIA dataset (also available under #OBSERVATIONS), while in a twin experiment the observed SST *anomalies* are smoothed out with a filter the length scale of which is a multiple of the local Rossby radius of deformation. The multiple is indicated in the run ID, i.e. lr30 implies a factor of 30. For more details see #OBSERVATIONS.

| Run                | Data        |  SST
|--------------------|-------------|-----------|
| amip-hist-obs      | 2010 - 2020 | unfiltered OSTIA SST
| amip-hist-obs-lr30 | 2010 - 2020 | OSTIA SST smoothed with 30 x Rossby radius
| amip-ng-obs        | 2020 - 2021 | unfiltered OSTIA SST
| amip-ng-obs-lr30   | 2020 - 2021 | OSTIA SST smoothed with 30 x Rossby radius

The "hist" runs are historical runs with time-dependent forcing based on IFS CY48R1.1, including some new EERIE source updates.
The "ng" runs use the NextGEMS cycle 3 configuration, i.e. perpetual 2020 forcing (except for SST & SIC).

#### OBSERVATIONS

Here is [README with description of observations](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/OBSERVATIONS)

## What you need to get started

* DKRZ account for IFS/FESOM and ICON ([Science Hour presentation from Fabian Wachsmann](https://eerie-project.eu/science-hour/2023/07/27/introduction-to-levante-and-easy-gems/)
    * use python3/unstable as kernel
* JASMIN for UM/NEMO, IFS/NEMO and IFS ([Science Hour presentation from Malcolm Roberts](https://eerie-project.eu/science-hour/2023/06/29/introduction-to-jasmin-and-datasets/))
    * [How to use EERIE's facilities at JASMIN](https://github.com/eerie-project/jasmin_instructions#how-to-use-eeries-facilities-at-jasmin)
* [How to use the earlier version of this repo](https://eerie-project.eu/science-hour/2023/08/24/use-of-ifs-fesom-and-icon-km-scale-data/)
* [Use of the ESGF portal to screen and download data of the Pre-EERIE simulations](https://eerie-project.eu/science-hour/2023/09/08/the-use-of-the-esgf-portal-to-screen-and-download-data-of-the-pre-eerie-simulations/)

## How to start
The easier way to move forward is to login to the system you going to work with (DKRZ or JASMIN) and clone this repo:
```bash
git clone https://github.com/eerie-project/EERIE_hackathon_2023.git
```
Then go to jupyterhub of [DKRZ](https://jupyterhub.dkrz.de/) or [JASMIN](https://notebooks.jasmin.ac.uk) and execute notebooks from there.

To login to JASMIN to clone the repository, you can either use [SSH](https://help.jasmin.ac.uk/article/187-login) or you can use the [JASMIN jupyterhub](https://notebooks.jasmin.ac.uk) and go to Launcher (blue cross) and then choose a new Terminal.

### dkrz jupyterhub https://jupyterhub.dkrz.de/

* account: bk1377 (make sure you are a member of it)
* profile: at least 50GB memory
* 20gb home. more data can be temporarily saved in /scratch/b/BNUMBER . if your account starts with m use m/MNUMBER
* server runs for specific amount of time, you can close the browser, the server continues. Unless you stop it via the hub control panel.

### jasmin notebook service https://notebooks.jasmin.ac.uk

stops when there is no activity

### General knowlege

- For unstructured meshes: [`/COMMON/FESOM2_ICON_grids_easy_plot_and_interpolate.ipynb`](/COMMON/FESOM2_ICON_grids_easy_plot_and_interpolate.ipynb)
- For data interpolated to regular grid: [FESOM example](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/HOWTO_destroy_FESOM_data_by_regridding.ipynb)
- For interpolation from NEMO/FESOM/IFS/UM grid to regular grid: [WORK IN PROGRESS](COMMON/Soon_not_be_created_interpolate_to_regular.ipynb)
- For effective parallel aggregations with dask: [FESOM example](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/HOWTO_aggregate_data_native_grid_parallel.ipynb)


### Individual models

Each coupled model example is located in individual folders, which are in turn split into components. Begin with `START_HERE.ipynb` for each component, and then explore the notebooks from the list in the README.

## Examples
* Basics (access data on the original grid, get data for one time step, open grid, have a look at the data)
  * [NEMO (from UM_NEMO)](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/UM_NEMO/NEMO/START_HERE.ipynb)
  * [UM](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/UM_NEMO/UM/START_HERE.ipynb)
  * [ICON-O](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/STARTHERE_ICON-O.ipynb)
  * [FESOM2 nextGESM example](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/STARTHERE_FESOM.ipynb)
  * [IFS (from IFS-FESOM), nextGEMS example](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/IFS/STARTHERE_IFS.ipynb)
* Regridding to a regular grid
  * [FESOM2](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/HOWTO_destroy_FESOM_data_by_regridding.ipynb)
* Plotting global and regional maps
  * [FESOM2](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/HOWTO_interpolate_data_and_plot_maps_in_different_projections.ipynb)
  * [ICON-O](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/HOWTO_interpolate_data_and_plot_maps_in_different_projections.ipynb)
* Finding a point nearest to coordinates, extracting time series
* Finding a set of points closest to a transect, plotting the transect
* Effective, parallel aggregations
  * [FESOM2, but will work with any](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/HOWTO_aggregate_data_native_grid_parallel.ipynb)
* Area integral, Volume integral
* Plot transect
  * [FESOM2](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/FESOM/HOWTO_plot_transect.ipynb)
* Curl
* Transport through a transect
* Compute AMOC
  * [ICON-O](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/eerie_icon_amoc-cell.ipynb)
  * [UM-NEMO](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/UM_NEMO/AMOC)


## Standard variables

Here is the [list of variables, that will be available during hackathon](https://docs.google.com/spreadsheets/d/1HWtNO28EBd4O6PdOh5RCHIHsgQ_TByT5F4i2ugNVTfg/edit#gid=83304216).

## External resources

* [easy.gems](https://easy.gems.dkrz.de/) as a user-driven site for documenting high-resolution climate simulation output and its increasingly challenging analysis
* [Cycle 2 nextGEMS Hackathon repository](https://github.com/nextGEMS/nextGems_Cycle2)
* [Cycle 3 nextGEMS Hackthon repository](https://github.com/nextGEMS/nextGEMS_Cycle3)

## Contribution

We welcome contributions to the EERIE_hackathon_2023 project! Depending on the extent of your contributions, you can follow one of the two processes:

### Small Contributions

For small, one-time contributions, please follow the standard GitHub process:
1. Fork the repository.
2. Create a new branch in your fork.
3. Make your changes and commit them to your branch.
4. Create a Pull Request (PR) from your branch to the main repository.

### Large Contributions
If you plan to make many contributions, you may request write access to the repository. Even with write access, it's best practice to:
1. Create a new branch for your changes.
2. Commit your changes to that branch.
3. Create a Pull Request (PR) from your branch to the main branch.

This ensures that changes are reviewed and integrated systematically. Please avoid committing directly to the main branch.

Thank you for your interest in contributing to the EERIE_hackathon_2023 project!

## Model documentation and useful links

### IFS/FESOM
* [IFS website](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model)
* [FESOM2 GitHub repo](https://github.com/FESOM/fesom2)
* [FESOM2 documentation](https://fesom2.readthedocs.io/en/latest/)
* [pyfesom2](https://github.com/FESOM/pyfesom2), python library to work with FESOM2 data
* [fint](https://github.com/FESOM/fint) FESOM2 interpolation command line utilities

### ICON

* [ICON website](https://code.mpimet.mpg.de/projects/iconpublic)

### IFS/NEMO

* [IFS website](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model)

### UM/NEMO

* [UM website](https://www.metoffice.gov.uk/research/approach/modelling-systems/unified-model)

### IFS

* [IFS website](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model)

