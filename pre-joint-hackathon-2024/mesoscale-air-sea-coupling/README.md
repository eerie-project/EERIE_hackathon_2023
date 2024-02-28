# Spatial scale dependency of air-sea coupling

There's a strong spatio-temporal scale dependency of air-sea coupling, and a myraid of methods to separate those scales. Here, we take a few examples of air-sea coupling coefficients and produce global maps of them for full fields, smoothed fields and high-pass filtered fields. 

## [Spatial filters](Spatial_Filters/README.md)
We can use spatial filters to tease apart the spatial scale dependency of air-sea coupling coefficients. Here, we provide examples of using 3 different filtering techniques.

## Coupling coefficients with [ICON](ICON/README.md) and [IFS/FESOM](IFS-FESOM/README.md)
Coupling coefficients based on regression are used for measuring strength of air-sea coupling (Renault et al., 2016), particularly for thermal feedback (TFB) and current feedback (CFB). Additionally, other quantities can illustrate air-sea coupling and associated mesoscale features/implications. 

TFB: 
1. SST vs wind/stress magnitude
2. downwind SST gradient (winds) vs wind divergence
3. downwind SST gradient (stress) vs stress divergence
4. crosswind SST gradient (winds) vs wind curl
5. crosswind SST gradient (stress) vs stress curl

CFB:
1. surface current vorticity vs wind curl
2. surface current vorticity vs stress curl \
    => wind curl vs stress curl

Other quantities:
- wind work
- surface KE 
- surface geostrophic KE and vorticity
- eddy-induced Ekman pumping (Wek): curl, vortgrad, Stern, classical)

## Coupling coefficients for various models (intermodel comparison)

- [X] [ICON](ICON/README.md)
- [ ] [IFS/FESOM](IFS-FESOM/README.md) in progress
- [ ] HadGEM = UM/NEMO
- [ ] IFS/NEMO
- [ ] Verification with observations/reanalysis

