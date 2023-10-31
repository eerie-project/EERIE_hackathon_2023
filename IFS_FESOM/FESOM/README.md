# FESOM data from IFS-FESOM simulations

Currently for examples we use [nextGEMS Cycle 3](https://easy.gems.dkrz.de/DYAMOND/NextGEMS/index.html#id4) simulations. Later they will be updated with EERIE simulations.

## Notebooks

* START_HERE.ipynb - simple, basic example, without a lot of explanations. Access to data, plot
* HOWTO_aggregate_data_native_grid_parallel - example of how to aggregate high resolution/high frequency data with dask. Works for FESOM and should work for other models as well.
* HOWTO_destroy_FESOM_data_by_regridding - examples of regriding with cdo and smmregrid (that uses cdo weights, but regrid in parallel using dask).
* HOWTO_interpolate_data_and_plot_maps_in_different_projections - Here we will show how to plot FESOM2 data (and any unstructured and structured data for that matter) on a map with different projections. It's a simple way not to wait for ages while your cartopy script will plot one time step. As a bonus we show at the end how to create netCDF file from your interpolated data, that you can animate with ncview.


## Data collections

FESOM data stored in [intake catalog](https://intake.readthedocs.io/en/latest/catalog.html). We still figuring out how to best represent infromation about stored there. 

