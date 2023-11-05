# IFS data from IFS-FESOM simulations

Currently for examples we use both EERIE and [nextGEMS Cycle 3](https://easy.gems.dkrz.de/DYAMOND/NextGEMS/index.html#id4) simulations. Examples for nextGEMS start with `nextGEMS` prefix. So far nextGEMS ones have much more data and with much higher frequency, but we are working on improving the situation for EERIE runs as well.

## Data collections

FESOM EERIE data stored in [intake catalog](https://intake.readthedocs.io/en/latest/catalog.html). Here are the links to basic examples for and [interpolated](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/IFS_FESOM/IFS/STARTHERE_IFS_interpolated_data.ipynb) data.

In short this should work to open the data:
```python
import intake
data_025 = cat['dkrz.disk.model-output.ifs-fesom2-sr.eerie-control-1950.atmos.gr025']['daily'].to_dask() # for daily interpolated data
```

## Notebooks

* START_HERE.ipynb - simple, basic example, without a lot of explanations. Access to data, plot.




