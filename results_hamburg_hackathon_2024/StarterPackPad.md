# Hackathon Starter Pack

# TABLE OF CONTENTS
- [Hackathon Starter Pack](#hackathon-starter-pack)
  * [Links to relevant documents](#links-to-relevant-documents)
  * [Using the Levante Supercomputer](#using-the-levante-supercomputer)
    + [DKRZ User account for data access](#dkrz-user-account-for-data-access)
    + [Jupyterhub](#jupyterhub)
    + [Python environments](#python-environments)
    + [CDO Versions](#cdo-versions)
    + [General documentation](#general-documentation)
- [Simulation Overview](#simulation-overview)
  * [NextGEMS](#nextgems)
    + [ICON](#icon)
      - [prefinal](#prefinal)
      - [pre-prefinal experiments **[volatile data](#Terms-and-conditions)**](#pre-prefinal-experiments-volatile-data---terms-and-conditions---)
      - [Terms and conditions](#terms-and-conditions)
    + [Basic notes on HEALpix:](#basic-notes-on-healpix-)
  * [EERIE](#eerie)
- [Working with the data](#working-with-the-data)
  * [Reading in the data](#reading-in-the-data)
    + [NextGEMS (data access via intake)](#nextgems--data-access-via-intake-)
    + [EERIE (data access via intake)](#eerie--data-access-via-intake-)
    + [EERIE (data access on shell environment for cdo operations)](#eerie--data-access-on-shell-environment-for-cdo-operations-)
  * [Example notebooks on some scientific analysis](#example-notebooks-on-some-scientific-analysis)
  * [Building python environment](#building-python-environment)
    + [Easiest option (pre-made python env for hackathon)](#easiest-option--pre-made-python-env-for-hackathon-)
- [Hackathon breakout groups](#hackathon-breakout-groups)
  * [Storms&Ocean](#storms-ocean)
  * [Storms&Radiation](#storms-radiation)
  * [Storms&Land](#storms-land)

-------------

## Links to relevant documents
* Event page with agenda https://mpim-po.pages.gwdg.de/km-scale-hackathon/
* Technical documentation:  https://easy.gems.dkrz.de 
* Mattermost channels:
    * [Hackathon channel](https://mattermost.mpimet.mpg.de/nextgems/channels/hamburg-km-scale-hackathon-march-2024) (to sign up for the nextGEMS team, join [here](https://mattermost.mpimet.mpg.de/signup_user_complete/?id=oiy5ibsux7yf8pqgcdu3dk7n6c&md=link&sbr=su))
    * [Simulation Support](https://mattermost.mpimet.mpg.de/nextgems/channels/dyamond-winter-tutorial)
    * Workgroups:
* Video Tutorials (from EERIE project): 
    * [Use of IFS-FESOM and ICON km-scale data](https://eerie-project.eu/science-hour/2023/08/24/use-of-ifs-fesom-and-icon-km-scale-data/) (Nikolay Koldunov)
    * [Introduction to Levante and easy.gems](https://eerie-project.eu/science-hour/2023/07/27/introduction-to-levante-and-easy-gems/) (Fabian Wachsmann)
* GitHub repositories for sharing scripts:
    * [nextgems_prefinal](https://github.com/nextGEMS/nextGEMS_Cycle4)
    * [EERIE_hackathon_2023](https://github.com/eerie-project/EERIE_hackathon_2023) for continuity of [workflow in some EERIE WPs](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/README.md)
* Wifi connectivity:
    * Eduroam (no further action required)
    * Otherwise you need a unique code to connect to the Guest Wifi (for access code please fill your name and email address in this [table](https://owncloud.gwdg.de/index.php/s/Vx74aCN3PymzbUq))


## Using the Levante Supercomputer

### DKRZ User account for data access 

To access the data available at this hackathon you need to have a user account at the German Climate Computing Centre (DKRZ). You can set up an account by following the documentation from the DKRZ [here](https://docs.dkrz.de/doc/getting_started/getting-a-user-account/dkrz-user-account.html) and quoting the project ID bm1153 (DYAMOND). Setting up a DKRZ user account is also covered in this [tutorial](https://eerie-project.eu/science-hour/2023/07/27/introduction-to-levante-and-easy-gems/). **If you already have your own project (e.g. because you work at MPI-M), please use that one instead.**



### Jupyterhub

Once you have a DKRZ user account, you can log into [jupyterhub](https://jupyterhub.dkrz.de) with your username (b123456 -style ID you obtained from luv) and password. From here you can open a jupter notebook and select the python3/unstable kernel. Now you're ready to get hacking!

### Python environments

See

https://pad.gwdg.de/aVT-yC_6T9qopIDekEipqA#
and
https://pad.gwdg.de/bJMq4TloSCiPFeWjvsprGg#

for some hints

### CDO Versions

Try
```
module load cdo/2.3.0-gcc-11.2.0
```
for a more up-to-date cdo, 
or 
```
module load cdo/.2.4.0-gcc-11.2.0
```
for a **rather untested** but even newer version.

### General documentation

For more documentation on Levante you can go to https://docs.dkrz.de 


# Simulation Overview

At this hackathon we have access to simulations from both the [nextGEMS](https://nextgems-h2020.eu) and the [EERIE](https://eerie-project.eu) projects. For more information on the simulations available for both projects please refer to the tables below. 

## NextGEMS

::: info
Also see the [![easy.gems](https://pad.gwdg.de/uploads/92f5cad0-ec2f-4df9-b289-0e6e5d021068.png =50x)](https://easy.gems.dkrz.de) site for documentation about these runs and the other nextGEMS cycles
:::

```python
import intake
cat = intake.open_catalog("https://data.nextgems-h2020.eu/catalog.yaml")
```
| Model    | Resolution atm/oce [km] | Simulation (forcing) | output | status | data | 
| -------- | --------   | -------- | --------| ---------|-----|
| [ICON (prefinal)](#ICON-prefinal) | 10/5 | 2020-2050 <br> (transient) </br> |healpix, multiple zoom|11/30 years done, ongoing |  ``cat.ICON.ngc4008``|
| IFS-FESOM (production)| 9/5 | 2020-2050 <br> (transient SSP3-7.0) </br> |healpix 2 zoom levels, regular 0.25| 30 years, completed | Monthly means on regular grid in catalog: ``cat.IFS['IFS_9-FESOM_5-production']['2D_monthly_0.25deg']`` <br> ``cat.IFS['IFS_9-FESOM_5-production']['3D_monthly_0.25deg']`` </br> Daily ocean means on healpix in catalog: ``cat.IFS['IFS_9-FESOM_5-production']['2D_daily_healpix512_ocean']`` <br> ``cat.IFS['IFS_9-FESOM_5-production']['3D_daily_healpix512_ocean']`` </br> Hourly atm means on healpix in catalog: ``cat.IFS['IFS_9-FESOM_5-production']['2D_hourly_healpix512']`` <br> ``cat.IFS['IFS_9-FESOM_5-production']['3D_hourly_healpix512']`` </br> Monthly means on healpix in catalog: ``cat.IFS['IFS_9-FESOM_5-production']['2D_monthly_healpix512']`` <br> ``cat.IFS['IFS_9-FESOM_5-production']['3D_monthly_healpix512']``
| ICON + HAMOCC (cycle 3)| 5/5 | 2020 (one year) </br>|native| completed |``cat.ICON.ngc3542`` |
| ICON-O + HAMOCC | 10 (ocean stand alone) | 1996-2012 forced by ERA |netcdf| completed | /work/mh0287/m300805/code/ICON/R2B8L72 (subset of variables)

### ICON

::: success
For a quick look at results and output available, see
* [Global mean time-series](https://swift.dkrz.de/v1/dkrz_b381d76e-63d7-4aeb-96f0-dfd91e102d40/nextgems_prefinal/index.html)
* [Atmospheric quickplots](https://swiftbrowser.dkrz.de/public/dkrz_cc566461dff84e59964ced89d96324d8/ngc4/)
* Oceanic quickplots ([ngc4008](https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/helmuth/all_qps/NextGems/qp-ngc4008/qp_index.html), [ngc4007](https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/helmuth/all_qps/NextGems/qp-ngc4007/qp_index.html), [ngc4006](https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/helmuth/all_qps/NextGems/qp-ngc4006/qp_index.html), [ngc4005](https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/helmuth/all_qps/NextGems/qp-ngc4005/qp_index.html))
* [Output variables by experiment](https://owncloud.gwdg.de/index.php/s/G6xEfuoHOZLB3Kt) (table)
* [Interactive mapping of variable/output frequency/horizontal resolution for ngc4008](https://swift.dkrz.de/v1/dkrz_b381d76e-63d7-4aeb-96f0-dfd91e102d40/nextgems_prefinal/nextgems_prefinal_output.html)
  * [Same plus additional 3h mean data for 2027-04 - 2027-09](https://swift.dkrz.de/v1/dkrz_b381d76e-63d7-4aeb-96f0-dfd91e102d40/nextgems_prefinal/nextgems_prefinal_output_anim.html) **[:zap:volatile data](#Terms-and-conditions)**
:::

 
#### prefinal 

* ngc4008 ^[[ngc4008 development info:lock:](https://gitlab.dkrz.de/icon/icon-mpim/-/issues/79)]: the default experiment for the hackathon. ssp370-like scenario run from 2020 to 2050. This run is based on updates/bugfix/tuning efforts done with the experiments ngc4005, ngc4006, and ngc4007 (see below)
* It is similar to ngc4007, but with reduced inhomogenity factor. 

#### pre-prefinal experiments **[:zap:volatile data](#Terms-and-conditions)**

:::info
Only available for HEALPix zoom level 0 - 8, plus level 9 for _precipitation flux_
:::

* ngc4005 ^[[ngc4005 development info:lock:](https://gitlab.dkrz.de/icon/icon-mpim/-/issues/17)]: ssp370 like scenario run from 2020 :warning: intermittent changes in output configuration.
Intake reference: `cat.ICON.ngc4005`
  * 2024-04-01: adjust sea-ice parameters to yield more summer sea ice
 
* ngc4006 ^[[ngc4006 development info:lock:](https://gitlab.dkrz.de/icon/icon-mpim/-/issues/57)]: continue ngc4005 for 2025 - 2040, finalized output configuration.
Intake reference: `cat.ICON.ngc4006`
    * discontinued in favor of ngc4007 (later ngc4008) as model results were increasingly impaired by  insufficient stratocumulus cloud formation

* ngc4007 ^[[ngc4007 development info:lock:](https://gitlab.dkrz.de/icon/icon-mpim/-/issues/78)]: includes bug fix for land energy balance; modification of inhomogeneity factor to account for boundary layer clouds. Starts with the 2020 initial conditions like ngc4005, modulo a more adjusted hydrological discharge model.
Intake reference: `cat.ICON.ngc4007`
    * Not restarted after about 1.3 years due stratocumulus albedo/temperature bias, in favor of ngc4008.

::: warning
#### Terms and conditions
The datasets marked as **:zap:volatile data** are provided as-is with the understanding that these results are preliminary, are primarily meant for insights into the nature of model tuning and changes, and will neither be supported nor provided for use beyond the hackathon.

If nevertheless you consider them relevant for your research, you are responsible to take the measures necessary to ensure good scientific practice, possibly including long-term storage. This does not waive any intellectual property rights of the data producers 
:::

### Basic notes on HEALpix:
| zoom index (ICON) | nside index (IFS/FESOM) |  resolution in degrees | resolution in km |
| --------------- | --------------- | --------------- | --------------- |
| zoom 0 | nside 1 | 59 deg | 6144 km | 
| zoom 1 | nside 2 | 29 deg | 3072 km |
| zoom 2 | nside 4 | 15 deg | 1536 km |
| zoom 3 | nside 8 | 7.3 deg | 768 km |
| zoom 4 | nside 16 | 3.7 deg | 384 km |
| zoom 5 | nside 32 | 1.8 deg | 192 km |
| zoom 6 | nside 64 | 0.92 deg | 96 km |
| zoom 7 | nside 128 | 0.46 deg | 48 km |
| zoom 8 | nside 256 | 0.23 deg | 24 km |
| zoom 9 | nside 512 | 0.11 deg | 12 km |
| zoom 10 | nside 1024 | 0.057 deg | 6 km |

## EERIE 

Details about EERIE models can be found [here](https://eerie-project.eu/research/modelling/our-models/)

An interactive overview on EERIE data can be found [here](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html).
{please fill information about where to find data and link to variable list}

<iframe src="https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html" width=100% height="800"></iframe>

| Model   | Resolution | Simulation (Forcing) | output | status | data <br> `eerie_cat['dkrz.disk.model-output'][model][expid][realm][gridspec]`| link(s) for more info [(interactive EERIE data overview)](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html) |
| -------- | --------   | -------- | --------| ---------|-----| ----|
| ICON  (cycle 1)   | 10km atm/ 5km ocn|  1950-2001 <br> (1950-spinup) 2002-2040 (1950-ctrl)  </br> |native ref. 0.25 deg| completed |model=['icon-esm-er'] <br> expid=['eerie-spinup-1950' , 'eerie-control-1950'] <br> realm=['atmos' , 'ocean']<br> gridspec=['gr025' , 'native']| Simulation details and data cautionary notes found [here](https://pad.gwdg.de/aavr_v90T9KjrhDZgWYy8w?view). <br> **Please limit usage to time period 2002-2039** <table>  <thead>  <tr>  <th> output freq (*issue*/plus) </th>  <th>time period</th>   </tr>  </thead>  <tbody>  <tr>  <td>daily mean 3d atm *(instantaneous, not mean)*</td>  <td>2002-2008</td>   </tr>  <tr>  <td> daily 2d min and max of tas and sfcwind *(wrong output_interval of month instead of daily)* </td>  <td>2002-2008</td>    </tr>  <tr>  <td>daily mean 3d ocean **(only available for 10 years)** </td>  <td>2002-2011</td>   </tr>  </tr>  </tbody>  </table> 
| IFS/FESOM (production)| 9km atm/ 5km ocn | 1950-1980 <br> (1950-ctrl) </br> |native ref. 0.25 deg| complete |model=['ifs-fesom-sr'] <br> expid=['eerie-control-1950'] <br> realm=['atmos' , 'ocean']<br> gridspec=['gr025' , 'native']| Details of the simulation and available variables at https://docs.google.com/document/d/123VqtO69HHoIKAnsKln1kLcDpsMghw-9jDHQNc8juFg/edit?usp=sharing
| HadGEM (production) | atm N640 (20km)/ oce 1/12 deg; <br> atm N216 (60km)/ oce 0.25deg | piCtrl (1850) <br> 130 years; <br> 50 years </br>| native 0.25 deg | ongoing | model=['hadgem3-gc5-n640-orca12' , 'hadgem3-gc5-n216-orca025'] <br> expid=['eerie-picontrol'] <br> realm=['atmos' , 'ocean']<br> gridspec=['gr025']| Full outputs available on JASMIN. Sporadic missing outputs on Levante [This is like observational data. Oh no, what to do? :grimacing:]. Use at own risk!
|IFS-NEMO | 9km atm/ 1/12 deg ocn | 20 years <br> (1950-ctrl) </br>|native | cycle 1 |  model=['ifs-nemo'] <br> expid=['eerie-control-1950'] <br> realm=['atmos' , 'ocean']<br> gridspec=['native']
| IFS AMIP | 28 km atm (TCO399) | 2010-2020 various experiments with filters | 0.25 deg | done | eerie_cat['dkrz.disk.model-output']['ifs-amip'][expid] <br> <table>  <thead>  <tr>  <th> expid </th>  <th>description</th>   </tr>  </thead>  <tbody>  <tr>  <td>amip-hist-obs.atmos.gr025</td>  <td>historical SST (ESA CCI v3)</td>   </tr>  <tr>  <td>amip-hist-obs-lr30.atmos.gr025</td>  <td>filtered SST anomalies</td>    </tr>  <tr>  <td>amip-hist-obs-c-lr30-a-0.atmos.gr025</td>  <td>filtered climatology</td>   </tr> <tr>  <td>amip-hist-obs-c-lr30-a-lr30.atmos.gr025</td>  <td>filtered climatology and anomalies</td>    </tr>  </tbody>  </table>  |Details of simulations  found [here](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/IFS_AMIP)
|IFS AMIP | 9 km atm (TCO1279)  | 2010-2020 filter experiments | 0.25 dg | ongoing
|Observations and reanalysis products (available on Levante via EERIE catalog) |variable  | MSWEP, ERA5, CERES, AVISO, PHC3, WOA18, OSI-SAF, EN4, GPM, OSTIA, ESA-CCI-SST, QUIKSCAT | varying | |eerie_cat['dkrz.disk.observations'][expid] <br> where expid=['MSWEP', 'ERA5', 'CERES', 'AVISO', 'PHC3', 'WOA18', 'OSI-SAF', 'EN4', 'GPM', 'OSTIA', 'ESA-CCI-SST', 'QUIKSCAT']| Notebook examples of how to access datasets and details of datasets found [here](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/OBSERVATIONS/README.md)|


# Working with the data

## Reading in the data

To read in the data, we use intake catalogs. The following examples show you how to open data in python with the intake catalog. 

### NextGEMS (data access via intake)

For the nextGEMS data we use ```intake.open_catalog``` for all simulations. Refer to the [easygems](https://easy.gems.dkrz.de) documentation for more detailed examples. 

Read in ICON ngc4008 (or ngc4007, ngc4006, ngc4005) simulation data as xarray dataset. For these simulations the data is available on the HEALPix grid, which allows us to specify a zoom level between 0 and maximum 10. More information about HEALPix can be found [here](https://easy.gems.dkrz.de/Processing/healpix/healpix_starter.html).  
```python=
import intake
import healpy

cat = intake.open_catalog("https://data.nextgems-h2020.eu/catalog.yaml")
exp_id = "ngc4005" # or 'ngc4006', 'ngc4007', 'ngc4008'
dataset = cat.ICON[exp_id](zoom=2).to_dask()
display(dataset)
```
:::warning
When using evaluation routines from previous hackathons, please note that the ICON variable names are no longer lowercase only!
:::
Read in data for ICON+HAMOCC simulation. Note that this data is not available on the HEALPix grid and we cannot specify the zoom level. 

```python=
import intake 

cat=intake.open_catalog("/work/bm1344/DKRZ/intake/dkrz_ngc_esm.yaml")
print(list(cat)) # returns list of datasets in catalog
# open one of the datasets in the catalog
dataset = cat['ICON-ESM-SR_coupled-climate-carbon-cycle_atm_2d_1h_inst'].to_dask()
display(dataset)
```

Read in IFS-FESOM production simulation data as xarray dataset
```python=
import intake
cat = intake.open_catalog("https://data.nextgems-h2020.eu/catalog.yaml")

exp_id = "IFS_9-FESOM_5-production"
stream = "2D_monthly_0.25deg" # e.g. '2D_monthly_0.25deg', '3D_monthly_0.25deg'
dataset = cat.IFS[exp_id][stream].to_dask()
```
[longer example on nextGEMS_prefinal github](https://github.com/nextGEMS/nextGEMS_prefinal/blob/main/IFS/STARTHERE_IFS-production.ipynb)


### EERIE (data access via intake)

EERIE data referenced with catalogs can be opened from DKRZ´s module/kernel named:
*python3/unstable*.

**With pure intake:**

```python=
import intake
eerie_cat=intake.open_catalog("https://raw.githubusercontent.com/eerie-project/intake_catalogues/main/eerie.yaml")
eerie_cat
```
[Tree structure of eerie catalogue](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/COMMON/eerie_data-access_dkrz-disk.ipynb):
model, expid, realm=['atmos' , 'ocean'], gridspec=['native' , 'gr025']

```python=
model_list=list(eerie_cat['dkrz.disk.model-output'])
print(model_list)
```
```co
['icon-esm-er', 'ifs-fesom2-sr', 'ifs-amip', 'ifs-nemo', 'hadgem3-gc5-n640-orca12', 'hadgem3-gc5-n216-orca025', 'csv', 'esm-json'] 
```
```python=
model = 'icon-esm-er'
expid=list(eerie_cat['dkrz.disk.model-output'][model])
print(expid)
```
```co
['eerie-control-1950', 'eerie-spinup-1950']
```

Example to access data:
```python=
model = 'ifs-fesom2-sr'
expid = 'eerie-control-1950'
gridspec = 'gr025'
realm='atmos'
cat_data=eerie_cat['dkrz.disk.model-output'][model][expid][realm][gridspec]
print(list(cat_data))
ds = cat_data['daily'].to_dask()
```

More detailed examples provided on [EERIE_hackaton_2023 repo](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/COMMON), and [EERIE data on easygems](https://easy.gitlab-pages.dkrz.de/-/gems/-/jobs/287574/artifacts/public/simulations/EERIE/eerie_data-access_dkrz.html).

**With intake-esm ([details here](https://easy.gitlab-pages.dkrz.de/-/gems/-/jobs/287574/artifacts/public/simulations/EERIE/eerie_data-access_dkrz.html)):**

```python=
import json
df=eerie_dkrz_disk["model-output"]["csv"].read()
esmjson=json.loads(''.join(cat["esm-json"].read()))
dkrz_disk_model_esm=intake.open_esm_datastore(
    obj=dict(
        esmcat=esmjson,
        df=df
    ),
    columns_with_iterables=["variables","variable-long_names","urlpath"],
)

dkrz_disk_model_esm.to_dataset_dict(
    xarray_open_kwargs=dict(
        backend_kwargs =dict(
            consolidated=False
        )
    ),
    storage_options=dict(
        remote_protocol="file",
        lazy=True
    )
```
### EERIE (data access on shell environment for cdo operations)
Data is catalogued using intake, we obtain path of data for use with cdo using *query_yaml.py*. A magic script created by Florian Ziemen for those who'd still like to use cdo shell environment for parts of their analysis.

**Load modules**
```bash
module use /work/k20200/k202134/hsm-tools/outtake/module
module load hsm-tools/unstable
```
**Get directory tree structure of EERIE data** (similar to [data access via intake](#EERIE-data-access-via-intake))

```bash
eerie_cat=https://raw.githubusercontent.com/eerie-project/intake_catalogues/main/eerie.yaml
query_yaml.py -c ${eerie_cat} dkrz disk model-output
```
Default catalog is NextGEMS. Hence, directory tree for NextGEMS simulations can be seen by just executing `query_yaml.py`

**Set [variable name](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html), access data and apply cdo operation**
```bash
varname='sst'
varfilelist=$(query_yaml.py -c ${eerie_cat} dkrz disk model-output ifs-fesom2-sr eerie-control-1950 ocean gr025 daily --var ${varname} --uri --cdo)
echo ${varfilelist}

cdo -P 64 -smooth,radius=3deg -select,name=${varname} ${varfilelist} ${varname}_sm3deg.nc
```

Example for performing a similar data accessing and cdo operation on NextGEMS data can be found [here](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md#bonus-spatial-filtering-on-healpix-data)

## Example notebooks on some scientific analysis
Here's a [collection of examples](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/README.md) particularly for topics on mesoscale eddies and their impact on air-sea coupling, ocean state (physical and BGC) and atmospheric state.

 - [Eddy identification, tracking and compositing](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/README.md) of physical (ocean/atmos) and biogeochemical properties
    - ICON (read-in netcdf; serial running): [identify and track eddies](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-IDtrackcompeddy-daily.ipynb), [build eddy composites](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-eddycompositeotherfields-daily.ipynb), [plot composites](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/ICON/ICON-O/howto-plot-eddycompositesalongtrack-dm.ipynb) by Dian Putrasahan
    - ICON (read-in netcdf; parallel running): [py-eddy-tracker parameter sensitivity experiment](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_parallel_computing) by Arjun Kumar
    - ICON ( [parallelise eddy identification code](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/ICON/identify_fast.py) and [compositing with higher res data](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/ICON/composite_tracks.py) than 0.25deg) by Moritz Epke
    - ICON ([read-in as xarray; parallel running](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/RESULTS/pyeddytracker_xarray_dask_parallel)) by Aaron Wienkers
    - [IFS-AMIP](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/eddy_composites-short.ipynb) (atm response) by Matthias Aengenheyster
    - [IFS/FESOM](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/IFS-FESOM/IDtrackeddy-daily-intake_IFSFESOM.ipynb) (use intake and read-in as xarray; parallel running) by Aaron Wienkers and Dian Putrasahan
    - [HAMOCC](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/HAMOCC/README.md) (read-in netcdf; serial running) by Johann Jungclaus and Dian Putrasahan
 - [Spatial filters](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md) on regular grid
    1. [Weighted area-average smoothing](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md#weighted-area-average-smoothing-using-cdo) using `cdo -smooth` operator. 
        - [Spatial filtering on HEALpix data](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md#bonus-spatial-filtering-on-healpix-data).
    2. [Bessel filter](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md#bessel-filter) using a function from py-eddy-tracker by Dian Putrasahan
    3. [Gaussian filter](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md#gaussian-filter) using a function from GCM filters by Matthias Aengenheyster and Dian Putrasahan
 - [Scale dependency of air-sea coupling](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/README.md)
    - [ICON](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/ICON/README.md) by Dian Putrasahan
    - [IFS/FESOM](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/IFS-FESOM/README.md) by Matthias Aengenheyster, Rohit Ghosh and Dian Putrasahan
- [Mean vs eddy fluxes in the ocean](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mean_eddy_flux/README.md)
    - [vertical heat fluxes in ICON](https://github.com/eerie-project/EERIE_hackathon_2023/blob/main/RESULTS/vertical_heat_flux_ICON_WP6_hackathon.ipynb) by Stella Bērziņa and Matthias Münnich
    - [in-situ or potential density from potential temperature and salinity](https://github.com/eerie-project/EERIE_hackathon_2023/tree/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mean_eddy_flux#in-situ-or-potential-density)
    - [find depth of isopycnal surfaces](https://github.com/eerie-project/EERIE_hackathon_2023/tree/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mean_eddy_flux#depth-of-isopycnal-surfaces)
- [Impact of eddies on atmosphere mean state (IFS-AMIP)](https://github.com/eerie-project/EERIE_hackathon_2023/tree/pre-joint-hackathon-2024/RESULTS)
    - [2D atm clim state](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_atmosresponse_to_SST_forcing_djf_clmdiff.ipynb) by Iuliia Polkova
    - [3D atm clim state](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_atmosresponse_to_SST_forcing_djf_clmdiff_3D.ipynb) by Iuliia Polkova
    - [atm covariability/correlation](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_atmosresponse_to_SST_forcing_djf_correlation.ipynb) by Iuliia Polkova
    - [local atm response (composites)](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/RESULTS/IFS_AMIP_composites.ipynb) by Chris Roberts and Matthias Aengenheyster


## Building python environment
Here are 3 options:
* [x] [Easiest option](#Easiest-option-pre-made-python-env-for-hackathon). Use pre-made environment that can be loaded via a 'module load'
* [x] [Use someone else's a working environment](https://pad.gwdg.de/bJMq4TloSCiPFeWjvsprGg?view#Using-someone-else%E2%80%99s-working-python-environment)
* [x] [Instructions to build your own python environment](https://pad.gwdg.de/bJMq4TloSCiPFeWjvsprGg?view#Build-your-own-python-environment), specifically for using py-eddy-tracker and GCM filters with EERIE and NextGEMS data
 
### Easiest option (pre-made python env for hackathon)

```
module use /work/k20200/k202134/hsm-tools/outtake/module
module rm python3
```

**Choose from 3 pre-made environments:**
For NextGEMS applications:
```
module load python3/hamburg-hackathon
python -m ipykernel install --name python-HH-hackathon --user
```
For pyeddytracker and GCM filters:
```
module load python3/hamburg-hackathon-eddyenv
python -m ipykernel install --name eddyenv-HH-hackathon --user
install_kernel --cdo /sw/spack-levante/cdo-2.3.0-mck3wy/bin/cdo --kernel_name hamburg-hackathon-eddyenv
```
For using an even newer python module on Levante:
```
module load python3/.newunstable
python -m ipykernel install --name newpy-HH-hackathon --user
```


# Hackathon breakout groups

On Tuesday, Wednesday and Thursday, we will be working in breakout groups. Below you will find information on the topics of the various breakout groups and the rooms in which these breakout groups will be located.

## Storms&Ocean 

All the breakout groups for Storms&Ocean will be in 22/23 in Bu53.

| Topics | Projects/WPs | Lead  |
| -------- | -------- | ------ |
| Atmospheric teleconnections/ Monsoon systems | NG 7.1/7.2 EERIE WP7/8  | Elsa Mohinjo, Simona Bordoni     |
| Tropical Cyclones | NG 7.3, <br> EERIE WP8 </br> | Pier-Luigi Vidale |
| Global primary productivity/ West African fisheries | NG 7.4, OBGC | Noel Keenlyside, Patrice Brehmer |
|Swirls and Shifts: <br> Impact of eddies on oceanic vertical fluxes and  horizontal flux divergence| NG 7.6, <br>EERIE WP6,</br> EPOC WP2| Fraser Goldsworth|
|Mystery of Arctic sea ice holes| NG 7.6, <br>EERIE WP6,</br> EPOC WP2 |  Oliver Gutjahr|
|Whirls of Wonder: <br>[Extracting mesoscales using GCM filter](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/Spatial_Filters/README.md) (day 1; MA lead) <br> Subgroups (day 2 & 3): </br> * Storms in the Southern Ocean, upper ocean structure, and carbon uptake (AK lead) <br> * [Spatial scale dependency of air-sea coupling](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/mesoscale-air-sea-coupling/README.md) (MA lead) <br> * [Eddy tracking and compositing](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/README.md) for 3D structure of eddies [T/S, BGC] or Marine heatwaves? (AW lead) </br>| NG 7.5, <br> EERIE WP5/7, </br> OBGC| Matthias Aengenheyster, <br> Arjun Kumar, </br> Aaron Wienkers, <br> (Dian Putrasahan provides support)
|Tropical Instability Waves and ocean mixing Deep Cycle Turbulence | NG 7.5, EERIE WP5/6/7 | Marcus Dengler, Johann Jungclaus


## Storms&Radiation

List of topics is provisional and may change. 

| Topics | Projects/WPs | Lead  |
| -------- | -------- | -------- |
| Drift, leaks, and where will the models land?         |          |           |
|Process-based evaluation of the energy budgets ||
|Cloud organisation|
|Circulation and clouds|
|Precipitation extremes|
|Global variability (potential cross-theme)|
|Bring your own...|


## Storms&Land 

Working towards papers, consolidate/collect results
- Diurnal variability over land in storm resolving models
    energy and water balance
    compare against observations
    combine global and local analysis
    land surface temperature, precip., 
    SW and LW radiation, 
    katabatic winds, 
    soil moisture-precip feedback

- Weaker land-atmosphere coupling



| Topics | Projects/WPs | Lead  |
| -------- | -------- | -------- |
|          |          |           |

## Room plan for breakout groups
![](https://pad.gwdg.de/uploads/0d84aa08-b647-486b-ba75-dc9f950fbe52.png)



