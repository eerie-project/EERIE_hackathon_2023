# Example code to plot AMOC from UM model

## Data

The EERIE simulations from the Met Office are CMIP6-like, with piControl outputs so far.
The AMOC METRIC code is used to calculate AMOC at different sections: RAPID, MOVE and SAMBA: Danabasoglu et al, 2021: https://doi.org/10.1029/2021GL093045


### UM/NEMO

Initial data from the full eerie-piControl simulation is available:

| Model                          | Data        | Suite name |
|--------------------------------|-------------|-------------
| HadGEM3-GC5-EERIE-N96-ORCA1    | 1851 - 2050 | u-cy163
| HadGEM3-GC5-EERIE-N216-ORCA025 | 1851 - 1960 | u-cy021
| HadGEM3-GC5-EERIE-N640-ORCA12  | 1851 - 1900 | u-cx993


