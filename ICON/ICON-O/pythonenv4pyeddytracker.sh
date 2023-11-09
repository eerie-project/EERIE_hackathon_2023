
#Download py-eddy-tracker to a folder
# https://py-eddy-tracker.readthedocs.io/en/stable/

module load git
cd /work/mh0256/m300466/
git clone https://github.com/AntSimi/py-eddy-tracker pyeddytracker/
source /work/mh0256/m300466/miniconda3/bin/activate
cd /work/mh0256/m300466/pyeddytracker
pip install --target=/work/mh0256/m300466/pyeddytracker/lib/python3.10/site-packages --prefix=/work/mh0256/m300466/pyeddytracker pyEddyTracker


module purge
source /work/mh0256/m300466/miniconda3/bin/activate
mamba create -n pyeddytracker_intake python=3.10
conda activate pyeddytracker_intake
cd /work/mh0256/m300466/pyeddytracker/

#Create a requirements text file
vi requirements.txt
matplotlib
opencv-python
pint
polygon3
pyyaml
requests
scipy
zarr
netCDF4
numpy
numba


#Install the required packages
python -m pip install --upgrade pip
pip install flake8 pytest pytest-cov
pip install -r requirements.txt
pip install -e .


conda env list
source activate /work/mh0256/m300466/miniconda3/envs/pyeddytracker_intake
mamba install ipykernel
python -m ipykernel install --user --name intakeeddytrack_py3.10  --display-name="intakeeddytrack_py3.10"

conda install -c conda-forge xarray



