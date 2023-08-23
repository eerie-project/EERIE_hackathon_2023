# Repository of the first EERIE hackathon

This repo contain infromation necessary for data access, and examples of data processing for 1st EERIE hackathon

## Data

The EERIE simulations are not ready yet, so initially examples will be based on data from other projects. We will gradually update examples with EERIE simulations when they become available.

### IFS/FESOM

**Test data** 

nextGEMS Cycle 3 simulations

Description of simulations: https://easy.gems.dkrz.de/DYAMOND/NextGEMS/index.html#id4

### ICON

**Test data**

nextGEMS Cycle 2 simulations

Description of simulations: https://easy.gems.dkrz.de/DYAMOND/NextGEMS/index.html#id1

### IFS/NEMO

### UM/NEMO

### IFS


## What you need to get started
* DKRZ account for IFS/FESOM and ICON
    * use python3/unstable as kernel
* JASMIN for UM/NEMO, UM/NEMO and IFS

## How to start

### General knowlege

- For unstructured meshes: [`/COMMON/FESOM2_ICON_grids_easy_plot_and_interpolate.ipynb`](/COMMON/FESOM2_ICON_grids_easy_plot_and_interpolate.ipynb)
- For data interpolated to regular grid: [`COMMON/Soon_not_be_created_interpolated_ocean_data_start.ipynb`](COMMON/Soon_not_be_created_interpolated_ocean_data_start.ipynb)
- For interpolation from NEMO/FESOM/IFS/UM grid to regular grid: [`COMMON/Soon_not_be_created_interpolate_to_regular.ipynb`](COMMON/Soon_not_be_created_interpolate_to_regular.ipynb)
- For effective parallel aggregations with dask: [`COMMON/Soon_not_be_created_parallel_aggregations_with_dask.ipynb`](COMMON/Soon_not_be_created_parallel_aggregations_with_dask.ipynb)


### Individual models

Each coupled model example is located in individual folders, which are in turn split into components. Begin with `START_HERE.ipynb` for each component, and then explore the notebooks from the list in the README.

## Examples (for now, mostly planned :) )
* Basics (access data on the original grid, get data for one time step, open grid, have a look at the data)
* Regridding to a regular grid
* Plotting global and regional maps
* Finding a point nearest to coordinates, extracting time series
* Finding a set of points closest to a transect, plotting the transect
* Effective, parallel aggregations
* Area integral, Volume integral
* Curl
* Transport through a transect
* Compute AMOC


## Standard variables (tentative list, will be coordinated between modelling groups)

* SST, daily
* SSH, daily
* ...
* 

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

