# 2023-07-21

# Generate SST & CI input data for given resolution

import numpy as np
import pandas as pd
import xarray as xr
import zarr
import dask
from glob import glob
from datetime import datetime
import os, sys
import time as T

def get_number_jobs():
    '''
    Count number of jobs currently on the queue
    '''
    os.system('squeue -u neam > status.txt')
    with open('status.txt','r') as f:
        lines = f.readlines()
        return len(lines) - 1

# SST products meant to be supported:
# ['OSTIA','ESAv2','ESAv3','GLORYS','ERA5']

product = 'OSTIA'
# product = 'ESAv2'
# product = 'ESAv3'
# product = 'GLORYS'
# resol = 'tco199'
resol = 'tco399'
# resol = 'tco319'
# resol = 'tco1279'
# smoothc = '0'
smoothc = 'LR30'
# smootha = '0'
smootha = 'LR30'

# Path and filenames for PERM storage files - "_4" denotes "GTYPE": _4 is for tco grids
assert resol[:3] == 'tco' # this only works for tco grids
if smoothc == '0' and smootha == '0':
    print('No filtering requested of either climatology or anomalies')
    # path_ancils = '/perm/neam/02_AMIP_IFS/ancil/{product}/{resoli}_4/'.format(
    # TESTING
    # path_ancils = '/perm/neam/02_AMIP_IFS/ancil/{product}_v7/{resoli}_4/'.format(
    path_ancils = '/perm/neam/01_SST_VAR/SST/gradients/{product}/{resoli}_4/'.format(
        product=product,resoli=resol[3:]
    )
else:
    path_ancils = '/perm/neam/01_SST_VAR/SST/gradients/{product}_c_{smoothc}_a_{smootha}/{resoli}_4/'.format(
        product=product,smoothc=smoothc,smootha=smootha,resoli=resol[3:]
    )

# pattern_ancil = 'sst_grad_{year:04d}{month:02d}{day:02d}.grib'
pattern_ancil = 'sst_grad_{year:04d}{month:02d}{day:02d}.nc'


def test_exist(year,month,day):
    '''
    Check if a file exists that should be one of the last ones created in the job
    '''
    testfilename = path_ancils + pattern_ancil.format(year=year,month=month,day=day)
    return os.path.exists(testfilename)

Nmax = 95 # maximum number of jobs allowed on the queue

dates = pd.date_range('2010-01-01','2021-12-31',freq='D')
# dates = pd.date_range('2018-01-01','2018-01-10',freq='D')
# dates = pd.date_range('2018-01-11','2018-01-20',freq='D')
# dates = pd.date_range('2021-01-01','2021-12-31',freq='D')
# dates = pd.date_range('2020-01-01','2020-12-31',freq='D')
# dates = pd.date_range('2020-01-01','2021-12-31',freq='D')
# dates = pd.date_range('1980-01-01','2021-12-31',freq='D')
# dates = pd.date_range('1982-01-01','2022-05-31',freq='D')
# dates = pd.date_range('2009-01-01','2022-05-31',freq='D')
# dates = pd.date_range('1982-01-01','2021-12-31',freq='D')
# dates = pd.date_range('2018-01-01','2018-03-31',freq='D')
# dates = pd.date_range('1993-01-01','2020-12-31',freq='D')
# dates = pd.date_range('1990-01-01','1990-07-01',freq='D')
# dates = pd.date_range('1990-01-01','1990-03-01',freq='D')

n = 1
print('Process %s SST gradient (clim smoothing %s, anomalies smoothing %s) to resolution %s for %i dates between %s and %s, to %s' % (product,smoothc,smootha,resol,len(dates),dates[0],dates[-1],path_ancils))
T.sleep(15)

for date in dates:

    ni = get_number_jobs()
    while ni >= Nmax:
        print('Too many jobs, take a 2 minute break before attempting to submit again\n\n=============================\n\n')
        print('2 more minutes')
        T.sleep(60)
        print('1 more minute')
        T.sleep(60)
        print('Go\n')
        ni = get_number_jobs()
        # continue

    year, month, day = date.year, date.month, date.day

    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ' : ' + 'Submit %.4i-%.2i-%.2i, %i / %i' % (year,month,day, n, len(dates)))

    command_str = "sbatch --wrap='module load conda && conda activate science39 && python compute_SST_grad.py {year:04d} {month:02d} {day:02d} {resol} {product} {smoothc} {smootha}' -q nf -t 00:15:00 --mail-type=FAIL --mail-user='matthias.aengenheyster@ecmwf.int' -o out/compute_SST_grad_{product}_{resol}_c_{smoothc}_a_{smootha}_{year:04d}{month:02d}{day:02d}.out -e err/compute_SST_grad_{product}_{resol}_c_{smoothc}_a_{smootha}_{year:04d}{month:02d}{day:02d}.err -J regrid_smooth".format(
        year=year,
        month=month,
        day=day,
        resol=resol,
        product=product,
        smoothc=smoothc,
        smootha=smootha
        )

    if not test_exist(year,month,day): # check if ancil data already exists
        print(command_str)
        os.system(command_str)
    else:
        print('Data already exists. Continue...')

    n += 1

print('\nDone with submitting\n')
print('\nNow monitor job queue until all jobs have finished\n')

# While loop to check if any regrid-tasks are still running
while True:
    T.sleep(60) # check every minute
    ni = get_number_jobs()
    with open('status.txt','r') as f:
        lines = f.readlines()
    job_is_regrid = ['regrid_smooth' in l for l in lines]
    still_running = any(job_is_regrid)
    if still_running:
        print('%i regridding jobs are still running' % sum(job_is_regrid))
    if not still_running:
        break

# Assert that the regridded file exists for all dates
T.sleep(60) # wait a minute
crash = False
for date in dates:
    year, month, day = date.year, date.month, date.day
    # assert test_exist(year,month,day)
    if not test_exist(year,month,day):
        print('Date %s does not exist in output even though requested.' % date)
        crash = True
assert crash==False, 'Not all dates exist in output'

print('Checked: Regridded SST gradient files for %s exist for all dates between %s and %s at resolution %s with clim smoothing %s, anomalies smoothing %s' % (product,dates[0],dates[-1],resol,smoothc,smootha))

print('Done')